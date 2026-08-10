const express = require ("express")
const farmers = require ("../models/farmers")
const router = express.Router();

router.post("/", async (req, res) => {
    try {
        const farmer = new farmers(req.body);

        const savedFarmer = await farmer.save();

        res.status(201).json(savedFarmer);

    } catch (error) {
        res.status(500).json({
            message: "Failed to create farmer",
            error: error.message
        });
    }
});

module.exports = router;