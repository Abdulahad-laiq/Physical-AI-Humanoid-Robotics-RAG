# Gemini API Quota Management Guide

## Current Status

✗ **All Gemini models have exhausted their free tier quota**

Your API key is **valid and working**, but you've hit the free tier limits.

## Quota Information

### Free Tier Limits (per day)
- **Requests**: 1,500 requests per day
- **Tokens**: ~1M input tokens per day
- **Rate**: 15 requests per minute

### Current Configuration
- Model: `gemini-1.5-flash` (recommended for free tier)
- Alternatives: `gemini-2.0-flash-exp`, `gemini-1.5-pro`

## Immediate Solutions

### Option 1: Wait for Quota Reset ⏰
Quotas reset at **midnight UTC daily**.

Check your current usage:
- Visit: https://ai.dev/usage?tab=rate-limit
- Monitor your quota consumption
- See when limits reset

### Option 2: Generate New API Key 🔑
If you have multiple Google accounts:

1. Go to: https://aistudio.google.com/apikey
2. Sign in with a different Google account
3. Create a new API key
4. Update `backend/.env` with the new key:
   ```env
   GEMINI_API_KEY=your_new_key_here
   ```

### Option 3: Upgrade to Paid Plan 💰
For production use, upgrade to pay-as-you-go:

1. Visit: https://ai.google.dev/pricing
2. Enable billing in Google Cloud Console
3. Much higher limits:
   - **1,000 requests per minute** (vs 15)
   - **4M tokens per minute** (vs daily limit)
   - Only pay for what you use (~$0.075 per 1M input tokens)

## Testing Your Configuration

### Quick Test
Run this to check if quota is available:

```bash
.venv\Scripts\python.exe backend\test_gemini_key.py
```

### Find Working Model
If one model is out of quota, test alternatives:

```bash
.venv\Scripts\python.exe backend\find_working_model.py
```

## Model Recommendations

### For Free Tier
**Primary:** `gemini-1.5-flash`
- Fastest response time
- Lowest token usage
- Best for chatbot/RAG applications

**Backup:** `gemini-2.0-flash-exp`
- Experimental but often available
- May have different quota pool

### For Paid Tier
**Primary:** `gemini-1.5-pro`
- Higher quality responses
- Better reasoning
- Recommended for production

**Alternative:** `gemini-2.0-flash`
- Latest model
- Good balance of speed and quality

## Error Handling

Your backend should gracefully handle quota errors. Check these files:

- `src/services/agent.py` - LLM service
- `src/api/v1/chat.py` - API endpoints

Expected error:
```
Error 429: RESOURCE_EXHAUSTED
Quota exceeded for metric: generativelanguage.googleapis.com/...
```

## Monitoring Best Practices

1. **Track Usage Daily**
   - Monitor at: https://ai.dev/usage
   - Set up alerts before hitting limits

2. **Implement Caching**
   - Cache common responses
   - Reduce redundant API calls

3. **Optimize Prompts**
   - Keep system prompts concise
   - Use retrieval to provide only relevant context

4. **Rate Limiting**
   - Already configured in backend (100 req/min)
   - Protects from accidental quota exhaustion

## Troubleshooting

### "All models show quota exceeded"
- **Cause**: Daily limit reached across all models
- **Solution**: Wait until midnight UTC or upgrade

### "Model not found" (404)
- **Cause**: Wrong model name or unavailable in region
- **Solution**: Use `gemini-1.5-flash` or `gemini-2.0-flash`

### "Invalid API key" (401)
- **Cause**: Expired or incorrect key
- **Solution**: Regenerate at https://aistudio.google.com/apikey

## Next Steps

1. ✓ API key updated in `backend/.env`
2. ✓ Model set to `gemini-1.5-flash`
3. ⏳ Wait for quota reset OR upgrade plan
4. ✓ Run test script to verify when quota is available

## Support

- **Gemini API Docs**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing
- **Usage Dashboard**: https://ai.dev/usage
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
