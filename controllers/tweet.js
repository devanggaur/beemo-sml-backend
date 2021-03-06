// const python = require("../");
const Tweet = require('../models/tweets');
const stateData = require('../models/stateWiseCount');

const getTweet = (req, res) =>{
    console.log("Get data statrer");
    const spawn = require("child_process").spawn;
    const process = spawn('python',["./utils/getTweet.py"]);
    process.stdout.on('data', function(data) { 
        res.send(data.toString()); 
    } ) 
};

const storeTweet = async (req, res) =>{
    const tweet = req.body.tweet;
    let storeTweet = new Tweet({
        tweet_id : tweet.id,
        tweet_id_str : tweet.id_str,
        messsage : tweet.message,
        city: tweet.city,
        state: tweet.state,
        country: tweet.country,
        centroid: tweet.centroid,
        screen_name: tweet.screen_name,
        sentiments : tweet.sentiments
    });


    await storeTweet.save().then(createdTweet => {
        console.log("tweet successfully saved");
      });
    if(tweet.state != undefined){
    const createStateData =async ()=>{ 
        await new stateData({ state_id: tweet.state, value:0}).save(()=>
        console.log("Data created SuccessFully"));
    }
    await stateData.findOne({state_id: tweet.state},async (err,data)=>{
        console.log(data);
          if(!data){
            await createStateData();
          }
        if (err){ 
            console.log(err) 
        } 
        else{ 
            console.log("Updated User : ", docs); 
        } 
      });
    await stateData.findOneAndUpdate({state_id: tweet.state},{ 
        $inc: { value: 1 }
     }, {new: true });
    }
    res.send("data saved successfully");
};


const reTweet = (req, res) =>{
    const spawn = require("child_process").spawn;
    const process = spawn('python',["./utils/reTweet.py", req.body.message, req.body.tweetId]);
    process.stdout.on('data', function(data) { 
        res.send(data.toString()); 
    } ) 
};

const markFavourite = (req, res) => {
    const spawn = require("child_process").spawn;
    const process = spawn('python',["./utils/markFavourite.py", req.query.tweetId]);
    process.stdout.on('data', function(data) { 
        res.send(data.toString()); 
    } ) 
};

const sentiments = async (req, res) =>{
    let positive = 0;
    let negative = 0;
    let neutral = 0;
    await Tweet.find({}, async (err, tweets)=>{
        console.log(tweets.length)
       tweets.forEach(async (tweet)=>{
       
        if(tweet._doc.sentiments> 0){
            positive += 1;
        }
        if(tweet._doc.sentiments < 0){
            negative += 1;
        }
        if(tweet._doc.sentiments == 0){
            neutral += 1;
        }
       });
        
    });
    const sentimentsArray = [positive, neutral, negative];
    res.send(sentimentsArray);
};

const getStoredTweets = async (req, res) => {
    console.log("I reached");
    await Tweet.find({},async (err, tweets)=>{
        if(err){
            console.log(err);
        }
        console.log(tweets);
        await res.send({"tweets":tweets});
    });
}

const getStateWiseData = async(req, res) => {
    await stateData.find({}, async (err,data) =>{
        if(err){
            console.log(err);
            throw err;
        }
        await res.send({"data":data});
    });
}

module.exports = {
    getTweet : getTweet,
    storeTweet: storeTweet,
    reTweet : reTweet,
    sentiments : sentiments,
    markFavourite: markFavourite,
    getStoredTweets: getStoredTweets,
    getStateWiseData: getStateWiseData
}