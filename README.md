# MCP Client

A Python client for interacting with Claude AI models using the Model Context Protocol (MCP).

## Description

This project provides a command-line interface for connecting to MCP servers and using their tools with Claude AI models. It allows you to:

- Connect to MCP servers via Docker, Python, JavaScript, or TypeScript
- Send queries to Claude AI models
- Use tools provided by connected MCP servers
- Process responses in an interactive chat loop

## Requirements

- Python 3.7+
- Anthropic API key
- MCP server(s)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Configuration

Configure MCP servers by setting environment variables in your `.env` file:

```
MCP_MEMORY_SERVER=docker://mcp/memory:latest
# Add more MCP servers as needed
# MCP_WEATHER_SERVER=path_to_weather_server_script
```

## Usage

Run the client:

```bash
python mcp_client.py
```

Enter your questions at the prompt. Type `quit` or `exit` to end the session.

## Supported MCP Server Types

- Docker images: `docker://<image[:tag]>`
- Python scripts: `*.py`
- JavaScript files: `*.js`
- TypeScript files: `*.ts`

## License

[License information]
