from openai import OpenAI
from IPython.display import display, Markdown

import requests
from io import BytesIO
from pypdf import PdfReader

client = OpenAI()

def send(message):
    
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Please keep your answers concise unless instructed otherwise. To output Latex formulas, enclose them with a $ symbol."
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-4-1106-preview",
    )

    display(Markdown(completion.choices[0].message.content))

def s(message):
    send(message)

def trivia():
    s("今日のトリビアを一つお願いします。")

def t():
    trivia()
    
##### pdf ######
def process_text(text_block):
    # ここに処理を実装します。下記は単にテキストをプリントするだけの例です。
    message = f"下記の文章を日本語で要約してください。\n\n{text_block}"
    send(message)

def summary_pdf(url):
    print(f"Fetching pdf... URL:{url}")
    response = requests.get(url)
    open("fetched.pdf", "wb").write(response.content)
    print("Starts the PDF summarization process.")
    reader = PdfReader("fetched.pdf")
    i = 1
    for page in reader.pages:
        print(f"--- page({i}) ---")
        i = i + 1
        process_text(page.extract_text())
    print("========== done. ==========")

def pdf(url):
    summary_pdf(url)
