const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const stateWise = new Schema ({

}, {strict: false});

module.exports = mongoose.model("stateData", stateWise);