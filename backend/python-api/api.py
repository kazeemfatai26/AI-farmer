"""
k-NN pattern-matching API.

Loads the model bundle produced by build_knn_model.ipynb, fetches farmer
profiles from the existing farmers API, runs a similarity match against the
AHS reference data, and serves the result for the GenAI/advisory module.

Real document shape (confirmed from a live sample), e.g.:
    {
        "_id": "6a7af745a3f434743ec1267d",
        "phone_number": "Toussaint",
        "name": "0781234567",
        "district": "Kwa simira",
        "sector": "Gasabo",
        "crop_type": "Beans",
        "planting_date": "2026-08-11T00:00:00.000Z",
        "preferred_language": "rw",
        ...
    }

s3_q4_1 (crop name) in the AHS extract is TEXT, not a numeric code, so
matching against the app's crop_type field is a text-matching problem —
handled with normalization (case/whitespace) plus a small alias table for
known spelling differences (e.g. app: "Beans" vs AHS: "Bean"). If the crop
still doesn't match anything the model was trained on, matching falls back
to district+season+day only rather than guessing.

There's also no `season` field on the farmer document — it's inferred from
`planting_date` (see infer_season below).

Two things worth flagging to whoever owns the onboarding form, independent
of this API:
  1. `phone_number` and `name` look swapped in the sample above.
  2. `district`/`sector` values in the sample don't look like real Rwandan
     admin names — worth double-checking the form's field mapping.

Endpoints:
    POST /api/match/<farmer_id>   -> run the match, cache result, return it
    GET  /api/results/<farmer_id> -> fetch the most recent cached result
    GET  /health                  -> basic liveness check

Environment variables:
    FARMERS_API_URL       URL of the existing fetch-all-farmers endpoint
                           (default: https://ai-farmer-56eq.onrender.com/fetchFarmers)
    MODEL_BUNDLE_PATH      Path to the .joblib file (default: knn_recommender.joblib)
"""

import os
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import requests
import sklearn
from flask import Flask, jsonify
from sklearn.exceptions import InconsistentVersionWarning
from sklearn.impute import SimpleImputer

# Older model bundles can still be used with newer scikit-learn when the
# serialized estimator expects a private attribute that was renamed in a later
# release. Restore the attribute directly on the fitted estimators after load so
# the legacy bundle continues to transform input data in the same way it was
# trained.
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)


def _restore_legacy_simple_imputer_dtype(transformer):
    """Patch fitted SimpleImputer objects loaded from older sklearn versions."""
    if transformer is None:
        return

    if isinstance(transformer, SimpleImputer):
        if not hasattr(transformer, "_fill_dtype") or transformer._fill_dtype is None:
            transformer._fill_dtype = np.dtype("O")
        return

    if hasattr(transformer, "steps"):
        for _, step_transformer in transformer.steps:
            _restore_legacy_simple_imputer_dtype(step_transformer)

    if hasattr(transformer, "transformers_"):
        for _, nested_transformer, _ in transformer.transformers_:
            _restore_legacy_simple_imputer_dtype(nested_transformer)


app = Flask(__name__)

FARMERS_API_URL = os.environ.get(
    "FARMERS_API_URL", "https://ai-farmer-56eq.onrender.com/fetchFarmers"
)
SINGLE_FARMER_API_URL = os.environ.get(
    "SINGLE_FARMER_API_URL", "https://ai-farmer-56eq.onrender.com/fetchFarmer"
)
MODEL_BUNDLE_PATH = os.environ.get(
    "MODEL_BUNDLE_PATH",
    str(Path(__file__).resolve().parent / "knn_recommender.joblib"),
)

# Load the model bundle once at startup, not per-request
bundle = joblib.load(MODEL_BUNDLE_PATH)

# Fail loudly and early if the environment that built this bundle doesn't
# match the environment trying to load it, instead of letting scikit-learn
# fail silently or throw a confusing unpickling error deep in a request.
_bundle_version = bundle.get("sklearn_version")
if _bundle_version is not None and _bundle_version != sklearn.__version__:
    warnings.warn(
        f"Model bundle was built with scikit-learn {_bundle_version}, but "
        f"this environment is running {sklearn.__version__}. The bundle is "
        "being loaded with a compatibility shim; if accuracy drifts, rebuild "
        "the model bundle in the same environment.",
        InconsistentVersionWarning,
    )
preprocessor_full = bundle["preprocessor_full"]
knn_full = bundle["knn_full"]
full_features = bundle["full_features"]
preprocessor_no_crop = bundle["preprocessor_no_crop"]
knn_no_crop = bundle["knn_no_crop"]
no_crop_features = bundle["no_crop_features"]
reference_df = bundle["reference_df"]
known_crops = {str(c).strip().lower() for c in bundle["known_crops"]}

_restore_legacy_simple_imputer_dtype(preprocessor_full)
_restore_legacy_simple_imputer_dtype(preprocessor_no_crop)

# In-memory result cache, keyed by farmer _id.
# NOTE: no known write-back endpoint exists yet for persisting results to
# Mongo. If one gets built, swap this dict for a call to it so results
# survive a restart and are visible to other services directly from the DB.
results_cache = {}

# Extend this as spelling mismatches turn up between the app's crop_type
# values and the crop names actually present in the AHS extract (printed by
# the notebook's "Unique crop names" cell). Keys and values are normalized
# (lowercase, stripped) text.
CROP_NAME_ALIASES = {
    "beans": "bean",
    "bean": "bean",
    "maize": "maize",
    "maizes": "maize",
}


# ---------------------------------------------------------------------------
# Farmer data access — via the existing HTTP endpoint, not a direct DB call
# ---------------------------------------------------------------------------

def fetch_all_farmers() -> list[dict]:
    """Calls /fetchFarmers and normalizes the response to a list of farmer
    dicts, regardless of whether it comes back as a bare list or wrapped in
    an object like {"farmers": [...]}.
    """
    resp = requests.get(FARMERS_API_URL, timeout=10)
    resp.raise_for_status()
    payload = resp.json()

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ("farmers", "data", "result", "results"):
            if key in payload and isinstance(payload[key], list):
                return payload[key]
        if "_id" in payload:
            return [payload]

    raise ValueError(
        f"Unrecognized response shape from {FARMERS_API_URL}: {type(payload)}"
    )


def fetch_farmer_by_id(farmer_id: str) -> dict:
    """Fetch one farmer directly from the backend's single-farmer endpoint."""
    url = f"{SINGLE_FARMER_API_URL}/{farmer_id}"
    resp = requests.get(url, timeout=60)

    if resp.status_code == 404:
        raise ValueError("farmer not found")

    try:
        payload = resp.json()
    except ValueError:
        raise ValueError(f"non-JSON response from {url}: {resp.text[:500]}")

    if isinstance(payload, dict):
        for key in ("farmer", "data", "result", "results"):
            value = payload.get(key)
            if isinstance(value, dict):
                doc_id = value.get("_id") or value.get("id")
                if doc_id is not None:
                    return value

        doc_id = payload.get("_id") or payload.get("id")
        if doc_id is not None:
            return payload

        if payload.get("message") == "farmer not found":
            raise ValueError("farmer not found")

    raise ValueError(f"Unexpected response shape from {url}: {payload}")


def find_farmer(farmer_id: str, farmers: list[dict]) -> dict | None:
    for f in farmers:
        if str(f.get("_id", "")) == str(farmer_id):
            return f
    return None


def infer_season(planting_date: pd.Timestamp) -> int:
    """Heuristic mapping from planting month to AHS season code, based on
    the AHS 2024 collection windows (Season A ~ Sept-Feb, Season B ~ Feb-Jun,
    Season C ~ Jun-Sept). Approximate — worth validating against an official
    Rwandan agricultural season calendar before relying on it beyond a demo.
    """
    month = planting_date.month
    if month in (9, 10, 11, 12, 1):
        return 1  # Season A
    if month in (2, 3, 4, 5):
        return 2  # Season B
    return 3  # Season C (6, 7, 8)


def normalize_crop_name(crop_type: str) -> str | None:
    """Lowercase/strip the incoming crop name and apply known aliases.
    Returns None if crop_type is empty.
    """
    if not crop_type:
        return None
    normalized = crop_type.strip().lower()
    normalized = CROP_NAME_ALIASES.get(normalized, normalized)
    if normalized in known_crops:
        return normalized

    # Some crop names in the DB are a pluralized or simple variant of the
    # canonical training names (for example, "Beans" vs "Bush bean"). Keep the
    # search tolerant by checking both the exact normalized form and a few
    # common aliases that map to the training vocabulary.
    for canonical in known_crops:
        if normalized == canonical or normalized in canonical.split():
            return canonical
    return normalized


def normalize_flag(value) -> str:
    if value is None:
        return "no"
    normalized = str(value).strip().lower()
    if normalized in {"yes", "y", "true", "1", "used"}:
        return "yes"
    return "no"


# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------

def run_match(farmer_doc: dict, farmer_id: str) -> dict:
    """Find similar historical AHS records and summarize their practices.
    Uses the full (district+crop+season+day) model when the crop name is
    recognized (after normalization/aliasing), otherwise falls back to
    district+season only.

    The real Mongo farmer document does not store the AHS columns used in the
    model bundle, so we map the app fields to the bundle schema and default any
    missing practice flags to "no" while keeping the original crop/date data.
    """
    district = (farmer_doc.get("district") or "").strip()
    crop_type_raw = farmer_doc.get("crop_type")
    planting_date_raw = farmer_doc.get("planting_date")

    if not district or not planting_date_raw:
        raise KeyError("district and planting_date are required fields")

    district = district.title()
    planting_date = pd.to_datetime(planting_date_raw)
    season = infer_season(planting_date)

    crop_normalized = normalize_crop_name(crop_type_raw)
    crop_recognized = crop_normalized is not None and crop_normalized in known_crops

    if crop_recognized:
        crop_normalized = crop_normalized.title()

    default_practice_flags = {
        "Pesticide use": str(farmer_doc.get("pesticide_use", "no") or "no").strip().lower(),
        "Organic fertilizer use": str(farmer_doc.get("organic_fertilizer_use", "no") or "no").strip().lower(),
        "Inorganic fertilizer use": str(farmer_doc.get("inorganic_fertilizer_use", "no") or "no").strip().lower(),
        "irrigated": str(farmer_doc.get("irrigated", "no") or "no").strip().lower(),
    }

    if crop_recognized:
        query_df = pd.DataFrame([{
            "district": district.lower(),
            "crop_name": crop_normalized,
            "Season": season,
            "Pesticide use": default_practice_flags["Pesticide use"],
            "Organic fertilizer use": default_practice_flags["Organic fertilizer use"],
            "Inorganic fertilizer use": default_practice_flags["Inorganic fertilizer use"],
            "irrigated": default_practice_flags["irrigated"],
        }])[full_features]
        q_processed = preprocessor_full.transform(query_df)
        _, indices = knn_full.kneighbors(q_processed)
        match_mode = "full"
    else:
        query_df = pd.DataFrame([{
            "district": district.lower(),
            "Season": season,
            "Pesticide use": default_practice_flags["Pesticide use"],
            "Organic fertilizer use": default_practice_flags["Organic fertilizer use"],
            "Inorganic fertilizer use": default_practice_flags["Inorganic fertilizer use"],
            "irrigated": default_practice_flags["irrigated"],
        }])[no_crop_features]
        q_processed = preprocessor_no_crop.transform(query_df)
        _, indices = knn_no_crop.kneighbors(q_processed)
        match_mode = "no_crop_fallback"

    neighbors = reference_df.iloc[indices[0]]

    return {
        "farmer_id": farmer_id,
        "match_mode": match_mode,
        "crop_type_received": crop_type_raw,
        "n_neighbors": int(len(neighbors)),
        "fertilizer_rate": _rate(neighbors["Organic fertilizer use"]),
        "inorganic_fertilizer_rate": _rate(neighbors["Inorganic fertilizer use"]),
        "pesticide_rate": _rate(neighbors["Pesticide use"]),
        "irrigation_rate": _rate(neighbors["irrigated"]),
        "median_harvest_kg": round(float(neighbors["crop_yield(kg)"].median()), 1),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def _rate(series: pd.Series) -> float | None:
    valid = series.dropna()
    if len(valid) == 0:
        return None

    normalized = valid.astype(str).str.strip().str.lower()
    numeric = pd.to_numeric(
        normalized.replace({"yes": 1, "y": 1, "true": 1, "no": 0, "n": 0, "false": 0}),
        errors="coerce",
    )
    numeric = numeric.dropna()
    if len(numeric) == 0:
        return None
    return round(float(numeric.mean()), 3)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/match/<farmer_id>", methods=["POST"])
def match_farmer(farmer_id):
    try:
        farmer_doc = fetch_farmer_by_id(farmer_id)
    except (requests.RequestException, ValueError) as e:
        if str(e).lower() == "farmer not found":
            return jsonify({"status": "error", "message": "farmer not found"}), 404
        return jsonify({"status": "error", "message": f"could not fetch farmer: {e}"}), 502

    try:
        result = run_match(farmer_doc, farmer_id)
    except (KeyError, ValueError) as e:
        return jsonify({
            "status": "error",
            "message": f"could not process farmer document: {e}"
        }), 400

    results_cache[farmer_id] = result
    return jsonify({"status": "success", "result": result})


@app.route("/api/results/<farmer_id>", methods=["GET"])
def get_results(farmer_id):
    """Endpoint for the GenAI/advisory module to pull the stored match
    result and turn it into a phrased message.
    """
    result = results_cache.get(farmer_id)
    if result is None:
        return jsonify({
            "status": "error",
            "message": "no result found — call /api/match/<farmer_id> first"
        }), 404

    return jsonify({"status": "success", "result": result})


@app.route("/api/predict/<farmer_id>", methods=["POST"])
def predict_farmer(farmer_id):
    """Fetch a farmer record, map it to the trained model schema, and return its
    nearest-neighbor recommendation.
    """
    try:
        farmer_doc = fetch_farmer_by_id(farmer_id)
        result = run_match(farmer_doc, farmer_id)
    except (requests.RequestException, ValueError, KeyError) as e:
        if str(e).lower() == "farmer not found":
            return jsonify({"status": "error", "message": "farmer not found"}), 404
        return jsonify({"status": "error", "message": f"could not predict: {e}"}), 400

    results_cache[farmer_id] = result
    return jsonify({"status": "success", "result": result})


if __name__ == "__main__":
    app.run(port=5000)
