# resume-chat

AI-powered resume chat for John Woo — lets recruiters and hiring agents ask natural-language questions about his work experience and technical skills.

Live at **[resume.etfai.ca](https://resume.etfai.ca)**

---

## What it does

- Answers questions about John's experience, AI/ML projects, and tech stack
- Powered by OpenAI (`gpt-5-mini` by default)
- Single-page chat UI — no login required
- Anthropic/Claude support stubbed in, ready to enable

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM | OpenAI API |
| Frontend | Vanilla HTML/CSS/JS (single file) |
| Deploy | Railway |
| Domain | resume.etfai.ca |

## Project structure

```
├── app/
│   ├── main.py          # FastAPI app, /api/chat endpoint
│   ├── resume_data.py   # Resume content used as system prompt
│   └── static/
│       └── index.html   # Chat UI
├── requirements.txt
├── Procfile             # Railway start command
└── .env.example
```

## Run locally

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI key
set OPENAI_API_KEY=sk-...     # Windows
# export OPENAI_API_KEY=sk-...  # Mac/Linux

# 4. Start the app
python app/main.py
```

Open `http://localhost:8000`

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | — | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-5-mini` | Model name |
| `PORT` | No | `8000` | Port (set automatically by Railway) |

See [`.env.example`](.env.example) for a template.

## Deploy to Railway

1. Push this repo to GitHub
2. In [Railway](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select this repo
4. Add environment variables (`OPENAI_API_KEY`, `OPENAI_MODEL`) in Railway's **Variables** tab
5. In **Settings → Domains**, add custom domain: `resume.etfai.ca`
6. In your DNS registrar, add a CNAME record:
   ```
   resume  →  <your-app>.railway.app
   ```
Railway auto-provisions the SSL certificate.

## Switch to Anthropic (future)

The Anthropic provider is already stubbed in [`app/main.py`](app/main.py). To enable it:

1. Uncomment the `call_anthropic` function and env var lines in `main.py`
2. Uncomment `anthropic==0.36.2` in `requirements.txt`
3. Set `ANTHROPIC_API_KEY` in Railway variables

---

Built by John Woo · [john.woo.canada@gmail.com](mailto:john.woo.canada@gmail.com)
