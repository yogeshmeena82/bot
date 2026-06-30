from flask import Flask, request

app = Flask(__name__)

# 1. THIS IS YOUR VERIFY TOKEN (You can change this string to whatever you want)
VERIFY_TOKEN = "MySecretInstagramBotToken123"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Meta handles verification handshake here
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return 'Verification failed', 403
        
    elif request.method == 'POST':
        # This is where your bot receives messages
        data = request.json
        print("Received message data:", data)
        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(port=5000)

