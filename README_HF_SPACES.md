# Deploying to Hugging Face Spaces

This guide explains how to deploy the Stock Search AI application to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account
2. API keys for:
   - OpenAI API (for the AI agent)
   - Alpaca Markets API (for stock data)

## Deployment Steps

### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Configure:
   - **Space name**: Choose a name (e.g., `stock-search-ai`)
   - **SDK**: Select `Gradio`
   - **Hardware**: Select `CPU basic` (or higher if needed)
   - **Visibility**: Choose Public or Private

### 2. Upload Files

Upload the following files to your Space:

- `app.py` (entry point for HF Spaces)
- `requirements.txt` (dependencies)
- `src/main.py` (main application)
- `src/alpaca_client.py` (Alpaca API client)
- `README.md` (optional, for Space description)

### 3. Set Up Secrets

In your Space settings, go to **Settings → Secrets** and add:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ALPACA_API_KEY`: Your Alpaca Markets API key
- `ALPACA_SECRET_KEY`: Your Alpaca Markets secret key

These will be automatically available as environment variables.

### 4. Deploy

The Space will automatically build and deploy when you push the files. You can monitor the build logs in the Space's "Logs" tab.

## File Structure for HF Spaces

```
your-space/
├── app.py                 # Entry point (required)
├── requirements.txt       # Dependencies (required)
├── README.md             # Space description (optional)
└── src/
    ├── main.py           # Main application
    └── alpaca_client.py  # Alpaca API client
```

## Using Git to Deploy

Alternatively, you can use Git to push your code:

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy your files
cp /path/to/stock-search-ai/app.py .
cp /path/to/stock-search-ai/requirements.txt .
cp -r /path/to/stock-search-ai/src .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

## Troubleshooting

### Build Errors

- Check that `requirements.txt` includes all dependencies
- Verify that `app.py` exists in the root directory
- Check the build logs for specific error messages

### API Key Issues

- Ensure all secrets are set in Space settings
- Verify that environment variable names match exactly:
  - `OPENAI_API_KEY`
  - `ALPACA_API_KEY`
  - `ALPACA_SECRET_KEY`

### Import Errors

- Make sure `src/` directory is included in your Space
- Verify that `app.py` correctly adds `src` to the Python path

## Notes

- The app will automatically use environment variables from HF Spaces secrets
- No `.env` file is needed for deployment (it's only used for local development)
- The app runs on HF Spaces infrastructure, so no need to configure ports or hosts

