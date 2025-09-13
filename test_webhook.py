#!/usr/bin/env python3
"""
Test script for the LINE Bot webhook
"""
import requests
import json

# Test webhook endpoint
WEBHOOK_URL = "http://localhost:5000/webhook"

def test_webhook():
    """Test the webhook endpoint"""
    
    # Test data simulating a LINE webhook
    test_data = {
        "events": [
            {
                "type": "message",
                "replyToken": "ZeFa2KBQj5Xt2aMb2Xhz88v4Nj93zMJ6TgKbDi2sVBWBgOVZYjbvBPcwKd6mH1OU5eHVgJhVgffNHDHIaETXklASefm73Qtb+2t1Rw/R0msEtlNpd2jiHmBFAHNkqAU0moK4DaH3PmxRXM2T1HhN/gdB04t89/1O/w1cDnyilFU=",
                "source": {
                    "userId": "test_user_123",
                    "type": "user"
                },
                "message": {
                    "type": "text",
                    "text": "Hello, this is a test message"
                },
                "timestamp": 1234567890123
            }
        ]
    }
    
    try:
        print("🧪 Testing webhook endpoint...")
        print(f"📡 URL: {WEBHOOK_URL}")
        print(f"📦 Data: {json.dumps(test_data, indent=2)}")
        
        # Send POST request
        response = requests.post(
            WEBHOOK_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the webhook server is running on port 5000")
    except Exception as e:
        print(f"❌ Test error: {str(e)}")

if __name__ == "__main__":
    test_webhook()
