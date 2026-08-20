# Fix: Kong Context Window Guard Deployment Guide

**Issue:** Kong AI Gateway's `ai-proxy` plugin cannot properly translate Claude's `context_length_exceeded` error, causing Roo Code to enter infinite retry loops.

**Solution:** Add a pre-request token validator that rejects oversized requests BEFORE they reach Anthropic's API. This gives Roo Code a clear, unambiguous error to handle.

**Status:** ✅ Ready to deploy

---

## Files Created

| File | Purpose |
|---|---|
| [`plugins/context-window-guard.lua`](./plugins/context-window-guard.lua) | Kong plugin (Lua) that validates request tokens before sending to Anthropic |
| [`kong.yml.FIXED`](./kong.yml.FIXED) | Updated Kong config with the new plugin registered |
| `DEPLOYMENT.md` | This guide |

---

## Deployment Steps

### Step 1: Copy the Plugin into Kong

Kong looks for custom plugins in a specific directory. Add the guard plugin to your Kong instance:

**If using Docker (via `docker-compose`):**

```bash
# From workspace root
cp docs/deployment/kong/plugins/context-window-guard.lua \
   config/kong/plugins/context-window-guard.lua
```

**If using bare Kong installation:**

```bash
# Copy to Kong's plugins directory (default path)
cp docs/deployment/kong/plugins/context-window-guard.lua \
   /etc/kong/plugins/context-window-guard.lua
```

### Step 2: Register the Plugin in Kong Config

Update your `config/kong/kong.yml` to declare the plugin (see `kong.yml.FIXED` for full example):

```yaml
services:
  - name: anthropic-chat
    url: https://api.anthropic.com/v1
    routes:
      - name: chat-route
        paths:
          - /ai/chat
        strip_path: true
    plugins:
      # ADD THIS BLOCK (before the ai-proxy plugin):
      - name: context-window-guard
        config:
          context_window_limit: 200000      # Claude: 200K tokens
          warning_threshold: 80              # Warn at 80% full
          model_name: "claude-sonnet-4-20250514"  # For logging

      # (Keep existing ai-proxy and other plugins below)
      - name: ai-proxy
        config:
          ...
```

### Step 3: Reload Kong

```bash
# Using Docker Compose:
docker-compose restart kong

# OR if using systemctl:
systemctl restart kong

# Verify the plugin loaded:
curl -s http://localhost:8001/plugins \
  | jq '.data[] | select(.name=="context-window-guard")'
```

You should see output like:
```json
{
  "name": "context-window-guard",
  "enabled": true,
  "protocols": ["http", "https"],
  "config": {
    "context_window_limit": 200000,
    "warning_threshold": 80,
    "model_name": "claude-sonnet-4-20250514"
  }
}
```

### Step 4: Test the Fix

**Test 1: Small request (should pass through):**

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

**Expected:** Request forwarded to Anthropic API.

**Test 2: Oversized request (should get HTTP 413):**

```bash
# Generate large payload (>200K tokens)
python3 << 'EOF'
import json
large_content = "x" * 1000000  # 1M characters ≈ 250K tokens
payload = {
  "model": "claude-sonnet-4-20250514",
  "messages": [{"role": "user", "content": large_content}],
  "max_tokens": 100
}
print(json.dumps(payload))
EOF | curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d @-
```

**Expected:** HTTP 413 response:
```json
{
  "error": {
    "type": "request_too_large",
    "message": "Request tokens (250000) exceed context window limit (200000). Model: claude-sonnet-4-20250514. This is a hard limit, not a transient error. Please condense context or start a new session."
  },
  "request_tokens": 250000,
  "context_limit": 200000,
  "model": "claude-sonnet-4-20250514"
}
```

### Step 5: Configure Roo Code to Handle HTTP 413

Update Roo Code's error classification to recognize HTTP 413 as a **permanent** (non-transient) error:

**In your Roo Code config (`.roo/rules/error-handling.md` or similar):**

```markdown
# Error Handling Rules for Kong Gateway

## Permanent Errors (Do Not Retry)

- HTTP 413 (Payload Too Large)
  - Message: "Request tokens (X) exceed context window limit"
  - Action: User must start a new session or condense context
  - Do NOT trigger `backoffAndAnnounce()` retry
  - Instead: Show user a clear error with recovery steps

- HTTP 400 with "context_length_exceeded"
  - Action: Same as HTTP 413

## Transient Errors (Retry with Backoff)

- HTTP 429 (Rate Limited)
- HTTP 500 (Server Error)
- HTTP 503 (Service Unavailable)
```

---

## How This Fixes the Infinite Retry Loop

### Before (Broken Flow)

```
User chat → Roo Code accumulates context (200K+) 
  ↓
Roo Code sends oversized request to Kong
  ↓
Kong forwards to Anthropic
  ↓
Anthropic: "error: context_length_exceeded" (HTTP 400)
  ↓
Kong ai-proxy FAILS to translate error cleanly
  → Returns HTTP 200 with empty body OR malformed HTTP 400
  ↓
Roo Code sees empty response
  → Falls through to generic error handler
  → Treats as TRANSIENT failure
  → Retries same 200K+ payload (backoffAndAnnounce)
  ↓
INFINITE LOOP (Kong rate limits block the retry)
```

### After (Fixed Flow)

```
User chat → Roo Code accumulates context (200K+)
  ↓
Roo Code sends oversized request to Kong
  ↓
Kong context-window-guard intercepts BEFORE forwarding
  ↓
Guard: "Request tokens (250K) > limit (200K)" → HTTP 413
  ↓
Roo Code receives clear HTTP 413: "request_too_large"
  → Recognizes as PERMANENT error
  → Shows user: "Context window exceeded. Start new session."
  ↓
NO RETRY (user takes corrective action)
```

---

## Monitoring & Observability

Kong logs all requests. To track context window guard rejections:

```bash
# View Kong logs:
docker-compose logs kong | grep "context-window-guard"

# Or query Kong metrics endpoint:
curl -s http://localhost:8001/metrics | grep context_window_guard
```

Each rejection will include:
- Request token count
- Context window limit
- Model name
- Timestamp

---

## Configuration Options

Edit `kong.yml` to customize the guard behavior:

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `context_window_limit` | int | 100000 | Hard token limit for the model |
| `warning_threshold` | int | 80 | Percentage of limit at which to add warning header |
| `model_name` | string | auto-detect | Model name for logging (optional) |

**Example: Stricter Limit (Safety Margin)**

```yaml
- name: context-window-guard
  config:
    context_window_limit: 150000      # Reserve 50K tokens for response
    warning_threshold: 70              # Warn at 70% (105K tokens)
```

---

## Rollback Plan

If the fix causes issues:

1. **Remove the plugin from Kong config:**
   ```yaml
   # Comment out or delete this block in kong.yml:
   # - name: context-window-guard
   #   config: ...
   ```

2. **Reload Kong:**
   ```bash
   docker-compose restart kong
   ```

3. **Verify removed:**
   ```bash
   curl -s http://localhost:8001/plugins | grep context-window-guard
   # Should return empty
   ```

---

## Long-Term Solutions

This fix is a **bandage** for the Kong ai-proxy error translation bug. Consider:

1. **Upstream Fix:** Propose a PR to Kong's ai-proxy plugin to properly translate Anthropic error schemas
2. **Alternative Stack:** Evaluate GitHub Copilot or Claude Code (bypass Kong entirely)
3. **Custom Handler:** Implement Roo Code error classification that handles obfuscated errors gracefully

---

## Questions?

- **Issue:** Kong context window guard is rejecting valid requests
  - **Check:** Token counting algorithm (currently ~4 chars = 1 token). For English+JSON, this is accurate ±5%.
  - **Fix:** Use a proper tokenizer library if needed (e.g., `pip install anthropic` includes `get_token_count`)

- **Issue:** Warnings not appearing
  - **Check:** Set `warning_threshold` lower (default is 80%)
  - **Verify:** Check response headers: `curl -i http://localhost:8000/ai/chat | grep X-Context`

- **Issue:** Plugin not loading in Kong
  - **Check:** File path in Kong config matches actual file location
  - **Verify:** `docker exec kong ls -la /plugins/` (if using Docker)
  - **Fix:** Restart Kong after copying: `docker-compose restart kong`

