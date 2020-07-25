const express = require('express');
const app = express();
const PORT = process.env.PORT || 5000;
var bodyParser = require('body-parser');
const cors = require("cors");
const tweetRouter = require("./routes/tweet-router");
let foo;
const path = require('path');
const database = require("./config/db_configuration");

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cors());
app.use("/tweets", tweetRouter)

app.get("/welcome", (req, res) => {
    console.log(foo);
    // console.log(ka);
    res.send("Welcome to Beemo Application");
});

  
database.then(() =>
    app.listen(PORT, () =>
        console.log(`Server running on port ${PORT}`)
    )).catch(err => {
    console.log(err);
});
