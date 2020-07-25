const express = require("express");
const router = express.Router();

const TweetController = require("../controllers/tweet");

router.get("/", TweetController.getTweet);
router.post("/store", TweetController.storeTweet);
router.post("/reply", TweetController.reTweet);
router.get("/sentiments", TweetController.sentiments);
router.get("/like", TweetController.markFavourite);
router.get("/getStoredTweets", TweetController.getStoredTweets);
router.get("/stateWiseData", TweetController.getStateWiseData);

module.exports = router;