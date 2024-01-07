from openai import OpenAI
from IPython.display import display, Markdown
import requests
from io import BytesIO
from pypdf import PdfReader
import time
import re

# 使用するモデルの定義
GPT35 = "gpt-3.5-turbo-1106"
GPT4 = "gpt-4-1106-preview"

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
    return url

# PDFファイルの処理
def pdf(url, pages=1, prompt="下記の文章を日本語で要約してください。", model=GPT4):
    if url.startswith("http"):
        try:
            response = requests.get(url)
            response.raise_for_status()
            file_name = name_from_url(url)
            with open(file_name, "wb") as file:
                file.write(response.content)
        except requests.RequestException as e:
            print(f"Error: {e}")
            return
    else:
        file_name = url

    try:
        reader = PdfReader(file_name)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return

    page_numbers = []
    text = ''
    for i, page in enumerate(reader.pages, 1):
        text += page.extract_text()
        page_numbers.append(i)
        if len(page_numbers) == pages:
            message = f"{prompt}\n\n{text}"
            s(message, model)
            text = ''
            page_numbers = []

    print("PDF processing completed.")

def pdf3(url, pages=1, prompt="下記の文章を日本語で要約してください。"):
    pdf(url, pages, prompt, GPT35)
