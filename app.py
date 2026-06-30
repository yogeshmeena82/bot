import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "MySecretInstagramBotToken123"

# PASTE YOUR META ACCESS TOKEN INSIDE THE QUOTES BELOW
ACCESS_TOKEN = "YOUR_META_ACCESS_TOKEN_HERE"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return 'Verification failed', 403
        
    elif request.method == 'POST':
        data = request.json
        print("Incoming Event Data:", data)
        
        # Parse the Instagram messaging structure
        try:
            if data.get('object') == 'instagram':
                for entry in data.get('entry', []):
                    for messaging_event in entry.get('messaging', []):
                        sender_id = messaging_event['sender']['id']
                        
                        # Handle text messages
                        if 'message' in messaging_event and 'text' in messaging_event['message']:
                            incoming_text = messaging_event['message']['text']
                            print(f"Received text: '{incoming_text}' from Sender ID: {sender_id}")
                            
                            # Construct response text
                            reply_text = f"Hello! You said: {incoming_text}"
                            send_instagram_message(sender_id, reply_text)
                            
        except Exception as e:
            print("Error parsing event:", e)
            
        return 'EVENT_RECEIVED', 200

def send_instagram_message(recipient_id, text_to_send):
    """Sends a text message using the Instagram Graph API Send endpoint"""
    url = f"https://facebook.com{ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text_to_send}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print("Send API Response:", response.json())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
