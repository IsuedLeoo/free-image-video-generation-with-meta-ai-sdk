---
name: metaai
description: Meta AI SDK — generate images, generate videos, and analyze/describe images using Meta AI (meta.ai). Use when the user wants to create AI images or videos from text prompts, or upload and analyze/describe images.
---

# Meta AI SDK

Unofficial Python SDK (`metaai-sdk`) for Meta AI — image generation, video generation, and image analysis/vision via Meta's Llama 3.

## Authentication

The SDK uses **cookie-based auth** — no API keys needed. Two cookies are required:

- `datr` — device identifier (long-lived)
- `ecto_1_sess` — session token (expires frequently)

### Stored Credentials

Cookies are saved in `.env.metaai` in the project root (`/Users/leongladyshev/Desktop/leadagenciesmiami/.env.metaai`).
Load them with: `dotenv.load_dotenv(".env.metaai")`

### Getting Cookies (if needed)

1. Open https://meta.ai in Chrome and log in
2. F12 → Application tab → Cookies → `https://meta.ai`
3. Copy the `datr` and `ecto_1_sess` values

## Quick Start

```bash
python3 -c "from metaai_api import MetaAI; print('OK')"
```

## Image Generation

```bash
python3 << 'PYEOF'
import json, sys
from metaai_api import MetaAI

ai = MetaAI()  # auto-loads from .env

result = ai.generate_image_new(
    prompt="a beautiful sunset over the ocean",
    orientation="LANDSCAPE",  # LANDSCAPE, VERTICAL, or SQUARE
    num_images=1
)

print(json.dumps(result, indent=2))

if result.get("success"):
    for url in result.get("image_urls", []):
        print(f"Image URL: {url}")
PYEOF
```

## Video Generation

```bash
python3 << 'PYEOF'
import json
from metaai_api import MetaAI

ai = MetaAI()

result = ai.generate_video_new(
    prompt="waves crashing on a beach at sunset",
    auto_poll=True,          # wait for video to be ready
    max_poll_attempts=15,
    poll_wait_seconds=3
)

print(json.dumps(result, indent=2))

if result.get("success"):
    for url in result.get("video_urls", []):
        print(f"Video URL: {url}")
PYEOF
```

## Image Analysis / Vision (Describe Image)

Upload an image and ask Meta AI to describe or analyze it:

```bash
python3 << 'PYEOF'
import json
from metaai_api import MetaAI

ai = MetaAI()

# Step 1: Upload the image
upload = ai.upload_image("/path/to/image.jpg")
print("Upload result:", json.dumps(upload, indent=2))

if upload.get("success"):
    media_id = upload["media_id"]

    # Step 2: Ask about the image
    response = ai.prompt(
        "Describe this image in detail.",
        media_ids=[media_id]
    )
    print("Analysis:", response.get("message", ""))

    # Or ask specific questions
    response2 = ai.prompt(
        "What colors dominate this image? What mood does it convey?",
        media_ids=[media_id]
    )
    print("Answer:", response2.get("message", ""))
PYEOF
```

## Chat (Text Only)

```bash
python3 << 'PYEOF'
from metaai_api import MetaAI

ai = MetaAI()

# Simple chat
response = ai.prompt("What is the capital of France?")
print(response["message"])

# Streaming
for chunk in ai.prompt("Tell me a story", stream=True):
    print(chunk, end="", flush=True)
PYEOF
```

## Direct Cookie Auth (No .env)

```python
from metaai_api import MetaAI

ai = MetaAI(cookies={
    "datr": "your_datr",
    "ecto_1_sess": "your_ecto_1_sess"
})
```

## Orientation Options for Image Generation

| Value | Aspect Ratio |
|---|---|
| `LANDSCAPE` | 16:9 |
| `VERTICAL` | 9:16 |
| `SQUARE` | 1:1 |

## Notes

- Image generation takes ~30-120 seconds; video takes ~20-45 seconds
- Cookies expire — if requests fail, refresh `ecto_1_sess` from the browser
- The SDK auto-detects and handles Meta's bot detection challenge pages
- Not officially affiliated with Meta Platforms, Inc.
- **✅ Fixed (Jun 21, 2026):** Meta migrated from HTTP POST mutations to DGW WebSocket subscriptions for image/video generation. Updated the `doc_id` to `16b03ab6b0bdd48bbbfc0ea46f42ca4f` (`useEctoSendMessageSubscription`) which works over HTTP POST with proper UUID conversation IDs. Removed deprecated GraphQL fields (`rewriteOptions`, `clippyIp`, etc.) that caused `GRAPHQL_VALIDATION_FAILED` errors. Image generation confirmed working.
