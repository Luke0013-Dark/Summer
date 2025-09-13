# LINE Bot Webhook Application

A FastHTML-based webhook server that receives POST requests and triggers LINE Bot API calls.

## Features

- **FastHTML Framework**: Lightweight Python web framework
- **LINE Bot Integration**: Sends replies using LINE Bot API
- **Webhook Endpoint**: `/webhook` receives POST requests
- **Health Check**: `/` endpoint for server status
- **Test Endpoint**: `/test` for testing functionality

## Configuration

### LINE Bot API Settings
- **Channel Access Token**: `1b03475340e1479f2e396fc85491134a`
- **Reply Token**: `ZeFa2KBQj5Xt2aMb2Xhz88v4Nj93zMJ6TgKbDi2sVBWBgOVZYjbvBPcwKd6mH1OU5eHVgJhVgffNHDHIaETXklASefm73Qtb+2t1Rw/R0msEtlNpd2jiHmBFAHNkqAU0moK4DaH3PmxRXM2T1HhN/gdB04t89/1O/w1cDnyilFU=`

## API Endpoints

### `GET /`
Health check endpoint showing server status and configuration.

### `POST /webhook`
Main webhook endpoint that:
1. Receives POST requests with JSON data
2. Extracts reply token from webhook data
3. Sends reply messages to LINE Bot API
4. Returns success/error response

### `GET /test`
Test endpoint that simulates a webhook call and sends a test message.

## Usage

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python webhook_app.py

# Server runs on http://localhost:5000
```

### Test the Webhook
```bash
# Run the test script
python test_webhook.py

# Or visit http://localhost:5000/test in browser
```

### Docker Deployment
```bash
# Build Docker image
docker build -t line-webhook .

# Run container
docker run -p 5000:5000 line-webhook
```

## Webhook Request Format

The webhook expects JSON data in this format:
```json
{
  "events": [
    {
      "type": "message",
      "replyToken": "your_reply_token_here",
      "source": {
        "userId": "user_id",
        "type": "user"
      },
      "message": {
        "type": "text",
        "text": "Hello, this is a test message"
      }
    }
  ]
}
```

## LINE Bot API Response

The webhook sends this reply to LINE Bot:
```json
{
  "replyToken": "extracted_or_provided_token",
  "messages": [
    {
      "type": "text",
      "text": "Hello, user"
    },
    {
      "type": "text",
      "text": "May I help you?"
    }
  ]
}
```

## Environment Variables

- `PORT`: Server port (default: 5000)
- `CHANNEL_ACCESS_TOKEN`: LINE Bot channel access token
- `REPLY_TOKEN`: Default reply token (fallback)

## Dependencies

- `python-fasthtml`: FastHTML web framework
- `requests`: HTTP client for LINE Bot API calls

## Error Handling

- Invalid JSON data returns 400 error
- LINE Bot API failures return 500 error
- All errors are logged to console
- Graceful error responses to webhook caller
