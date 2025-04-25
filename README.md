# Customer Service Chatbot with MCP Integration

A simple Streamlit chatbot application that serves customers and remembers their attributes using OpenAI for the LLM and two MCPs: Knowledge Graph Memory for persistent memory and Weather MCP for providing weather information. This project now includes proper MCP client implementation.

## Features

- Streamlit application with proper MCP client integration
- Support for both OpenAI and Google Gemini LLMs
- Knowledge Graph Memory MCP for persistent customer information storage
- Weather MCP for providing weather information to customers
- Extracts and remembers customer attributes (names, preferences, etc.)
- Simple and intuitive chat interface
- Standalone MCP client for direct interaction with MCP servers

## Requirements

- Python 3.8+
- OpenAI API key (for original implementation)
- Google API key (for new MCP client implementation)
- MCP server setup for Knowledge Graph Memory and Weather

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` file to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

## Configuration

### OpenAI API Key

You need to set up your OpenAI API key in one of the following ways:

1. Set it as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

2. Create a `.streamlit/secrets.toml` file with the following content:
   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   ```

3. Enter it directly in the application's sidebar when prompted

### MCP Setup

#### Knowledge Graph Memory MCP

To use the Knowledge Graph Memory MCP, you need to set it up according to the documentation:

#### VS Code Installation

For quick installation, use one of the one-click installation buttons:

- Install with NPX in VS Code
- Install with Docker in VS Code

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code:

```json
{
  "mcp": {
    "servers": {
      "memory": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-memory"
        ]
      }
    }
  }
}
```

Or with Docker:

```json
{
  "mcp": {
    "servers": {
      "memory": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "-v",
          "claude-memory:/app/dist",
          "--rm",
          "mcp/memory"
        ]
      }
    }
  }
}
```

#### Weather MCP

To use the Weather MCP, you need to set it up in your VS Code settings:

```json
{
  "mcp": {
    "servers": {
      "weather": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-weather"
        ]
      }
    }
  }
}
```

Or with Docker:

```json
{
  "mcp": {
    "servers": {
      "weather": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "mcp/weather"
        ]
      }
    }
  }
}
```

## Usage

### Original Streamlit Application

1. Start the original Streamlit application:

```bash
streamlit run customer_chatbot.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

3. Enter your OpenAI API key in the sidebar if not configured through environment variables or secrets

### New MCP Client Implementation

#### Streamlit Application with MCP Client

1. Start the new Streamlit application with proper MCP client integration:

```bash
streamlit run customer_chatbot_mcp.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

3. Enter your Google API key in the sidebar if not configured through environment variables

#### Standalone MCP Client

1. Run the standalone MCP client with a specific server script:

```bash
python mcp_client.py
```

This will connect to both the Memory and Weather MCP servers configured in `.vscode/mcp.json`.

2. Or run with a specific server script:

```bash
python run_mcp_client.py path/to/server/script.py
```

3. Start chatting with the MCP client! The application will:
   - Process your queries using the MCP tools
   - Store information in the Knowledge Graph Memory
   - Provide weather information when asked
   - Generate responses using Google Gemini LLM

## How It Works

### Original Implementation

1. **Information Extraction**: The application uses OpenAI to extract relevant customer information from messages
2. **Knowledge Storage**: Extracted information is stored in the Knowledge Graph Memory as entities, relations, and observations
3. **Contextual Responses**: When generating responses, the application retrieves relevant customer information from the Knowledge Graph and includes it in the context sent to OpenAI
4. **Weather Information**: When a user asks about weather in a specific location, the application uses the Weather MCP to fetch and display current weather information

### New MCP Client Implementation

1. **MCP Client Initialization**: The application establishes connections with MCP servers using the proper MCP client protocol
2. **Tool Loading**: Tools from the MCP servers are loaded and made available to the agent
3. **Agent Creation**: A React agent is created with the Google Gemini LLM and the loaded MCP tools
4. **Query Processing**: User queries are processed by the agent, which can use the MCP tools to access external services
5. **Response Generation**: The agent generates responses based on the query and the results of tool usage

## Customization

You can customize the application by modifying the following aspects:

### Original Implementation
- Change the OpenAI model in the `extract_customer_info` and `generate_response` functions
- Modify the system prompts to change how information is extracted or how the chatbot responds
- Add additional fields to extract in the `extract_customer_info` function
- Enhance the UI with additional Streamlit components

### New MCP Client Implementation
- Change the Google Gemini model or parameters in the `initialize_mcp` function
- Add support for additional MCP servers by modifying the `server_names` list
- Customize the agent behavior by modifying the React agent configuration
- Enhance the UI with additional Streamlit components

## Files

- `customer_chatbot.py`: Original Streamlit application with direct MCP integration
- `customer_chatbot_mcp.py`: New Streamlit application with proper MCP client integration
- `mcp_client.py`: Standalone MCP client that connects to configured MCP servers
- `run_mcp_client.py`: Utility script to run the MCP client with a specific server script
- `requirements.txt`: List of required Python packages
- `.vscode/mcp.json`: MCP server configuration for VS Code
- `.env.example`: Example environment variables file

## License

This project is open source and available under the MIT License.
