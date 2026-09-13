---
title: GAIA Final Agent
emoji: 🕵️
colorFrom: blue
colorTo: purple
sdk: static
pinned: false
---

# Final Challenge — GAIA Benchmark Agent

The capstone project for Hugging Face's Agents Course: build an agent, run it against 20 questions from the [GAIA benchmark](https://huggingface.co/papers/2311.12983), and score at least 30% to earn the course certificate.

**Result: 75% (15/16 questions attempted correctly)**

## Stack

- **Framework**: [smolagents](https://github.com/huggingface/smolagents) `CodeAgent`
- **Model**: `gemini-3.5-flash-lite` via LiteLLM — chosen after ruling out HF's free Inference Providers tier (tiny daily quota) and Groq (persistent `tool_choice` bugs with `gpt-oss` models, plus a 200k-token/day cap that a multi-step search agent burns through fast)
- **Tools**: DuckDuckGo web search, plus `requests`/`bs4`/`json`/`re` authorized so the agent can parse pages directly (e.g. Wikipedia's REST extract endpoint, live roster pages) when that's more reliable than search snippets alone

## What this agent does

For each question, it searches the web and/or parses pages directly, reasons over multiple steps (`max_steps=15`), and returns a single clean answer string — no explanation, matching GAIA's exact-match scoring.

## Known limitations

Two questions in the set require reading an attached file (a `.py` script and a `.xlsx` spreadsheet). The sandboxed code environment `CodeAgent` runs in blocks direct file-system access (`os`, `open`, `glob`, even `__import__` are all disallowed) as a safety measure, and there's no built-in mechanism connecting the agent to GAIA's file-download endpoint. Rather than guess, these two questions are filtered out at runtime via a `skip_extensions` check — an honest "can't currently solve this" rather than a blind answer.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with:

HF_TOKEN=your_hugging_face_token
GEMINI_API_KEY=your_gemini_api_key


## Run

```bash
python app.py
```

Opens a local Gradio interface — log in with your Hugging Face account, then click "Run Evaluation & Submit All Answers" to fetch the questions, run the agent, and submit for scoring.

## Notes on debugging this

Getting a reliable agent running locally (outside a hosted Space, due to free-tier hosting limits) surfaced a long list of issues worth documenting: Gradio's OAuth mock behavior when running locally, LiteLLM's internal retry/timeout quirks, a smolagents sandbox bug where authorizing `urllib.request` specifically breaks the import, `CodeAgent`'s default `<code>`-tag expectation not matching Gemini's natural markdown code-fence output (fixed via `code_block_tags="markdown"`), and provider-specific `tool_choice` bugs that made an earlier Groq-based version unreliable. Most of these weren't documented anywhere obvious — worked out through trial, error, and reading raw tracebacks.