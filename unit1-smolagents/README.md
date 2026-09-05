---
title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.23.1
app_file: app.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- agent-course
---

# Unit 1 — Agent Fundamentals (smolagents)

A `CodeAgent` built with [smolagents](https://github.com/huggingface/smolagents), featuring two custom tools:

- **`check_url_safety`** — scans a URL against VirusTotal's threat intelligence API and returns a safety verdict
- **`check_domain_age`** — looks up a domain's WHOIS registration date, useful for spotting recently-registered (often suspicious) domains

## Setup

\```bash
pip install -r requirements.txt
\```

Create a `.env` file with:
\```
HF_TOKEN=your_hugging_face_token
VIRUSTOTAL_API_KEY=your_virustotal_key
\```

## Run

\```bash
python app.py
\```

Opens a local Gradio chat interface where you can interact with the agent.