const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tweet = new Schema({
    

    },{strict: false}
);

module.exports = mongoose.model("Tweet", tweet);