const mongoose = require("mongoose");

const farmerSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },

    phone: {
        type: String,
        required: true
    },

    district: {
        type: String,
        required: true
    },

    crop: {
        type: String,
        required: true
    }
});

module.exports = mongoose.model("farmer", farmerSchema);