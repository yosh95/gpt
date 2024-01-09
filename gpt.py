from IPython.display import display, Markdown
from bs4 import BeautifulSoup
from io import BytesIO
from openai import OpenAI
from pypdf import PdfReader

import os
import re
import requests
import time

# 使用するモデルの定義
GPT35 = "gpt-3.5-turbo-1106"
GPT4 = "gpt-4-1106-preview"

# downloadディレクトリの作成
DOWNLOAD_DIR = "./download/"
if not os.path.exists(DOWNLOAD_DIR):
    # 存在しない場合、ディレクトリを作成
    os.makedirs(DOWNLOAD_DIR)

# ROLE定数
#ROLE_0 = ""

ROLE_1 = """
Please keep your answers concise unless instructed otherwise.
To output Latex formulas, enclose them with a $ symbol.
When outputting in Latex format, do not break lines.
"""

#ROLE_2 = """
#あなたは小学校の先生です。小学生でもわかるように回答してください。漢字にはフリガナを振ってください。
#"""

client = OpenAI()

def s(message, model=GPT4, role=ROLE_1):
    start_time = time.time()

    message = message.strip()
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": message},
        ],
        model=model,
    )

    end_time = time.time()
    display(Markdown(completion.choices[0].message.content))
    print(f"(Elapsed Time: {round(end_time - start_time, 2)} sec)")

def s3(message):
    s(message, GPT35)

def t():
    s("今日のトリビアを一つお願いします。", role=ROLE_1)

# URLから適切なファイル名を生成
def name_from_url(url):
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'[./]', '_', url)
    url = re.sub('_pdf$', '.pdf', url)
    url = re.sub('_html$', '.html', url)
    return DOWNLOAD_DIR + url

# fetch
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

# PDFファイルの処理
def pdf(url, pages=1, prompt="下記の文章を日本語で要約してください。", model=GPT4):
    file_name = fetch(url)
    if file_name == '':
        return

    try:
        reader = PdfReader(file_name)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return

    num_of_pages = len(reader.pages)
    page_numbers = []
    text = ''
    for i, page in enumerate(reader.pages, 1):
        text += page.extract_text()
        page_numbers.append(i)
        if (len(page_numbers) == pages) or (i == num_of_pages):
            print(f"pages={page_numbers}")
            message = f"{prompt}\n\n{text}"
            s(message, model)
            text = ''
            page_numbers = []

    print("PDF processing completed.")

def pdf3(url, pages=1, prompt="下記の文章を日本語で要約してください。"):
    pdf(url, pages, prompt, GPT35)

# HTMLページの処理
def html(url, prompt="下記の文章を日本語で要約してください。", model=GPT4):
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
    s(message, model)

def html3(url, prompt="下記の文章を日本語で要約してください。"):
    html(url, prompt, GPT35)
