#!/usr/bin/env python3
"""Meta AI CLI helper — generate images, videos, or analyze images."""

import argparse
import json
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Meta AI SDK CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Image generation
    img_parser = subparsers.add_parser("image", help="Generate images from text")
    img_parser.add_argument("prompt", help="Image prompt")
    img_parser.add_argument("--orientation", default="LANDSCAPE",
                           choices=["LANDSCAPE", "VERTICAL", "SQUARE"])
    img_parser.add_argument("--num", type=int, default=1, help="Number of images (max 4)")

    # Video generation
    vid_parser = subparsers.add_parser("video", help="Generate videos from text")
    vid_parser.add_argument("prompt", help="Video prompt")
    vid_parser.add_argument("--no-poll", action="store_true",
                           help="Don't wait for video to be ready")

    # Image analysis
    analyze_parser = subparsers.add_parser("analyze", help="Analyze/describe an image")
    analyze_parser.add_argument("image_path", help="Path to image file")
    analyze_parser.add_argument("--question", default="Describe this image in detail.",
                               help="Question to ask about the image")

    # Chat
    chat_parser = subparsers.add_parser("chat", help="Chat with Meta AI")
    chat_parser.add_argument("message", help="Message to send")

    # Cookie check
    subparsers.add_parser("check", help="Check if cookies are configured")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Lazy import
    try:
        from metaai_api import MetaAI
    except ImportError:
        print("ERROR: metaai-sdk not installed. Run: python3 -m pip install metaai-sdk", file=sys.stderr)
        sys.exit(1)

    if args.command == "check":
        # Try loading from .env.metaai first, then .env
        try:
            from dotenv import load_dotenv
            env_paths = [".env.metaai", ".env"]
            for p in env_paths:
                if os.path.exists(p):
                    load_dotenv(p)
                    break
        except ImportError:
            pass
        datr = os.environ.get("META_AI_DATR", "")
        sess = os.environ.get("META_AI_ECTO_1_SESS", "")
        if datr and sess:
            print("OK: Meta AI cookies are configured")
        else:
            print("ERROR: Meta AI cookies not configured.", file=sys.stderr)
            print("Set META_AI_DATR and META_AI_ECTO_1_SESS environment variables", file=sys.stderr)
            print("or create a .env file with those values.", file=sys.stderr)
            sys.exit(1)
        return

    # Load env
    try:
        from dotenv import load_dotenv
        for p in [".env.metaai", ".env"]:
            if os.path.exists(p):
                load_dotenv(p)
                break
    except ImportError:
        pass

    # Initialize SDK
    try:
        ai = MetaAI()
    except Exception as e:
        print(f"ERROR: Failed to initialize Meta AI SDK: {e}", file=sys.stderr)
        print("Make sure META_AI_DATR and META_AI_ECTO_1_SESS are set.", file=sys.stderr)
        sys.exit(1)

    if args.command == "image":
        print(f"Generating image: {args.prompt}...", file=sys.stderr)
        result = ai.generate_image_new(
            prompt=args.prompt,
            orientation=args.orientation,
            num_images=args.num
        )
        print(json.dumps(result, indent=2))
        if result.get("success"):
            for url in result.get("image_urls", []):
                print(f"\nImage URL: {url}")

    elif args.command == "video":
        print(f"Generating video: {args.prompt}...", file=sys.stderr)
        result = ai.generate_video_new(
            prompt=args.prompt,
            auto_poll=not args.no_poll
        )
        print(json.dumps(result, indent=2))
        if result.get("success"):
            for url in result.get("video_urls", []):
                print(f"\nVideo URL: {url}")

    elif args.command == "analyze":
        if not os.path.exists(args.image_path):
            print(f"ERROR: File not found: {args.image_path}", file=sys.stderr)
            sys.exit(1)
        print(f"Uploading image: {args.image_path}...", file=sys.stderr)
        upload = ai.upload_image(args.image_path)
        if not upload.get("success"):
            print(f"ERROR: Upload failed: {upload}", file=sys.stderr)
            sys.exit(1)
        media_id = upload["media_id"]
        print(f"Uploaded (media_id: {media_id}). Analyzing...", file=sys.stderr)
        response = ai.prompt(args.question, media_ids=[media_id])
        print(response.get("message", ""))

    elif args.command == "chat":
        response = ai.prompt(args.message)
        print(response.get("message", ""))

if __name__ == "__main__":
    main()
