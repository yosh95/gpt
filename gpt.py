from openai import OpenAI
from IPython.display import display, Markdown

import requests
from io import BytesIO
from pypdf import PdfReader

import time
import re

GPT35 = "gpt-3.5-turbo-1106"
GPT4 = "gpt-4-1106-preview"

ROLE_0 = ""

ROLE_1 = """
Please keep your answers concise unless instructed otherwise.
To output Latex formulas, enclose them with a $ symbol.
When outputting in Latex format, do not break lines.
"""

ROLE_2 = """
あなたは小学校の先生です。小学生でもわかるように回答してください。漢字にはフリガナを振ってください。
"""

client = OpenAI()

def s(message, model=GPT4):

    start_time = time.time()
    
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ROLE_0,
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        model=model,
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    display(Markdown(completion.choices[0].message.content))
    print(f"(elapsed: {round(elapsed_time, 2)}sec)")

def s3(message):
    s(message, GPT35)

def t():
    s("今日のトリビアを一つお願いします。")

##### process url #####
def name_from_url(url):
    # 'https://' または 'http://' を取り除く
# 'https://' または 'http://' を取り除く
    url = re.sub(r'^https?://', '', url)

    # '.' または '/' を '_' に置換する
    url = re.sub(r'[./]', '_', url)

    # '_pdf'で終わっていたら.pdfに書き換え
    url = re.sub('_pdf$', '.pdf', url)

    return url
    
##### pdf ######
def pdf(url, pages=1, model=GPT4, prompt="下記の文章を日本語で要約してください。"):

    # urlがhttpsでなければローカルファイルと判断
    if url.startswith("http"):
        response = requests.get(url)
        file_name = name_from_url(url)
        open(file_name, "wb").write(response.content)
    else:
        file_name = url

    reader = PdfReader(file_name)
    i = 1
    text = ''
    page_numbers = []
    for page in reader.pages:
        text = text + page.extract_text()
        page_numbers.append(i)
        if len(page_numbers) == pages:
            print(f"--- page({','.join(map(str, page_numbers))}) ---")
            message = f"{prompt}\n\n{text}"
            s(message, model)
            text = ''
            page_numbers = []
        i = i + 1
    print("========== done. ==========")

def pdf3(url, pages=1, model=GPT35):
    pdf(url, pages, model)
