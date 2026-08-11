const mongoose = require("mongoose");

const GEN_AISchema = new mongoose.Schema({
    prompt: {
        type: String,
        required: true
    },

    response: {
        type: String,
        required: true
    },

});

module.exports = mongoose.model("GEN-AI", GEN_AISchema);