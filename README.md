# LLM Chat Tool

This is a simple command-line tool for interacting with LLM APIs.  It allows you to:

* Send text prompts and receive responses.
* Read text from files or URLs and send it to the LLM as a prompt.
* Manage your conversation history.
* Set custom prompts.
* Easily change the chunk size for processing large amounts of text.

## Requirements

* Python 3.6 or later
* `requests`
* `filetype`
* `pypdf`
* `beautifulsoup4`
* `prompt_toolkit`
* `dotenv`

You can install the requirements using pip:

```bash
pip install requests filetype pypdf beautifulsoup4 prompt-toolkit dotenv
```

## Usage

1. **Set up your environment:**
   - Create a `.env` file in the same directory as the script.
   - Add your LLM API credentials to the `.env` file. Refer to the specific LLM API documentation for the required environment variables. 
   - Refer to the `example.env` file for a sample environment file.

2. **Run the script:**

   ```bash
   python llm_chat_tool.py
   ```

3. **Interact with the LLM:**

   - You can provide text prompts directly in the terminal.
   - You can also provide a file path or URL as an argument to the script.
   - Use the following commands to manage your conversation:
     - `.q` or `.quit`: Quit the chat tool.
     - `.h` or `.history`: Show the chat history.
     - `.clear`: Clear the chat history.
     - `.info`: Print information about the current model, chunk size, etc.
     - `.g` or `.goto`: Go to the beginning of the text.
     - `.goto N`: Go to position N in the text.
     - `.chunk=N` or `.chunk N`: Set the chunk size to N.
     - `.prompt=PROMPT` or `.prompt PROMPT`: Set the default prompt to PROMPT.
     - `.o` or `.open`: Open the URL being processed in a web browser.
   - Use the `-a` or `--all` flag to process the entire text as a single chunk.
   - Use the `-p` or `--prompt` flag to override the default prompt for external data.

## Example

```bash
# Run the script with a text file
python llm_chat_tool.py my_file.txt

# Run the script with a URL
python llm_chat_tool.py https://www.example.com

# Run the script with a direct prompt and override the default prompt
python llm_chat_tool.py "What is the meaning of life?" -p "Please answer the question in a philosophical way."

# Run the script and set the chunk size to 5000
python llm_chat_tool.py -c 5000
```

## Configuration

The following environment variables can be set in the `.env` file to customize the chat tool:

- **`DEFAULT_CHUNK_SIZE`**: The default chunk size for processing text.
- **`DEFAULT_PROMPT`**: The default prompt used for external data.
- **`PROMPT_HISTORY`**: The path to the file where the input history is stored.
- **`OUTPUT_HISTORY`**: The path to the file where the chat history is stored.
- **`SYSTEM_PROMPT`**: The system prompt used for the LLM.
- **`USER_AGENT`**: The User-Agent header used for HTTP requests.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

----

# Web Search Utility - google\_search.py

This Python script provides a command-line interface for web searches using Google Custom Search Engine and a language model for summarizing web pages.

## Features

- Uses Google Custom Search Engine API to perform web searches.
- Integrates with either Gemini or GPT models to summarize web pages.
- Provides a user-friendly menu for selecting search results.
- Allows users to navigate through multiple pages of search results.
- Supports user-agent and API key configuration via environment variables.

## Requirements

- Python 3.6 or higher
- `requests` library
- `urllib` library
- `prompt_toolkit` library
- `dotenv` library
- Gemini or GPT model (depending on the chosen helper)

## Installation

1. Install the required packages:
   ```bash
   pip install requests urllib3 prompt_toolkit dotenv
   ```

2. Install the Gemini or GPT model (depending on the chosen helper) by following their respective installation instructions.

## Configuration

1. Create a `.env` file in the same directory as the script.
2. Set the following environment variables:
   - `USER_AGENT`: Your desired user agent string (optional).
   - `GOOGLE_API_KEY`: Your Google Custom Search Engine API key.
   - `GOOGLE_CSE_ID`: Your Google Custom Search Engine ID.
   - `SEARCH_HELPER`: The chosen language model (either "gemini" or "gpt").
   - `GEMINI_MODEL`: The path to your Gemini model (if using Gemini).
   - `GPT_MODEL`: The path to your GPT model (if using GPT).

## Usage

1. Run the script from the command line:
   ```bash
   python web_search.py <query keywords>
   ```
   For example:
   ```bash
   python web_search.py "best restaurants in New York"
   ```

2. The script will display the search results and prompt you to select one.
3. After selecting a result, the script will use the chosen language model to summarize the web page and display the summary.

## Example

```
Query: best restaurants in New York

Search Results
Please select one search result from the following:

1. Best Restaurants in NYC | 2023 Guide (Michelin, Zagat, More)
2. The 50 Best Restaurants in New York City - Thrillist
3. 100 Best Restaurants in NYC | OpenTable
4. Best Restaurants in New York City - The New York Times
5. Best Restaurants in New York City - Eater
6. Previous
7. Next

```

## License

This project is licensed under the MIT License.

