# arXiv CS Expert Chatbot

A computer science expert chatbot that leverages the arXiv dataset to deliver accurate, research-backed responses. The chatbot can answer complex queries, summarize research papers, explain advanced concepts, search for papers, and visualize concepts, all while maintaining conversation context for follow-up questions.

## Features

The application is divided into three main sections:

### Chat Interface
- **Expert Responses**: Get accurate, research-backed answers to computer science questions
- **Paper Summaries**: Summarize arXiv research papers
- **Concept Explanations**: Explain complex computer science concepts
- **Conversation Context**: Maintain context for follow-up questions

### Paper Search
- Search for relevant papers on arXiv
- View paper metadata including title, authors, abstract, and publication date

### Visualization
- Generate visualizations of computer science concepts
- View diagrams of algorithms, data structures, and other CS concepts

## Architecture

The chatbot is built using the following components:

- **Backend**: FastAPI with LangChain for integration with Ollama and arXiv
- **Frontend**: React with TypeScript
- **LLM**: llama3.1:8b:8b via Ollama
- **Data Source**: arXiv papers via MCP (Model Context Protocol)
- **Visualization**: Graphviz for generating diagrams

## Prerequisites

- Python 3.8+
- Node.js 16+
- Ollama (with llama3.1:8b:8b model)
- Graphviz (optional, for diagram generation)

Note: If Graphviz is not installed, the chatbot will still work but will generate text-based images instead of diagrams for visualization requests.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd arvix-cs-expert-chatbot
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up the frontend

```bash
cd frontend
npm install
```

### 4. Install Ollama and download the llama3.1:8b:8b model

Follow the instructions at [Ollama's website](https://ollama.com/) to install Ollama, then run:

```bash
ollama pull llama3.1:8b
```

## Running the Application

### 1. Start the Ollama server

```bash
ollama serve
```

### 2. Start the backend server

```bash
cd backend
python run.py
```

### 3. Start the frontend development server

```bash
cd frontend
npm run dev
```

### 4. Open the application

Open your browser and navigate to `http://localhost:5173`

## Usage

### Chat Interface
The chatbot supports the following commands:
- `explain <concept>`: Explain a computer science concept
- `summarize <paper_id>`: Summarize a research paper by ID
- You can also ask general questions about computer science topics

### Paper Search
- Enter a search query to find relevant papers on arXiv
- View the search results with paper details

### Visualization
- Enter a concept to generate a visualization
- View the generated diagram

## Example Queries

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

## Development

### Backend Structure

- `app/main.py`: FastAPI application
- `app/models/chatbot.py`: Core chatbot functionality
- `app/mcp/arxiv_client.py`: arXiv MCP client
- `app/utils/visualizer.py`: Visualization utilities

### Frontend Structure

- `src/components/`: React components
- `src/services/`: API services
- `src/types/`: TypeScript type definitions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [arXiv](https://arxiv.org/) for providing access to research papers
- [Ollama](https://ollama.com/) for the LLM
- [LangChain](https://python.langchain.com/) for the integration framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
- [Graphviz](https://graphviz.org/) for visualization
