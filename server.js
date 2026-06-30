const express = require('express');
const app = express();
app.use(express.json());

// 1. THIS IS YOUR VERIFY TOKEN (You can change this string to whatever you want)
const VERIFY_TOKEN = "MySecretInstagramBotToken123";

app.all('/webhook', (req, res) => {
  if (req.method === 'GET') {
    // Meta handles verification handshake here
    let mode = req.query['hub.mode'];
    let token = req.query['hub.verify_token'];
    let challenge = req.query['hub.challenge'];

    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      res.status(200).send(challenge);
    } else {
      res.sendStatus(403);
    }
  } else if (req.method === 'POST') {
    // This is where your bot receives messages
    console.log("Received message data:", req.body);
    res.status(200).send('EVENT_RECEIVED');
  }
});

app.listen(5000, () => console.log('Webhook server running on port 5000'));

