# Meta AI SDK for Claude Code

Unofficial skill plugin for Claude Code that adds Meta AI capabilities — image generation, video generation, image analysis, and chat — powered by Meta's Llama 3 model.

## Features

- **Image Generation** — Create images from text prompts with orientation control (16:9, 9:16, 1:1)
- **Video Generation** — Generate short video clips with automatic polling for completion
- **Image Analysis** — Upload images and ask Meta AI to describe or analyze them
- **Chat & Reasoning** — Full conversational AI with streaming support
- **No API Keys** — Authenticates using browser cookies from [meta.ai](https://meta.ai)

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/IsuedLeoo/metaai-sdk.git
cd metaai-sdk
bash install.sh
```

This will:
- Install Python dependencies (`metaai-api`, `requests`, `python-dotenv`)
- Copy skill files to `~/.claude/skills/metaai/`
- Create a `.env.metaai` config file
- Open the documentation in your browser

### 2. Configure your cookies

Edit `~/.claude/skills/metaai/.env.metaai` and fill in your cookie values:

1. Open [https://meta.ai](https://meta.ai) in Chrome and log in
2. Open DevTools (`F12` or `Cmd + Option + I`)
3. Go to **Application** → **Cookies** → `https://meta.ai`
4. Copy the values for `datr` and `ecto_1_sess` into your `.env.metaai`

### 3. Restart Claude Code

The skill will be available as `/metaai` in your next session.

## Manual Installation

If you prefer to set things up manually:

```bash
# Install Python package
pip install metaai-api

# Install skill files
mkdir -p ~/.claude/skills/metaai
cp skill/SKILL.md ~/.claude/skills/metaai/
cp skill/metaai_generate.py ~/.claude/skills/metaai/

# Configure
cp .env.example ~/.claude/skills/metaai/.env.metaai
# Edit ~/.claude/skills/metaai/.env.metaai with your cookies
```

## Documentation

Open `docs/index.html` in your browser for the full developer documentation with:
- API reference
- Code examples for every method
- HTTP REST server setup
- CLI reference

## Repository Structure

```
metaai-sdk/
├── README.md              # This file
├── install.sh             # Automated installer
├── .env.example           # Cookie config template
├── docs/
│   ├── index.html         # Full developer documentation
│   └── styles.css
└── skill/
    ├── SKILL.md           # Claude Code skill definition
    └── metaai_generate.py # CLI helper script
```

## Usage Examples

### Python

```python
from metaai_api import MetaAI

ai = MetaAI()

# Generate an image
result = ai.generate_image_new(
    prompt="a beautiful sunset over mountains",
    orientation="LANDSCAPE"
)
print(result["image_urls"])

# Chat with the AI
response = ai.prompt("Explain quantum computing simply")
print(response["message"])
```

### CLI

```bash
# Generate an image
python skill/metaai_generate.py image "a beautiful sunset"

# Chat
python skill/metaai_generate.py chat "Tell me a joke"

# Analyze an image
python skill/metaai_generate.py analyze photo.jpg
```

## HTTP REST Server

The underlying `metaai_api` package includes a FastAPI server:

```bash
python -m metaai_api.api_server
# → http://localhost:8000
```

Endpoints: `/chat`, `/image`, `/video`, `/video/async`, `/upload`, `/healthz`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `FacebookInvalidCredentialsException` | Refresh `ecto_1_sess` cookie from browser |
| `FacebookRegionBlocked` | Meta AI isn't available in your region |
| Slow generation | Normal — images take 30-120s, videos 20-45s |
| 412 upload errors | Handled automatically with retry |

## License

MIT License. Not officially affiliated with Meta Platforms, Inc.

## Links

- [Meta AI](https://meta.ai) — The official web interface
- [PyPI Package](https://pypi.org/project/metaai-api/) — `metaai-api` on PyPI
- [Upstream GitHub](https://github.com/mir-ashiq/metaai-api) — Original package by Ashiq Hussain Mir
