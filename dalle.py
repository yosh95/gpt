#!/usr/bin/env python3

import argparse
import json
import os
import requests

from dotenv import load_dotenv

# Read .env
load_dotenv()

# Constants
API_URL = 'https://api.openai.com/v1/images/generations'
MODEL = os.getenv("IMAGE_MODEL", "dall-e-3")
IMAGE_SIZE = "1024x1024"

# OpenAI
API_KEY = os.getenv("OPENAI_API_KEY", "")


def _send(message):

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
        }

        data = {
            'model': MODEL,
            'prompt': message,
            'size': IMAGE_SIZE
        }

        response = requests.post(API_URL,
                                 headers=headers,
                                 data=json.dumps(data))
        response.raise_for_status()

        result = response.json()

        print(f"({MODEL}): ", end="")

        print(result['data'][0]['revised_prompt'])
        print("")
        print(result['data'][0]['url'])

    except Exception as e:
        print(e)


# CLI Interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Image generation utility.")

    parser.add_argument('source',
                        help="Specify prompt for the image generation.")
    args = parser.parse_args()

    _send(args.source)
