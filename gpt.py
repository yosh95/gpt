#!/usr/bin/env python3

import chat
import json
import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY", "")
API_URL = 'https://api.openai.com/v1/chat/completions'
MODEL = os.getenv("GPT_MODEL", "gpt-4o")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", None)


class GPT(chat.Chat):

    def _send(self, message, conversation, use_history):

        if conversation is None:
            messages = []
        elif use_history is True:
            messages = list(conversation)
        else:
            messages = []

        if SYSTEM_PROMPT is not None:
            system_message = {"role": "system", "content": SYSTEM_PROMPT}
            messages.append(system_message)

        message = message.strip()
        user_message = {"role": "user", "content": message}
        messages.append(user_message)

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}',
            }

            data = {
                'model': MODEL,
                'messages': messages,
            }

            content = ''

            response = requests.post(API_URL,
                                     headers=headers,
                                     data=json.dumps(data))
            response.raise_for_status()

            result = response.json()

            print(f"({MODEL}): ", end="")

            content = result['choices'][0]['message']['content']
            print(content, end="")

            usage = result['usage']

            model_message = {"role": "assistant", "content": content}
            if conversation is not None:
                conversation.append(user_message)
                conversation.append(model_message)

        except Exception as e:
            print(e)
            return None, None
        return content, usage

    def _send_image(self, message, mime_type, base64_image):

        messages = []

        if SYSTEM_PROMPT is not None:
            messages.append({"role": "system", "content": SYSTEM_PROMPT})

        image_url = f"data:{mime_type};base64,{base64_image}"

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": message
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        })

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}',
            }

            data = {
                'model': MODEL,
                'messages': messages,
            }

            content = ''

            response = requests.post(API_URL,
                                     headers=headers,
                                     data=json.dumps(data))
            response.raise_for_status()

            result = response.json()

            print(f"({MODEL}): ", end="")

            content = result['choices'][0]['message']['content']
            print(content, end="")

            usage = result['usage']

        except Exception as e:
            print(e)
            return None, None
        return content, usage


if __name__ == "__main__":
    gpt = GPT(MODEL)
    gpt.main()
