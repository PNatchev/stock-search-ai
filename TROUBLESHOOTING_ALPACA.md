# Troubleshooting Alpaca API Subscription Block on Hugging Face Spaces

## Problem
You can use Alpaca API locally but get "API subscription block" errors when deploying to Hugging Face Spaces.

## Common Causes & Solutions

### 1. **Sandbox vs Production API Keys** (Most Common)

Alpaca provides two types of API keys:
- **Sandbox Keys**: For testing, have limited access and may not work on third-party platforms
- **Production Keys**: Full access, required for deployment on platforms like Hugging Face Spaces

**Solution:**
1. Log into your [Alpaca Dashboard](https://app.alpaca.markets/)
2. Go to **API Keys** section
3. Ensure you're using **Production API Keys** (not Sandbox keys)
4. Update your Hugging Face Space secrets with the production keys:
   - `ALPACA_API_KEY` → Your production API key
   - `ALPACA_SECRET_KEY` → Your production secret key

**How to identify:**
- Sandbox keys typically have different prefixes or are clearly labeled as "Sandbox"
- Production keys are your main trading account keys

### 2. **API Subscription Tier**

Some Alpaca subscription tiers may have restrictions on:
- Third-party platform deployments
- API call limits
- Data access permissions

**Solution:**
1. Check your Alpaca subscription tier in the dashboard
2. Verify that your tier supports API access from external platforms
3. If needed, upgrade your subscription plan
4. Contact Alpaca support if you're unsure about your tier's capabilities

### 3. **IP Address Restrictions**

Your API keys might be configured to only work from specific IP addresses.

**Solution:**
1. Check your Alpaca API key settings for IP restrictions
2. Remove IP restrictions or add Hugging Face Spaces IP ranges
3. Note: Hugging Face Spaces uses dynamic IPs, so IP whitelisting may not be practical

### 4. **Environment Variables Not Set Correctly**

The API keys might not be properly configured as secrets in Hugging Face Spaces.

**Solution:**
1. Go to your Space settings on Hugging Face
2. Navigate to **Settings → Secrets**
3. Verify these secrets are set:
   - `ALPACA_API_KEY` (exact name, case-sensitive)
   - `ALPACA_SECRET_KEY` (exact name, case-sensitive)
4. Ensure there are no extra spaces or characters
5. Redeploy your Space after updating secrets

### 5. **Rate Limiting**

Hugging Face Spaces might be making requests from shared infrastructure that hits rate limits faster.

**Solution:**
1. Add retry logic with exponential backoff
2. Implement request caching where appropriate
3. Monitor your API usage in the Alpaca dashboard
4. Consider upgrading your subscription if you're hitting limits

## Verification Steps

1. **Test API Keys Locally:**
   ```python
   from alpaca.data.historical import StockHistoricalDataClient
   import os
   
   client = StockHistoricalDataClient(
       api_key=os.getenv("ALPACA_API_KEY"),
       secret_key=os.getenv("ALPACA_SECRET_KEY"),
   )
   # Try a simple request
   ```

2. **Check Space Logs:**
   - Go to your Hugging Face Space
   - Check the **Logs** tab for detailed error messages
   - Look for specific error codes (403, 401, etc.)

3. **Verify Environment Variables:**
   - Add a debug endpoint to print environment variable names (without values)
   - Ensure variables are being loaded correctly

## Additional Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca Support](https://alpaca.markets/support)
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)

## Quick Checklist

- [ ] Using production API keys (not sandbox)
- [ ] API keys set as secrets in HF Space settings
- [ ] Secret names match exactly: `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`
- [ ] Subscription tier supports external platform access
- [ ] No IP restrictions on API keys
- [ ] Checked Space logs for specific error messages

