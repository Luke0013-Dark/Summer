# How to Get a Valid Google GenAI API Key

## Step 1: Go to Google AI Studio
1. Visit: https://aistudio.google.com/
2. Sign in with your Google account

## Step 2: Create an API Key
1. Click on "Get API Key" in the left sidebar
2. Click "Create API Key"
3. Choose "Create API key in new project" or select an existing project
4. Copy the generated API key (it will look like: `AIzaSy...`)

## Step 3: Set the API Key in Railway
1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Variables" tab
4. Add a new environment variable:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: `your_actual_api_key_here` (paste the key from Step 2)
5. Click "Add"
6. Railway will automatically redeploy your app

## Step 4: Verify the Fix
1. Check the Railway logs to see if the API key validation passes
2. Try uploading an image to test the OCR functionality

## Important Notes:
- Keep your API key secure and don't share it publicly
- The API key should start with `AIzaSy` and be about 39 characters long
- Make sure there are no extra spaces or characters when copying the key
