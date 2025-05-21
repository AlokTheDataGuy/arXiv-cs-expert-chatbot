# arXiv CS Expert Chatbot - Technical Documentation

## Project Overview

The arXiv CS Expert Chatbot is an advanced conversational AI system designed to serve as a computer science expert, leveraging the arXiv dataset to provide accurate, research-backed responses. The chatbot is built using free and open-source tools, making it accessible for local development and testing without requiring cloud deployment or paid services.

## Key Features

### 1. Chat Interface
- **Expert Responses**: Provides accurate, research-backed answers to computer science questions
- **Paper Summaries**: Summarizes arXiv research papers using their IDs (e.g., "summarize 2105.08123")
- **Concept Explanations**: Explains complex computer science concepts in detail (e.g., "explain neural networks")
- **Conversation Context**: Maintains context for natural follow-up questions

### 2. Paper Search
- Search for relevant papers on arXiv using keywords
- View paper metadata including title, authors, abstract, and publication date
- Direct links to original arXiv papers

### 3. Visualization
- Generate visualizations of computer science concepts
- View diagrams of algorithms, data structures, and other CS concepts
- Fallback to text-based images if Graphviz is not available

## Technical Architecture

### System Components

#### 1. Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Key Libraries**:
  - `react-router-dom` for navigation
  - `axios` for API requests
  - `react-markdown` for rendering markdown content
  - `react-icons` for UI icons

#### 2. Backend
- **Framework**: FastAPI (Python)
- **Key Libraries**:
  - `langchain` for LLM integration
  - `langchain_community` for Ollama integration
  - `graphviz` for diagram generation
  - `uvicorn` for ASGI server

#### 3. LLM Integration
- **Model**: llama3.1:8b via Ollama
- **Integration**: LangChain for connecting to Ollama
- **Memory**: ConversationBufferMemory for maintaining chat context

#### 4. Data Source
- **arXiv Papers**: Accessed via Model Context Protocol (MCP)
- **Client**: Custom ArxivMCPClient for paper retrieval and analysis

#### 5. Visualization
- **Library**: Graphviz for generating diagrams
- **Fallback**: PIL (Python Imaging Library) for text-based images

### Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  React Frontend │◄────┤  FastAPI Backend│◄────┤  Ollama (LLM)   │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │                       │
         │               ┌───────▼───────┐     ┌─────────────────┐
         │               │               │     │                 │
         └──────────────►│  MCP Client   │◄────┤  arXiv Dataset  │
                         │               │     │                 │
                         └───────┬───────┘     └─────────────────┘
                                 │
                                 │
                         ┌───────▼───────┐
                         │               │
                         │   Graphviz    │
                         │               │
                         └───────────────┘
```

## Implementation Details

### Backend Components

#### 1. FastAPI Application (`app/main.py`)
- Defines API endpoints for chat, search, and visualization
- Handles WebSocket connections for real-time chat
- Serves static files (images) for visualizations

#### 2. Chatbot Model (`app/models/chatbot.py`)
- Core chatbot functionality using LangChain and Ollama
- Intent parsing for different query types (explain, summarize, general)
- Source extraction from LLM responses
- Conversation memory management

#### 3. arXiv MCP Client (`app/mcp/arxiv_client.py`)
- Interface for searching, downloading, and analyzing arXiv papers
- Simulates MCP server responses for development
- Provides paper metadata and content

#### 4. Visualization Utility (`app/utils/visualizer.py`)
- Generates diagrams using Graphviz
- Uses LLM to create Graphviz DOT code
- Provides fallback mechanisms for when Graphviz is unavailable

### Frontend Components

#### 1. Chat Interface (`components/ChatInterface.tsx`)
- Real-time chat UI with message history
- Displays bot responses with markdown formatting
- Shows paper sources and generated images
- Maintains chat context

#### 2. Paper Search (`components/PaperSearch.tsx`)
- Search form for querying arXiv papers
- Displays search results with paper metadata
- Provides direct links to original papers on arXiv

#### 3. Visualization (`components/Visualization.tsx`)
- Interface for generating concept visualizations
- Displays generated diagrams
- Handles loading states and errors

#### 4. Message Bubble (`components/MessageBubble.tsx`)
- Renders individual chat messages
- Supports markdown, images, and paper sources
- Different styling for user and bot messages

## Data Flow

1. **Chat Flow**:
   - User sends a message via the chat interface
   - Backend parses the intent (explain, summarize, general)
   - LLM generates a response based on the intent
   - Response is sent back to the frontend with any sources or images
   - Frontend displays the response with proper formatting

2. **Search Flow**:
   - User enters a search query
   - Backend searches for relevant papers using the MCP client
   - Results are returned to the frontend
   - Frontend displays the paper metadata with links to arXiv

3. **Visualization Flow**:
   - User enters a concept to visualize
   - Backend uses the LLM to generate Graphviz DOT code
   - Graphviz renders the diagram as an image
   - Image path is returned to the frontend
   - Frontend displays the generated image

## Technical Requirements

### Software Requirements
- **Python**: 3.8+
- **Node.js**: 16+
- **Ollama**: Latest version with llama3.1:8b model
- **Graphviz**: Latest version (optional, for diagram generation)

### Hardware Requirements
- **CPU**: 4+ cores recommended for running Ollama
- **RAM**: 8GB+ (16GB recommended for optimal performance)
- **Storage**: 10GB+ free space for models and application

## Setup and Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd arvix-cs-expert-chatbot
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Install Ollama and Download the Model
Follow instructions at [Ollama's website](https://ollama.com/) to install Ollama, then run:
```bash
ollama pull llama3.1:8b
```

### 5. Install Graphviz (Optional)
Follow instructions at [Graphviz's website](https://graphviz.org/download/) to install Graphviz and add it to your system PATH.

## Running the Application

### Using the Convenience Scripts
- **Windows**: Run `run.bat`
- **Linux/Mac**: Run `./run.sh`

### Manual Startup
1. Start Ollama:
```bash
ollama serve
```

2. Start the backend:
```bash
cd backend
python run.py
```

3. Start the frontend:
```bash
cd frontend
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Example Usage

### Chat Interface
- "explain neural networks"
- "summarize 2105.08123"
- "What is the difference between supervised and unsupervised learning?"
- "How does blockchain technology work?"

### Paper Search
- "neural networks"
- "quantum computing"
- "blockchain"

### Visualization
- "binary tree"
- "neural network"
- "sorting algorithm"

## Future Enhancements

1. **Enhanced Paper Analysis**: Deeper integration with arXiv for more detailed paper analysis
2. **Multi-Modal Support**: Adding support for images and diagrams in explanations
3. **User Accounts**: Saving chat history and favorite papers
4. **Citation Generation**: Generating proper academic citations for papers
5. **Interactive Visualizations**: Making diagrams interactive for better understanding

## Troubleshooting

### Common Issues

1. **Ollama Connection Issues**:
   - Ensure Ollama is running with `ollama serve`
   - Verify the model is downloaded with `ollama list`

2. **Visualization Not Working**:
   - Check if Graphviz is installed and in your PATH
   - The system will fall back to text-based images if Graphviz is unavailable

3. **Backend Connection Issues**:
   - Verify the backend is running on port 8000
   - Check for any CORS issues in the browser console

4. **Frontend Development Issues**:
   - Clear node_modules and reinstall with `npm clean-install`
   - Check for TypeScript errors with `npm run lint`
