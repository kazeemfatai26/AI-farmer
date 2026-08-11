require("dotenv").config();

const express = require("express");
const connectDB = require("./src/config/db");
const cors = require("cors");

//Routes - add all the routes here
const farmersRoute = require("./src/routes/farmersRoute")
const GenAIRoute = require("./src/routes/GEN-AI-Route")

const app = express();

connectDB().then(r => {});


app.use(express.json());
app.use(cors());
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