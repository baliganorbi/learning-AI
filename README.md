# AI Learning Project

A collection of Jupyter Notebooks exploring various AI-related topics and techniques as I learn them.

## Notebooks

### **llamaindex-google-genai.ipynb**
Demonstrates various features of Google's GenAI with LlamaIndex integration:
- Basic LLM completion and streaming with GoogleGenAI
- Cached content support for improved performance and cost efficiency with large contexts
- Multi-modal support: processing PDFs, images, and text in a single request
- Structured prediction using Pydantic models for extraction
- Works with Google's Vertex AI generative models (Gemini family)

### **llamaindex-agents.ipynb**
Comprehensive guide to building AI agents with LlamaIndex:
- **FunctionAgent**: Simple agent for custom Python functions
- **AgentWorkflow**: More flexible agent implementation with tool composition
- Integration with existing tools (Yahoo Finance ToolSpec) for financial data retrieval
- State management: Maintaining conversation state across multiple runs using Context
- Serialization of agent context for persistence and restoration

### **llamaindex-local-ollama.ipynb**
Explores running local Large Language Models with LlamaIndex:
- Integration with Ollama for running open-source models locally
- Completion API for simple text generation
- Chat messaging with system prompts and roles
- Streaming support for real-time token generation
- Uses Gemma3 (1B parameter model) for local inference

## Python Modules

### **agent-state.py**
A standalone module demonstrating agent state management and persistence:
- Creates an AgentWorkflow with financial tools (Yahoo Finance) and custom math functions
- Uses GoogleGenAI (Gemini) as the underlying LLM via Vertex AI
- Demonstrates Context-based state management for multi-turn conversations
- Shows how to serialize and restore agent state using JsonSerializer

## Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab
- LlamaIndex library: `pip install llama-index`
- LlamaIndex Google GenAI integration: `pip install llama-index-llms-google-genai google-genai`
- LlamaIndex Ollama integration (optional): `pip install llama-index-llms-ollama`
- Environment variables configured for Google Cloud (for Google GenAI notebooks):
  - `GCP_PROJECT_ID` - Your Google Cloud project ID
  - `GCP_LOCATION` - The region for Vertex AI (e.g., "us-central1")
  - `GOOGLE_API_KEY` - Your Google GenAI API key

### Running the Notebooks

1. Clone or navigate to this repository
2. Install dependencies:
   ```bash
   pip install jupyter llama-index llama-index-llms-google-genai llama-index-llms-ollama google-genai
   ```
3. Set up environment variables (create a `.env` file):
   ```
   GCP_PROJECT_ID=your-project-id
   GCP_LOCATION=us-central1
   GOOGLE_API_KEY=your-api-key
   ```
4. Start Jupyter:
   ```bash
   jupyter notebook
   ```
5. Open any `.ipynb` file to explore the content

### Project Structure

- `llamaindex-*.ipynb` - Interactive notebooks exploring different AI topics
- `agent-state.py` - Python module demonstrating agent state management
- `chroma_db/` - Vector database for embeddings storage
- `data/` - Supporting data files and documents

## About

This project serves as a learning space for experimenting with LlamaIndex framework and various AI technologies. It includes:
- Cloud-based models: Google's Gemini models via Vertex AI
- Local models: Open-source models via Ollama
- Agent design patterns and state management
- Multi-modal AI capabilities and structured output generation

## Key Topics Covered

- **LLM Integration**: Working with different LLM providers (Google GenAI, Local Ollama)
- **Agent Architectures**: Building function-based and workflow-based agents
- **State Management**: Maintaining conversational context and persistence
- **Advanced Features**: Caching, multi-modal inputs, structured prediction
- **Tools & Integrations**: Using specialized tool packages (Yahoo Finance, etc.)

## Notes

- Each notebook is self-contained and can be run independently
- Notebooks require appropriate API keys and credentials to be configured
- The `agent-state.py` module can be run directly using: `python agent-state.py`
- For local LLM examples, ensure Ollama is installed and running
- Token limits and context windows vary by model - check individual notebooks for specifics

---

*Last Updated: February 2026*
