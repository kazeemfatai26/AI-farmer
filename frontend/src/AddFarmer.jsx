import {useState} from 'react';

const AddFarmer = ({ onAddFarmer }) => {
const [name, setName] = useState("");
const [phoneNumber, setPhoneNumber] = useState("");
const [district, setDistrict] = useState("");
const [sector, setSector] = useState("");
const [cropType, setCropType] = useState("");
const [plantingDate, setPlantingDate] = useState("");
const [preferredLanguage, setPreferredLanguage] = useState("rw");

const [successMessage, setSuccessMessage] = useState("");

const [isSubmitting, setIsSubmitting] = useState(false);

const [showForm, setShowForm] = useState(true);

const handleSubmit = async (e) => {
  e.preventDefault();

  setIsSubmitting(true);

  const newFarmer = {
    name: name,
    phone_number: phoneNumber,
    district: district,
    sector: sector,
    crop_type: cropType,
    planting_date: plantingDate,
    preferred_language: preferredLanguage,
  };

  try {
    const response = await fetch("https://ai-farmer-56eq.onrender.com/createFarmer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newFarmer),
    });

    if (!response.ok) {
      throw new Error("Failed to save farmer");
    }

    const savedFarmer = await response.json();
    if (typeof onAddFarmer === "function") {
      onAddFarmer(savedFarmer);
    }
   setSuccessMessage(`${savedFarmer.name} was registered successfully!`);
   setShowForm(false);
   setIsSubmitting(false);
  } catch (error) {
    console.error("Error adding farmer:", error);
    alert("Something went wrong while saving. Please try again.");
     setIsSubmitting(false);
  }
};

const handleRegisterAnother = () => {   // ← ADD IT HERE, right after
        setName("");
        setPhoneNumber("");
        setDistrict("");
        setSector("");
        setCropType("");
        setPlantingDate("");
        setPreferredLanguage("rw");
        setSuccessMessage("");
        setShowForm(true);
    };

    return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-green-700">Add Farmer</h2>
        {successMessage && (
      <div className="mb-4 p-4 bg-green-100 text-green-800 rounded-lg border border-green-300">
        <p className="font-semibold">{successMessage}</p>
      </div>
    )}
        {showForm ? (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div className="mb-4">
                <label htmlFor="name" className="block text-gray-700 font-semibold mb-2">Full Name</label>
                <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
            </div>

            <div className="mb-4">
                <label htmlFor="phoneNumber" className="block text-gray-700 font-semibold mb-2">Phone Number</label>
                <input type="tel" id="phoneNumber" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
            </div>

            <div className="mb-4">
                <label htmlFor="district" className="block text-gray-700 font-semibold mb-2">District</label>
                <input type="text" id="district" value={district} onChange={(e) => setDistrict(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
            </div>

            <div className="mb-4">
                <label htmlFor="sector" className="block text-gray-700 font-semibold mb-2">Sector</label>
                <input type="text" id="sector" value={sector} onChange={(e) => setSector(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
            </div>

            <div className="mb-4">
                <label htmlFor="cropType" className="block text-gray-700 font-semibold mb-2">Crop Type</label>
                <select id="cropType" value={cropType} onChange={(e) => setCropType(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required>
                    <option value="">Select a crop</option>
                    <option value="Maize">Maize</option>
                    <option value="Beans">Beans</option>
                    <option value="Coffee">Coffee</option>
                    <option value="Tea">Tea</option>
                    <option value="Bananas">Bananas</option>
                    <option value="Cassava">Cassava</option>
                    <option value="Rice">Rice</option>
                </select>
            </div>

            <div className="mb-4">
                <label htmlFor="plantingDate" className="block text-gray-700 font-semibold mb-2">Planting Date</label>
                <input type="date" id="plantingDate" value={plantingDate} onChange={(e) => setPlantingDate(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300" required />
            </div>

            <div className="mb-4">
                <label htmlFor="preferredLanguage" className="block text-gray-700 font-semibold mb-2">Preferred Language</label>
                <select id="preferredLanguage" value={preferredLanguage} onChange={(e) => setPreferredLanguage(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-300">
                    <option value="rw">Kinyarwanda</option>
                </select>
            </div>

             <button type="submit"   disabled={isSubmitting} className="w-full bg-green-700 text-white font-bold rounded cursor-pointer py-2 hover:bg-green-800">
                    {isSubmitting ? "Registering..." : "Register Farmer"}
                </button>
        </form>
        ) : (
      <button
        onClick={handleRegisterAnother}
        className="w-full bg-green-700 text-white font-bold rounded cursor-pointer py-2 hover:bg-green-800"
      >
        Register Another Farmer
      </button>
    )}
    </div>
);
}

export default AddFarmer;
