# Hugging Face AI Agents Course

My hands-on work through Hugging Face's free [AI Agents Course](https://huggingface.co/learn/agents-course) — building agents from scratch across different frameworks, one unit at a time.

🎓 [Unit 1 Certificate of Fundamentals of Agents](https://huggingface.co/spaces/agents-course/unit_1_quiz/discussions/746#6a9c0f6f3c21cccf089ab5ce)

## Structure

Each unit lives in its own self-contained folder with its own `requirements.txt`.

| Folder | Framework | What it covers |
|---|---|---|
| [`unit1-smolagents`](./unit1-smolagents) | smolagents | Agent fundamentals — built a `CodeAgent` with two custom tools: a URL safety checker (VirusTotal API) and a domain age/WHOIS lookup tool |

*(More units added as the course progresses.)*

## Running a unit locally

Each folder is independent:

\```bash
cd unit1-smolagents
pip install -r requirements.txt
python app.py
\```

You'll need your own API keys (Hugging Face token, VirusTotal key) in a local `.env` file — see each unit's own README for specifics.