from IPython.display import display, Markdown
from bs4 import BeautifulSoup
from io import BytesIO
from openai import OpenAI
from pypdf import PdfReader

import os
import re
import requests
import time

### Model
MODEL = "gpt-4-1106-preview"

### Create download directory if not exists
DOWNLOAD_DIR = "./download/"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

### System Prompt
SYSTEM_PROMPT = """
Please keep your answers concise unless instructed otherwise.
To output Latex formulas, enclose them with a $ symbol.
When outputting in Latex format, do not break lines.
"""

### conversation
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

### Main
client = OpenAI()

def send(message):
    start_time = time.time()

    conversation.append(
        {"role": "user", "content": message.strip()}
    )

    completion = client.chat.completions.create(
        messages=conversation,
        model=MODEL,
    )

    end_time = time.time()
    display(Markdown(completion.choices[0].message.content))
    print(f"(Elapsed Time: {round(end_time - start_time, 2)} sec)")

    conversation.append(
        {"role": "assistant", "content": completion.choices[0].message.content}
    )

def trivia():
    send("今日のトリビアを一つお願いします。")

### talk
def talk():
    while True:
        print("==========")
        user_input = input("Prompt('q' to quit): ")
        print("-----")
        if user_input.lower() == 'q':
            break
        send(user_input)

    print("Bye.")

### Create a file name from URL
def name_from_url(url):
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'[./]', '_', url)
    url = re.sub('_pdf$', '.pdf', url)
    url = re.sub('_html$', '.html', url)
    return DOWNLOAD_DIR + url

### fetch
def fetch(url):
    if url.startswith("http"):
        try:
            response = requests.get(url)
            response.raise_for_status()
            file_name = name_from_url(url)
            with open(file_name, "wb") as file:
                file.write(response.content)
            return file_name
        except requests.RequestException as e:
            print(f"Error: {e}")
            return
    else:
        file_name = url

### Processing the PDF file
def pdf(url, prompt="下記の文章を日本語で要約してください。"):
    file_name = fetch(url)
    if file_name == '':
        return

    try:
        reader = PdfReader(file_name)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return

    text = ''
    for page in reader.pages:
        text += page.extract_text()

    message = f"{prompt}\n\n{text}"
    send(message)

### Processing the HTML file
def html(url, prompt="下記の文章を日本語で要約してください。"):
    file_name = fetch(url)
    if file_name == '':
        return

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            html_doc = file.read()
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return

    soup = BeautifulSoup(html_doc, 'lxml')

    text = soup.get_text()
    text = re.sub(r'\n\s*\n', '\n', text)

    message = f"{prompt}\n\n{text}"
    send(message, model)
