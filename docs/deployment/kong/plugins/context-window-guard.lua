-- Kong Plugin: context-window-guard
-- Purpose: Pre-request token counting and context window validation for LLM calls
-- Prevents "context_length_exceeded" errors by rejecting oversized payloads early
--
-- Models supported:
--   - Anthropic Claude (200K context: Sonnet, Opus)
--   - OpenAI GPT-4 (128K context)
--   - Generic token approximation (4 chars ≈ 1 token)
--
-- Author: Generated fix for Kong ai-proxy context window issue
-- Date: 2026-08-20

local plugin = {
  PRIORITY = 1000,  -- Run BEFORE ai-proxy (which has priority 400)
  VERSION = "1.0.0",
}

-- Token counting: naive approximation
-- Production systems should use a proper tokenizer library (e.g., tiktoken)
local function estimate_tokens(text)
  if not text then return 0 end
  -- Rough approximation: 4 characters = 1 token (works for English + JSON)
  return math.ceil(string.len(text) / 4)
end

-- Extract model context window limit from Kong plugin config or model name
local function get_context_window_limit(conf, model_name)
  -- If explicit limit configured, use it
  if conf.context_window_limit then
    return conf.context_window_limit
  end

  -- Infer from model name
  if model_name then
    if string.find(model_name, "claude%-opus") then
      return 200000  -- Claude Opus: 200K
    elseif string.find(model_name, "claude%-sonnet") then
      return 200000  -- Claude Sonnet: 200K
    elseif string.find(model_name, "gpt%-4%-turbo") then
      return 128000  -- GPT-4 Turbo: 128K
    elseif string.find(model_name, "gpt%-4o") then
      return 128000  -- GPT-4o: 128K
    end
  end

  -- Default fallback: conservative estimate
  return 100000
end

-- Calculate total payload size (messages + system prompt + tools + metadata)
local function estimate_request_tokens(request_body, conf)
  if not request_body then return 0 end

  local cjson = require("cjson")
  local total = 0

  -- Parse JSON request
  local ok, payload = pcall(function() return cjson.decode(request_body) end)
  if not ok then
    return 0  -- Can't parse; let it through (Kong ai-proxy will handle errors)
  end

  -- Count messages
  if payload.messages then
    for _, msg in ipairs(payload.messages) do
      if msg.content then
        if type(msg.content) == "string" then
          total = total + estimate_tokens(msg.content)
        elseif type(msg.content) == "table" then
          for _, block in ipairs(msg.content) do
            if block.text then
              total = total + estimate_tokens(block.text)
            end
          end
        end
      end
    end
  end

  -- Count system prompt
  if payload.system then
    total = total + estimate_tokens(payload.system)
  end

  -- Count tools definition (if present)
  if payload.tools then
    local tools_json = cjson.encode(payload.tools)
    total = total + estimate_tokens(tools_json)
  end

  -- Add safety margin for model-generated response + internal tokens
  -- (typically 10-15% overhead for response generation)
  total = total + math.floor(total * 0.15)

  return total
end

-- Main plugin handler
function plugin:access(conf)
  local request_body = ngx.var.request_body
  
  -- Only check LLM chat completions (not embeddings, not other routes)
  if ngx.var.uri ~= "/ai/chat" and ngx.var.uri ~= "/llm/v1/chat" then
    return
  end

  -- Estimate request size
  local request_tokens = estimate_request_tokens(request_body, conf)

  -- Get model from request body or use configured default
  local model_name = conf.model_name
  if not model_name then
    local cjson = require("cjson")
    local ok, payload = pcall(function() return cjson.decode(request_body) end)
    if ok and payload.model then
      model_name = payload.model
    end
  end

  -- Determine context window limit
  local limit = get_context_window_limit(conf, model_name)

  -- Reject if oversized
  if request_tokens > limit then
    ngx.status = 413  -- HTTP 413 Payload Too Large
    ngx.header["Content-Type"] = "application/json"
    
    local response = {
      error = {
        type = "request_too_large",
        message = string.format(
          "Request tokens (%d) exceed context window limit (%d). " ..
          "Model: %s. This is a hard limit, not a transient error. " ..
          "Please condense context or start a new session.",
          request_tokens, limit, model_name or "unknown"
        ),
      },
      request_tokens = request_tokens,
      context_limit = limit,
      model = model_name,
    }

    ngx.say(require("cjson").encode(response))
    return ngx.exit(ngx.HTTP_REQUEST_ENTITY_TOO_LARGE)
  end

  -- If configured, add warning header for requests near the limit
  if conf.warning_threshold then
    local threshold = math.floor(limit * (conf.warning_threshold / 100))
    if request_tokens > threshold then
      ngx.header["X-Context-Window-Warning"] = string.format(
        "%d/%d tokens (%.1f%% full)",
        request_tokens, limit,
        (request_tokens / limit) * 100
      )
    end
  end
end

return plugin
