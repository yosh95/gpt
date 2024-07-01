#!/usr/bin/env python3

import chat
import json
import os
import requests

MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
API_KEY = os.getenv("GEMINI_API_KEY", "")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/" \
           + MODEL + ":generateContent?key=" + API_KEY
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", None)


class Gemini(chat.Chat):

    def _send(self, message, conversation, use_history):

        if conversation is None:
            messages = []
        elif use_history is True:
            messages = list(conversation)
        else:
            messages = []

        message = message.strip()
        user_message = {"role": "user", "parts": [{"text": message}]}
        messages.append(user_message)

        content = ''
        try:
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                'contents': messages
            }
            if SYSTEM_PROMPT is not None:
                data['system_instruction'] = {
                    'parts': [{
                        'text': SYSTEM_PROMPT
                    }]
                }

            response = requests.post(API_URL,
                                     headers=headers,
                                     data=json.dumps(data))

            self.write_request_debug_log(headers, data, response)

            response.raise_for_status()

            result = response.json()

            content = result['candidates'][0]['content']['parts'][0]['text']
            content = content.rstrip(" \n")
            if content.startswith("'content'"):  # for debug
                print(content) # for debug
            model_message = {"role": "model", "parts": [{"text": content}]}

            print(f"({MODEL}): ", end="")

            print(content, end="")

            usage = result['usageMetadata']

            if conversation is not None:
                conversation.append(user_message)
                conversation.append(model_message)

        except Exception as e:
            print(e)
            return None, None
        return content, usage

    def _send_image(self, message, mime_type, base64_image):

        messages = []

        messages.append({
            "parts": [
                {
                    "text": message
                },
                {
                    "inlineData": {
                        "mimeType": mime_type,
                        "data": base64_image
                    }
                }
            ]
        })

        try:
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                'contents': messages
            }

            content = ''

            response = requests.post(API_URL,
                                     headers=headers,
                                     data=json.dumps(data))

            self.write_request_debug_log(headers, data, response)

            response.raise_for_status()

            result = response.json()

            content = result['candidates'][0]['content']['parts'][0]['text']
            content = content.rstrip(" \n")

            print(f"({MODEL}): ", end="")

            print(content, end="")

        except Exception as e:
            print(e)
            return None, None
        return content, None


# CLI Interface
if __name__ == "__main__":
    gemini = Gemini(MODEL)
    gemini.main()
