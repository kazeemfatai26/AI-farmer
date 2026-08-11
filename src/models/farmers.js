const mongoose = require("mongoose");

const farmerSchema = new mongoose.Schema({
    phone_number: {
        type: String,
        required: true
    },

    name: {
        type: String,
        required: true
    },

    district: {
        type: String,
        required: true
    },

    sector: {
        type: String,
        required: false
    },
    crop_type: {
        type: String,
        required: true
    },
    planting_date: {
        type: Date,
        required: true
    },
    preferred_language: {
        type: String,
        required: true
    }
}, {
    timestamps: true
});

module.exports = mongoose.model("farmer", farmerSchema);