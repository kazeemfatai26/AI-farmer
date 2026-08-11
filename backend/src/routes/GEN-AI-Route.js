const express = require ("express")
const GenAI = require ("../models/GEN-AI")
const router = express.Router();

router.post("/addPrompt", async (req, res) => {
    try {
        const Gen_AI = new GenAI(req.body);

        const savedPrompt = await Gen_AI.save();

        res.status(201).json(savedPrompt);

    } catch (error) {
        res.status(500).json({
            message: "Failed to save prompt",
            error: error.message
        });
    }
});

module.exports = router;