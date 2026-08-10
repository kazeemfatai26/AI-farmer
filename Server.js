require("dotenv").config();

const express = require("express");
const connectDB = require("./src/config/db");

//Routes - add all the routes here
const farmersRoute = require("../Academic bootcamp/src/routes/farmersRoute")
const GenAIRoute = require("../Academic bootcamp/src/routes/GEN-AI-Route")

const app = express();

connectDB().then(r => {});

app.use(express.json());

//Endpoints - add all the endpoints here
app.use("/", farmersRoute)
app.use("/", GenAIRoute)

app.get("/", (req, res) => {
    res.send("API is running");
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});