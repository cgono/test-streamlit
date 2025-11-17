# test-streamlit

A Streamlit app integrated with LangChain and OpenAI, providing an interactive chat interface powered by GPT models.

## Current Status

This project is configured to use **Python 3.14**, which was recently released. However, some of Streamlit's dependencies (specifically `pyarrow`) do not yet have pre-built wheels for Python 3.14, which causes installation to fail when trying to build from source.

### Workaround

Until pre-built wheels become available for Python 3.14, you can use **Python 3.13** as a temporary alternative:

```bash
# Switch to Python 3.13
echo "3.13" > .python-version

# Update pyproject.toml to require Python >= 3.13
# Then install dependencies
uv sync
```

## Setup

### Prerequisites

- Python 3.12+ (3.13 recommended)
- [uv](https://docs.astral.sh/uv/) package manager (optional) or pip
- OpenAI API key (get one at [OpenAI Platform](https://platform.openai.com/api-keys))

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install streamlit langchain-openai langgraph python-dotenv
   ```

3. Configure your OpenAI API key:
   ```bash
   # Create a .env file from the example
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-api-key-here
   ```

4. Run the Streamlit app:
   ```bash
   # Using uv
   uv run streamlit run app.py
   
   # Or using the virtual environment
   source .venv/bin/activate
   streamlit run app.py
   ```

## Project Structure

- `app.py` - Main Streamlit application with LangChain graph integration
- `pyproject.toml` - Project configuration and dependencies
- `.python-version` - Python version specification
- `.env.example` - Example environment variables file
- `.env` - Your environment variables (not committed to git)

## Features

- **LangChain Graph Integration**: Uses LangGraph to create a stateful conversation flow
- **OpenAI Integration**: Powered by GPT-4o-mini for intelligent responses
- **Chat Interface**: Clean Streamlit chat UI with message history
- **Environment Configuration**: Secure API key management via .env file

## Usage

### Basic Usage

Run the app locally:
```bash
# Using uv
uv run streamlit run app.py

# Or using the virtual environment
source .venv/bin/activate
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Using the Chat Interface

1. Make sure your OpenAI API key is configured in the `.env` file
2. Open the app in your browser
3. Type your message in the chat input box
4. Press Enter or click Send
5. The LangChain graph will process your query and return a response from OpenAI
6. Continue the conversation - the chat history is maintained in the session
7. Use the "Clear Chat History" button in the sidebar to start a new conversation

## Development

### Code Quality Tools

This project uses the following code quality tools:
- **ruff**: Fast Python linter and code formatter
- **mypy**: Static type checker
- **pre-commit**: Git hooks to run checks before commits

#### Setup Pre-commit Hooks

Install the pre-commit hooks:
```bash
uv run pre-commit install
```

#### Running Code Quality Checks

Run ruff linter:
```bash
uv run ruff check .
```

Run ruff formatter:
```bash
uv run ruff format .
```

Run mypy type checker:
```bash
uv run mypy app.py
```

Run all pre-commit hooks manually:
```bash
uv run pre-commit run --all-files
```

### Adding Dependencies

Add new dependencies:
```bash
uv add <package-name>
```

Remove dependencies:
```bash
uv remove <package-name>
```

## Note on Python 3.14

This project is configured for Python 3.14. Once the Python ecosystem catches up and pyarrow releases wheels for Python 3.14, you can update `.python-version` back to `3.14` and run:

```bash
rm -rf .venv uv.lock
uv sync
```
