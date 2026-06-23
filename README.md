# Free Image & Video Generation with Meta AI SDK

**Give your AI agents the power to generate images and video — completely free.**

This is a free, unofficial integration layer that lets **any AI agent or system** — Claude Code, OpenClaw, Hermes, AutoGPT, CrewAI, LangChain, custom scripts, or literally anything that can make HTTP requests — generate images and videos using Meta AI's Llama 3 model at zero cost. No API keys, no billing, no usage limits. Just a browser cookie from [meta.ai](https://meta.ai).

## Who Is This For?

This project is for anyone who wants to add **free image and video generation** to their AI-powered systems:

- **Claude Code users** — Install the skill and your coding agent can generate images and videos directly in your terminal
- **OpenClaw / Hermes / AGI agents** — Wire up free visual content generation to any agent framework
- **Developers** — Use the Python SDK or HTTP REST server in any application
- **MLOps / AI pipelines** — Integrate free image/video generation into automated workflows
- **Hobbyists** — Because paying for DALL-E or Runway adds up fast

## Features

- **Free Image Generation** — Text-to-image with orientation control (16:9, 9:16, 1:1)
- **Free Video Generation** — Text-to-video with automatic polling for completion
- **Image Analysis (Vision)** — Upload images and ask the AI to describe or analyze them
- **Chat & Reasoning** — Full conversational AI with streaming support
- **Zero Cost** — No API keys, no billing account, no usage caps
- **Universal Integration** — Works with any system: Python, HTTP REST, CLI, or Claude Code skill

## Quick Start

### Option 1: Claude Code Skill (easiest)

```bash
git clone https://github.com/IsuedLeoo/free-image-video-generation-with-meta-ai-sdk.git
cd free-image-video-generation-with-meta-ai-sdk
bash install.sh
```

This will:
- Install Python dependencies
- Copy the skill to `~/.claude/skills/metaai/`
- Create a `.env.metaai` config file
- Open the documentation in your browser

Then edit `~/.claude/skills/metaai/.env.metaai` with your cookies, restart Claude Code, and use `/metaai`.

### Option 2: Python SDK (any project)

```bash
pip install metaai-api
```

```python
from metaai_api import MetaAI

ai = MetaAI()

# Generate an image — free
result = ai.generate_image_new(
    prompt="a cyberpunk city at night, neon lights",
    orientation="LANDSCAPE"
)
print(result["image_urls"])

# Generate a video — free
video = ai.generate_video_new(
    prompt="timelapse of stars moving across the sky"
)
print(video["video_urls"])
```

### Option 3: HTTP REST Server (any language)

```bash
python -m metaai_api.api_server
# → http://localhost:8000
```

```bash
curl -X POST http://localhost:8000/image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset", "orientation": "LANDSCAPE"}'
```

Works with **any** system that can make HTTP requests — Node.js, Go, Rust, Ruby, shell scripts, Home Assistant, n8n, Zapier, etc.

## Getting Your Free Cookies

The only thing you need is a free [meta.ai](https://meta.ai) account. The SDK authenticates using your browser session:

1. Open [https://meta.ai](https://meta.ai) in Chrome and log in (free)
2. Open DevTools: `F12` or `Cmd + Option + I`
3. Go to **Application** → **Cookies** → `https://meta.ai`
4. Copy the values for `datr` and `ecto_1_sess`

That's it. No credit card, no API key registration, no billing setup.

## Documentation

Open `docs/index.html` in your browser for the full developer documentation:
- Complete API reference
- Code examples for every method
- HTTP REST server endpoints
- CLI reference
- Integration patterns

## Repository Structure

```
free-image-video-generation-with-meta-ai-sdk/
├── README.md              # This file
├── install.sh             # One-command installer for Claude Code skill
├── .env.example           # Cookie config template
├── docs/
│   ├── index.html         # Full developer documentation site
│   └── styles.css
└── skill/
    ├── SKILL.md           # Claude Code skill definition
    └── metaai_generate.py # CLI helper script
```

## Integration Examples

### Claude Code

After installing the skill, just ask your agent:
> "Generate an image of a sunset over the ocean"
> "Create a video of waves on a beach"

### Any AI Agent Framework

```python
from metaai_api import MetaAI

ai = MetaAI()

# Use in any agent loop
response = ai.prompt("What do you see in this image?", media_ids=[media_id])
```

### n8n / Zapier / Make

Use the HTTP REST server:
```
POST http://localhost:8000/image
{"prompt": "your image description"}
```

### Custom Agent (any language)

```bash
# Start the server
python -m metaai_api.api_server

# From your agent
curl -X POST http://localhost:8000/chat \
  -d '{"message": "Tell me about this image"}'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `FacebookInvalidCredentialsException` | Refresh `ecto_1_sess` cookie from browser |
| `FacebookRegionBlocked` | Meta AI isn't available in your region |
| Slow generation | Normal — images take 30-120s, videos 20-45s |
| 412 upload errors | Handled automatically with retry |

## Why Free?

Meta AI offers their image and video generation capabilities for free on their web interface. This project simply lets your AI agents use the same capabilities programmatically. You're using your own Meta AI account through your own browser session — there's no third-party proxy or middleware.

## License

MIT License. Not officially affiliated with Meta Platforms, Inc.

## Links

- [Meta AI](https://meta.ai) — The official web interface (free)
- [PyPI Package](https://pypi.org/project/metaai-api/) — `metaai-api` on PyPI
- [Upstream GitHub](https://github.com/mir-ashiq/metaai-api) — Original package by Ashiq Hussain Mir
