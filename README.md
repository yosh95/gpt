# GPT Utility Script

This script is designed as a versatile tool for interacting with the OpenAI GPT models, including features for text summarization, conversation, and direct input processing from various sources like URLs, PDFs, and plain text files. It supports different versions of GPT models, configurable prompt settings, text chunk sizes for processing large documents, and a history of interactions for an ongoing conversation.

## Features

- **Model Selection**: Choose between GPT-3.5 Turbo and GPT-4 Turbo Preview models for text generation, or specify any OpenAI model name.
- **Multiple Source Inputs**: Accepts input from direct text prompts, URLs (fetching content from webpages), local PDF files, and plain text files.
- **Conversation History**: Maintains a configurable history of interactions to consider in ongoing conversations, enhancing context awareness.
- **Customizable Chunk Size**: Allows for setting a custom text chunk size for processing large documents in manageable pieces.
- **Dynamic Prompt Setting**: Enables specifying a custom prompt directly via command-line arguments for immediate text generation.

## Requirements

Before running this script, ensure the following dependencies are installed:

- Python 3.x
- `openai`: OpenAI Python client library for accessing GPT models.
- `requests`: For URL content fetching.
- `bs4` (BeautifulSoup4): For parsing HTML content from web pages.
- `pypdf`: For PDF file reading.
- `filetype`: For identifying file types.
- `prompt_toolkit`: For enhancing CLI interaction.
- `python-dotenv`: For loading environment variables from a `.env` file.

Additionally, you need an OpenAI API Key. Set this key in your environment variables or a `.env` file with the variable name `OPENAI_API_KEY`.

## Installation

1. Ensure you have Python 3 installed.
2. Install the required Python packages by running:
   ```bash
   pip install openai requests bs4 pypdf filetype prompt_toolkit python-dotenv
   ```
3. Clone this script or copy it to your local machine.

## Usage

Run the script from the command line, specifying the required options.

```bash
./gpt.py [source] [options]
```

### Options

- `source`: Optionally specify the source for the prompt. Can be a URL, a file path, or direct prompt text.
- `-c` or `--chunk_size`: Set the text chunk size (in characters) for reading operations. Default is 3000 characters.
- `-d` or `--depth`: Define the number of previous interactions to consider in the conversation history. Default is 8.
- `-m` or `--model`: Choose the GPT model for text generation. Options are `3` (for GPT-3.5 Turbo), `4` (for GPT-4 Turbo Preview), or an explicit OpenAI model name. Default is GPT-3.5 Turbo.
- `-p` or `--prompt`: Directly provide the text prompt for generation. This will override the default prompt set in environment variables or the `.env` file.

## Examples

- Running the script without specifying a source will start a prompt for manual text input:
  ```bash
  ./gpt.py
  ```
- To process text from a URL:
  ```bash
  ./gpt.py "http://example.com" --model 4
  ```
- Processing a PDF file with a custom chunk size:
  ```bash
  ./gpt.py "/path/to/document.pdf" -c 5000
  ```

## Environment Variables

The script utilizes several environment variables, which can be set directly or through a `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API Key.
- `GPT_DEFAULT_PROMPT`: Default prompt text when not specified via command-line arguments.
- `GPT_INPUT_HISTORY`: Path to save the input history for conversation mode.
- `GPT_SYSTEM_PROMPT`: A system prompt to prepend before every user input internally during conversations.
- `GPT_USER_AGENT`: Custom user-agent string for fetching URL content.

For additional help and options, run the script with `-h` or `--help`.

## Contributing

Feel free to fork this project, submit pull requests, or report bugs and suggest features via issues.

## License

This script is open-source software licensed under the MIT license.
