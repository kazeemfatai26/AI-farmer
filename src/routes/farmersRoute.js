const express = require ("express")
const Farmer = require ("../models/farmers")
const router = express.Router();

router.post("/createFarmer", async (req, res) => {
    try {
        const farmer = new Farmer(req.body);

        const savedFarmer = await farmer.save();

        res.status(201).json(savedFarmer);

    } catch (error) {
        res.status(500).json({
            message: "Failed to create farmer",
            error: error.message
        });
    }
});

router.get("/fetchFarmers", async (req, res) => {
    try {
        const farmers = await Farmer.find();

        res.status(200).json(farmers);
    } catch (error) {
        res.status(500).json({
            message: "Failed to fetch farmers",
            error: error.message
        });
    }
});

router.get("/fetchFarmer/:id", async (req, res) => {
    try {
        const farmer = await Farmer.findById(req.params.id);

        if (!farmer) {
            return res.status(404).json({
                message: "Farmer not found"
            });
        }

        res.status(200).json(farmer);

    } catch (error) {
        res.status(500).json({
            message: "Failed to fetch farmer",
            error: error.message
        });
    }
});

module.exports = router;