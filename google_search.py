import argparse
import gpt
import os
import requests
import urllib.parse

from dotenv import load_dotenv
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.bindings.focus \
        import focus_next, focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings \
        import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.shortcuts import dialogs, prompt
from prompt_toolkit.widgets import Button, Dialog, Label, RadioList

load_dotenv()

USER_AGENT = os.getenv("GPT_USER_AGENT", None)
API_KEY = os.getenv("GOOGLE_API_KEY", None)
CSE_ID = os.getenv("GOOGLE_CSE_ID", None)


def select_list(title, explanation, items, default):

    if items is None:
        items = []

    radio_list = RadioList(values=items, default=default)

    def ok_handler() -> None:
        get_app().exit(result=radio_list.current_value)

    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text=explanation), radio_list],
            padding=1,
        ),
        buttons=[
            Button(text="OK", handler=ok_handler),
            Button(text="Cancel", handler=dialogs._return_none),
        ],
        with_background=True,
    )

    bindings = KeyBindings()
    bindings.add("right")(focus_next)
    bindings.add("left")(focus_previous)
    bindings.add("c-d")(lambda event: event.app.exit())
    bindings.add("c-z")(lambda event: event.app.suspend_to_background())
    bindings.add("c-delete")(lambda event: event.app.exit())
    bindings.add("escape")(lambda event: event.app.exit())

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=None,
        full_screen=True,
    ).run()


def search(search_term):

    print("Query: " + search_term)
    param = {
        "q": search_term
    }
    encoded = urllib.parse.urlencode(param)

    base_url = "https://www.googleapis.com/customsearch/v1?" \
        + f"key={API_KEY}&cx={CSE_ID}&{encoded}"

    headers = {}
    if USER_AGENT is not None:
        headers['User-Agent'] = USER_AGENT

    startIndex = 0

    while True:

        url = base_url + f"&start={startIndex}"
        response = requests.get(url, headers=headers)

        search_results = {}
        if response.status_code == 200:
            response.encoding = 'utf-8'
            search_results = response.json()
        else:
            print(f"Failed to retrieve the web page: {response.status_code}")
            return False

        if 'items' not in search_results:
            print("No results.")
            return False

        links = []

        for item in search_results['items']:
            links.append((item['link'], item['title']))

        prevIndex = -1
        nextIndex = -1

        if 'queries' in search_results:
            if 'previousPage' in search_results['queries']:
                prevIndex =\
                    search_results['queries']['previousPage'][0]['startIndex']
                links.append(('Previous', 'Previous'))
            if 'nextPage' in search_results['queries']:
                nextIndex =\
                    search_results['queries']['nextPage'][0]['startIndex']
                links.append(('Next', 'Next'))

        result = None

        while True:

            result = select_list(
                    'Search Results',
                    'Please select one search result from the following:',
                    links, result)

            if result is None:
                return True

            if result == 'Previous':
                startIndex = prevIndex
                break

            if result == 'Next':
                startIndex = nextIndex
                break

            print(f"URL: {result}")
            if gpt.read_and_process(result) is False:
                prompt("Press the enter key to continue. ")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description="Web search utility")

    parser.add_argument('query',
                        nargs='*',
                        help="Specify query keywords.")

    args = parser.parse_args()

    if len(args.query) == 0:
        print('Query string is not specified.')
    else:
        search(' '.join(args.query))
