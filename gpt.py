#!/usr/bin/env python3

import argparse
import filetype
import json
import openai
import os
import re
import requests
import webbrowser

from bs4 import BeautifulSoup
from collections import deque
from dotenv import load_dotenv
from io import BytesIO
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import prompt
from pypdf import PdfReader

# Read .env
load_dotenv()

# Constants
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", 10000))
MODEL = os.getenv("GPT_MODEL", "gpt-4o")
DEFAULT_PROMPT = os.getenv("DEFAULT_PROMPT", None)
DEFAULT_TIMEOUT_SEC = 30
INPUT_HISTORY = os.getenv(
        "PROMPT_HISTORY",
        f"{os.path.expanduser('~')}/.prompt_history")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", None)
USER_AGENT = os.getenv("USER_AGENT", "LLM_Chat_Tool")

# OpenAI
api_key = os.getenv("OPENAI_API_KEY", "")
openai_client = openai.OpenAI(api_key=api_key)

# prompt_toolkit
kb = KeyBindings()


@kb.add('escape', 'enter')
def _(event):
    event.current_buffer.insert_text('\n')


@kb.add('c-delete')
def _(event):
    event.app.exit(exception=EOFError)


@kb.add('escape')
def _(event):
    event.app.exit(exception=EOFError)


@kb.add('escape', 'backspace')
def _(event):
    event.app.exit(exception=EOFError)


@kb.add('f9')
def _(event):
    event.app.exit(exception=EOFError)


@kb.add('f10')
def _(event):
    event.current_buffer.validate_and_handle()


def _send(message, conversation):

    if conversation is None:
        messages = []
    else:
        messages = list(conversation)

    if SYSTEM_PROMPT is not None:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

    message = message.strip()
    messages.append({"role": "user", "content": message})

    all_content = ''
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            timeout=DEFAULT_TIMEOUT_SEC
        )

        print(f"({MODEL}): ", end="")

        for chunk in response:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message:
                all_content += chunk_message
                print(chunk_message, end="", flush=True)

    except Exception as e:
        print(e)
    return all_content


def read_pdf(byte_stream):

    reader = PdfReader(byte_stream)
    text = ''
    for page in reader.pages:
        text += '\n' + page.extract_text()
    return text


def fetch_url_content(url):
    headers = {}
    headers['User-Agent'] = USER_AGENT
    try:
        response = requests.get(url,
                                headers=headers,
                                timeout=DEFAULT_TIMEOUT_SEC)
        response.raise_for_status()
    except Exception as e:
        print(e)
        return

    content_type = response.headers['Content-Type']

    content = response.content

    if 'application/pdf' in content_type:
        return read_pdf(BytesIO(content))
    elif 'text/html' in content_type:
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text(' ', strip=True)
    elif 'text/plain' in content_type:
        return content.decode('utf-8')
    else:
        print(f"Unavailable content type: {content_type}")
        return None


# Processing Functions
def talk(text, read_all=False, url=None):

    buf = text
    if read_all is True:
        chunk_size = len(text)
    else:
        chunk_size = DEFAULT_CHUNK_SIZE
    prmt = DEFAULT_PROMPT

    prompt_history = FileHistory(INPUT_HISTORY)
    conversation = deque()

    processed = 0

    while True:

        if len(text) > 0:
            pct = processed / len(text) * 100
            print(f"({processed:,}/{len(text):,})({pct:.2f}%)")

        try:
            user_input = prompt('> ',
                                history=prompt_history,
                                key_bindings=kb,
                                enable_suspend=True)
            user_input = user_input.strip()
        except UnicodeDecodeError as e:
            print(e)
            continue
        except KeyboardInterrupt:
            break
        except EOFError:
            break

        # special commands
        if user_input in ['.q', '.quit']:
            break
        if user_input in ['.i', '.info']:
            print(f"Model: {MODEL}")
            print(f"Chunk size: {chunk_size}")
            print(f"Default prompt: {prmt}")
            print(f"System prompt: {SYSTEM_PROMPT}")
            print(f"History size: {len(conversation)}")
            print(f"Reading URL: {url}")
            print(f"User Agent: {USER_AGENT}")
            continue
        if user_input in ['.h', '.history']:
            print(json.dumps(list(conversation), indent=2, ensure_ascii=False))
            continue
        if user_input == '.clear':
            conversation.clear()
            continue
        if user_input in ['.g', '.goto']:
            buf = text
            print("Going to the first.")
            processed = 0
            continue
        pattern = r'^\.(goto|g) (\d+)$'
        match = re.search(pattern, user_input)
        if match:
            pos = int(match.group(2))
            if pos < 0:
                pos = 0
            buf = text[pos:]
            print(f"Going to {pos}")
            processed = pos
            continue
        pattern = r'^\.(chunk|c)(=|\s)(\d+)$'
        match = re.search(pattern, user_input)
        if match:
            chunk_size = int(match.group(3))
            if chunk_size < 1:
                chunk_size = 1
            print(f"chunk_size has been set to {chunk_size}")
            continue
        pattern = r'^\.(prompt|p)(=|\s)(.+)$'
        match = re.search(pattern, user_input, re.DOTALL)
        if match:
            new_prompt = match.group(3)
            if new_prompt != "":
                print(f"PREVIOUS default prompt: {prmt}")
                print(f"NEW default prompt: {new_prompt}")
                prmt = new_prompt
            continue
        if user_input in ['.o', '.open']:
            if url is None:
                print("No url to open.")
            else:
                webbrowser.open(url)
            continue

        if user_input == '':
            if len(buf) > 0:
                chunk = buf[:chunk_size]
                buf = buf[len(chunk):]
                message = chunk
                if prmt is not None:
                    message += "\n\n" + prmt
                response = _send(message, None)
                conversation.append(
                        {"role": "user",
                         "content": message})
                conversation.append(
                        {"role": "assistant",
                         "content": response})
                processed += chunk_size
                if processed >= len(text):
                    processed = len(text)
            else:
                continue
        else:
            response = _send(user_input, conversation)
            conversation.append(
                    {"role": "user",
                     "content": user_input})
            conversation.append(
                    {"role": "assistant",
                     "content": response})
        print()


def process_pdf(file_name, read_all):
    with open(file_name, "rb") as fh:
        text = read_pdf(BytesIO(fh.read()))

    if text != '':
        talk(text, read_all)
    else:
        print("Empty PDF.")


def process_text(file_name, read_all):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
        if text != '':
            talk(text, read_all)


def read_and_process(source, read_all):
    if source.startswith("http"):
        text = fetch_url_content(source)
        if text is not None and text != '':
            talk(text, read_all, url=source)
        else:
            print("Failed to read.")
            return False
        return True

    if os.path.exists(source):
        kind = filetype.guess(source)
        if kind and kind.extension == 'pdf':
            process_pdf(source, read_all)
        else:
            process_text(source, read_all)
    else:
        _send(source, None)
        print()

    return True


# CLI Interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This LLM utility offers versatile "
                    + "options for generating text with GPT."
                    + "You can provide a source as either a URL, "
                    + "a file path, or directly as a prompt.")

    parser.add_argument('source',
                        nargs='?',
                        help="Specify the source for the prompt. "
                             + "Can be a URL, a file path, "
                             + "or a direct prompt text.")
    parser.add_argument('-a',
                        '--all',
                        action='store_true',
                        help="This option overrides the default chunk size. "
                             + "LLM uses the entire text data.")
    parser.add_argument('-p',
                        '--prompt',
                        help="Specify a prompt that overrides "
                             + "the default prompt applied to "
                             + "external data. This is effective "
                             + "when processing and loading external data.")
    args = parser.parse_args()

    if args.prompt is not None:
        DEFAULT_PROMPT = args.prompt

    if args.source is None:
        talk("")
    else:
        read_and_process(args.source, args.all)
