# gpt.py - A Versatile GPT Utility

This Python program (`gpt.py`) provides a flexible and interactive way to utilize the power of OpenAI's GPT models for various text generation and processing tasks. 

## Features

- **Multiple Input Sources:** Interact with GPT by providing input from various sources:
    - **Direct Input:** Type your prompt directly in the interactive console.
    - **File Input:** Load and process text from local files (supports both `.txt` and `.pdf`).
    - **URL Input:** Fetch and analyze content from websites (handles both HTML and PDF content).
- **Interactive Console:** Enjoy a user-friendly console experience with:
    - **History:**  Access previous prompts and responses for context.
    - **Special Commands:**  Use commands to control the session, view information, adjust settings, and more (see below for a list of commands). 
- **Chunking:** Process large texts effectively by breaking them into smaller chunks and feeding them to GPT incrementally. You can customize the chunk size for optimal results.
- **Prompt Engineering:**
    - **Default Prompt:** Set a default prompt that is appended to each chunk of text for consistent guidance to the model.
    - **Custom Prompts:**  Override the default prompt for specific interactions.
- **System Prompts:** Provide high-level instructions to guide the overall behavior of GPT during the session. 
- **OpenAI API Integration:**  Seamlessly connects to the OpenAI API using your API key (stored in a `.env` file).
- **Web Browsing:**  Quickly open URLs mentioned in the conversation. 

## Installation and Setup

1. **Dependencies:** Install the necessary Python packages.
   ```bash
   pip install -r requirements.txt 
   ```
2. **OpenAI API Key:**
   - Create an account at [https://beta.openai.com/](https://beta.openai.com/) and obtain an API key.
   - Create a `.env` file in the same directory as `gpt.py` and add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here 
     ```
3. **Environment Variables (Optional):**  Customize the tool's behavior further by setting the following environment variables in your `.env` file:
    - `DEFAULT_CHUNK_SIZE`:  Adjust the default chunk size for processing large texts (default: 10000 characters).
    - `DEFAULT_MODEL`: Choose the desired GPT model (default: `gpt-4`).
    - `DEFAULT_PROMPT`:  Specify a default prompt for external data.
    - `PROMPT_HISTORY`:  Set the path for storing prompt history (default: `~/.prompt_history`).
    - `SYSTEM_PROMPT`: Provide a system-level prompt.
    - `USER_AGENT`: Set a custom user agent for web requests (default: `GPT_Tool`).

## Usage

Run `gpt.py` from your terminal. You can provide an optional source argument:

```bash
python gpt.py [source]
```

- **[source]:** (Optional) Can be:
    - A URL (e.g., `https://www.example.com/article.pdf`).
    - A file path (e.g., `my_document.txt`, `report.pdf`).
    - Omitted for direct interaction.

## Special Commands

Use the following commands within the interactive console: 

| Command              | Description                                         |
|----------------------|-----------------------------------------------------|
| `.q`, `.quit`        | Exit the program.                                    |
| `.i`, `.info`        | Display current settings and information.            |
| `.raw`              | Show the last raw user input.                    |
| `.hist`, `.history` | Print the conversation history (JSON format).        |
| `.pop`               | Remove and display the oldest entry from the history. |
| `.clear`            | Clear the conversation history.                       |
| `.reset`            | Reset all settings to their defaults.               |
| `.g`, `.goto`       | Go back to the beginning of the text.               |
| `.goto [position]`  | Jump to a specific position in the text.             |
| `.chunk [size]`    | Set a new chunk size for text processing.            |
| `.prompt [prompt]`  | Change the default prompt.                       |
| `.o`, `.open`       | Open the current URL (if available).                 |
| `.open [URL]`        | Open a specific URL in a web browser.                |
| `.read [source]`   | Load and process content from a new source.         |
| `.search [query]`   | Perform a Google search.                             |

## Examples

- **Direct Interaction:**
  ```bash
  python gpt.py 
  > What are the benefits of using GPT-3?
  ```

- **Process a Local File:**
  ```bash
  python gpt.py my_document.txt 
  > Summarize the key points from this text. 
  ```

- **Analyze a Website:**
  ```bash
  python gpt.py https://en.wikipedia.org/wiki/Artificial_intelligence
  > What are the different types of AI?
  ```

## Notes

- This program requires an active internet connection to communicate with the OpenAI API.
- Ensure that you have a valid OpenAI API key and have set it up correctly in the `.env` file.

This README provides a comprehensive overview of `gpt.py`, its features, and how to use it effectively.


# google_search.py

## Description

This is a Python command-line tool that enables you to perform a Google search and subsequently analyze the content of returned web pages using GPT-3.

## Features

* **Google Search Integration:** Directly queries the Google Custom Search JSON API using provided API key and CSE ID.
* **Interactive Result Selection:** Presents a user-friendly interface for choosing from a paginated list of search results.
* **GPT-3 Content Analysis (Optional):** Integrates with a separate `gpt` module (not included in this script) to analyze the content of selected web pages.

## Prerequisites

1. **Python 3.7 or later**
2. **Required Python Packages:**
   - `argparse`
   - `prompt_toolkit`
   - `requests`
   - `python-dotenv`
3. **API Keys and Setup:**
   - **Google Custom Search Engine ID (CSE ID):**  Create a custom search engine and obtain its ID from the Google Cloud Console.
   - **Google API Key:** Obtain an API key with access to the Custom Search JSON API.
   - **OpenAI API Key (Optional):** Required only if using the GPT-3 content analysis feature.
4. **Environment Variables:** Store API keys securely using environment variables or a `.env` file. This script expects the following:
   - `GOOGLE_API_KEY`
   - `GOOGLE_CSE_ID`
   - `USER_AGENT` (Optional, for customizing HTTP requests)

## Installation

1. **Install Python packages:**
   ```bash
   pip install argparse prompt_toolkit requests python-dotenv 
   ```

2. **Create a `.env` file in the same directory as the script and add your API keys:**
   ```
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_google_cse_id
   USER_AGENT=your_custom_user_agent (optional)
   ```

## Usage

1. **Save the script as `google_search.py`**.
2. **From your terminal, execute the script with your search query:**
   ```bash
   python google_search.py keyword1 keyword2 
   ```

   For example:
   ```bash
   python google_search.py python web scraping 
   ```

## How It Works

1. **Parses Command-Line Arguments:** Uses `argparse` to handle search keywords provided by the user.
2. **Constructs and Executes Google Search Query:** Sends a request to the Google Custom Search JSON API with the provided API key, CSE ID, and search terms.
3. **Displays Interactive Search Results:** Presents the user with a list of search result titles and links.
4. **Handles User Selection:** Allows the user to navigate and choose a search result using the arrow keys and Enter key.
5. **Optionally Triggers GPT-4o Analysis:** If the `gpt` module is available and configured, it processes the content of the selected web page using GPT-4o.

## Notes

* This script assumes you have a separate `gpt` module that handles the GPT-4o interaction.
* The script utilizes the `prompt_toolkit` library for an enhanced interactive command-line experience. 
* Consider error handling and security best practices when working with API keys and external data sources.
