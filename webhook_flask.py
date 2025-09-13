from flask import Flask, request, jsonify
import requests
import json
import os
import base64
import google.generativeai as genai

# Create Flask app
app = Flask(__name__)

# LINE Bot API configuration
CHANNEL_ACCESS_TOKEN = "1b03475340e1479f2e396fc85491134a"
REPLY_TOKEN = "E/1IgJu+jDjDhYJsPmvCRsozNANgqGNh2CA4FAa5lxRqkNnbGWmV76bvCjXV4Q64jGesR9dT+BV6zwaTnod/nhFFVzlZ0yI6B2kfQBXp/uaPhB7P/Njx7dY85V7ZM5XtsDYsg6cMZnWZE33HlCSZJgdB04t89/1O/w1cDnyilFU="

# LINE Bot API endpoints
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"
LINE_CONTENT_API_URL = "https://api-data.line.me/v2/bot/message/{messageId}/content"

# Configure Google GenAI
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("⚠️ GEMINI_API_KEY not set, OCR functionality will be limited")
    genai.configure(api_key="dummy_key")
else:
    genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_line_image_content(message_id):
    """Fetch image content from LINE Bot API"""
    try:
        print(f"📷 Fetching image content for message ID: {message_id}")
        
        headers = {
            'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
        }
        
        url = LINE_CONTENT_API_URL.format(messageId=message_id)
        print(f"🔗 LINE Content API URL: {url}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Successfully fetched image content ({len(response.content)} bytes)")
            return {"status": "success", "content": response.content, "content_type": response.headers.get('content-type', 'image/jpeg')}
        else:
            print(f"❌ Failed to fetch image content: {response.status_code} - {response.text}")
            return {"status": "error", "message": f"Failed to fetch image: {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Error fetching LINE image: {str(e)}")
        return {"status": "error", "message": f"Error: {str(e)}"}

def extract_text_from_image(image_data, content_type="image/jpeg"):
    """Extract text from image using Google GenAI"""
    try:
        print(f"🔍 Processing image with GenAI (type: {content_type})")
        
        # Convert image data to base64 for Gemini API
        img_base64 = base64.b64encode(image_data).decode()
        
        # Create the prompt for OCR
        prompt = "Extract all text from this image. Return only the extracted text, no additional formatting or explanations."
        
        print(f"🤖 Sending image to Gemini API...")
        
        # Use Gemini to extract text
        response = model.generate_content([prompt, {"mime_type": content_type, "data": img_base64}])
        
        if not response.text:
            print("⚠️ No text extracted from image")
            return "No text could be extracted from the image."
        
        print(f"✅ OCR Result: {response.text[:100]}...")
        return response.text
        
    except Exception as e:
        print(f"❌ Error processing image with GenAI: {str(e)}")
        return f"Error processing image: {str(e)}"

def send_line_reply(reply_token, messages):
    """Send reply message to LINE Bot API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
        }
        
        data = {
            "replyToken": reply_token,
            "messages": messages
        }
        
        print(f"📤 LINE API Request:")
        print(f"  URL: {LINE_API_URL}")
        print(f"  Headers: {headers}")
        print(f"  Payload: {json.dumps(data, indent=2)}")
        
        response = requests.post(LINE_API_URL, headers=headers, json=data)
        
        print(f"📥 LINE API Response:")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response Headers: {dict(response.headers)}")
        print(f"  Response Body: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Successfully sent reply to LINE Bot")
            return {"status": "success", "message": "Reply sent successfully"}
        else:
            print(f"❌ Failed to send reply: {response.status_code} - {response.text}")
            return {"status": "error", "message": f"Failed to send reply: {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Error sending LINE reply: {str(e)}")
        return {"status": "error", "message": f"Error: {str(e)}"}

@app.route('/')
def index():
    """Health check endpoint"""
    return "LINE Bot Webhook Server is running!"

@app.route('/health')
def health():
    """Simple health check for Railway"""
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook requests"""
    try:
        # Get the request body
        webhook_data = request.get_json()
        
        print(f"📨 Received webhook payload: {json.dumps(webhook_data, indent=2)}")
        
        # Extract reply token from webhook data
        reply_token = None
        if 'events' in webhook_data and len(webhook_data['events']) > 0:
            reply_token = webhook_data['events'][0].get('replyToken')
            print(f"Extracted replyToken: {reply_token}")
        
        # Use the provided reply token if not found in webhook data
        if not reply_token:
            reply_token = REPLY_TOKEN
            print(f"⚠️ Using provided reply token: {reply_token[:20]}...")
        else:
            print(f"📝 Using webhook reply token: {reply_token[:20]}...")
        
        # Process each event in the webhook
        for event in webhook_data.get('events', []):
            event_type = event.get('type')
            print(f"Event type: {event_type}")
            
            if event_type == 'message':
                message = event.get('message', {})
                message_type = message.get('type')
                print(f"Message type: {message_type}")
                
                if message_type == 'image':
                    # Handle image message
                    message_id = message.get('id')
                    print(f"📷 Processing image message with ID: {message_id}")
                    
                    # Fetch image content from LINE API
                    image_result = fetch_line_image_content(message_id)
                    
                    if image_result["status"] == "success":
                        # Process image with OCR
                        ocr_text = extract_text_from_image(
                            image_result["content"], 
                            image_result["content_type"]
                        )
                        
                        # Prepare reply with OCR result
                        messages = [
                            {
                                "type": "text",
                                "text": f"📷 Image received! Here's the extracted text:"
                            },
                            {
                                "type": "text",
                                "text": ocr_text
                            }
                        ]
                    else:
                        # Error fetching image
                        messages = [
                            {
                                "type": "text",
                                "text": f"❌ Sorry, I couldn't process the image. Error: {image_result['message']}"
                            }
                        ]
                
                elif message_type == 'text':
                    # Handle text message
                    text_content = message.get('text', '')
                    print(f"📝 Text message: {text_content}")
                    
                    # Prepare reply for text message
                    messages = [
                        {
                            "type": "text",
                            "text": "Hello, user"
                        },
                        {
                            "type": "text", 
                            "text": "May I help you?"
                        }
                    ]
                
                else:
                    # Handle other message types
                    print(f"ℹ️ Unsupported message type: {message_type}")
                    messages = [
                        {
                            "type": "text",
                            "text": f"Received {message_type} message. Please send an image for OCR processing or text for general chat."
                        }
                    ]
                
                # Send reply to LINE Bot API
                print(f"Sending reply with messages: {json.dumps(messages, indent=2)}")
                result = send_line_reply(reply_token, messages)
                
                if result["status"] != "success":
                    print(f"❌ Failed to send reply: {result['message']}")
        
        # Return response
        return jsonify({"status": "success", "message": "Webhook processed successfully"})
            
    except Exception as e:
        print(f"❌ Webhook processing error: {str(e)}")
        return jsonify({"status": "error", "message": f"Error processing webhook: {str(e)}"}), 500

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting Flask webhook server on port {port}")
    print(f"📡 Webhook endpoint: http://0.0.0.0:{port}/webhook")
    print(f"🏥 Health check: http://0.0.0.0:{port}/health")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=port, debug=False)
