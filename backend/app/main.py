"""
Main FastAPI application for the arXiv CS Expert Chatbot.
"""

import os
import uuid
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import json

from app.models.chatbot import Chatbot
from app.mcp.arxiv_client import ArxivMCPClient
from app.utils.visualizer import generate_diagram

# Initialize FastAPI app
app = FastAPI(
    title="arXiv CS Expert Chatbot API",
    description="API for a computer science expert chatbot using arXiv data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create images directory if it doesn't exist
os.makedirs("static/images", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize chatbot and other components
chatbot = Chatbot()
arxiv_client = ArxivMCPClient()

# Define request and response models
class ChatRequest(BaseModel):
    query: str

class Source(BaseModel):
    id: str
    title: str
    authors: List[str]
    url: str
    year: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    image: Optional[str] = None
    sources: Optional[List[Source]] = None

class SearchRequest(BaseModel):
    query: str
    max_results: int = 10

class VisualizationRequest(BaseModel):
    concept: str

class VisualizationResponse(BaseModel):
    message: str
    image: str

class PaperSearchResult(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    published: str

# Define API endpoints
@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "arXiv CS Expert Chatbot API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat request and return a response."""
    if not request.query:
        raise HTTPException(status_code=400, detail="No query provided")

    try:
        print(f"Processing query: {request.query}")
        response = chatbot.process_query(request.query)
        print(f"Response: {response}")
        return response
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error processing query: {str(e)}")
        print(f"Traceback: {error_traceback}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/search", response_model=List[PaperSearchResult])
async def search_papers(request: SearchRequest):
    """Search for papers on arXiv."""
    if not request.query:
        raise HTTPException(status_code=400, detail="No query provided")

    try:
        results = arxiv_client.search_papers(request.query, request.max_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching papers: {str(e)}")

@app.post("/visualize", response_model=VisualizationResponse)
async def visualize_concept(request: VisualizationRequest):
    """Generate a visualization for a concept."""
    if not request.concept:
        raise HTTPException(status_code=400, detail="No concept provided")

    try:
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join("static/images", filename)

        # Generate the diagram
        generate_diagram(request.concept, filepath)

        return {
            "message": f"Visualization of {request.concept} created successfully",
            "image": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating visualization: {str(e)}")

@app.get("/images/{filename}")
async def get_image(filename: str):
    """Serve a generated image."""
    image_path = f"static/images/{filename}"
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)

# WebSocket connection for real-time chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            # Process the query
            response = chatbot.process_query(message["query"])

            # Send response back to client
            await websocket.send_json(response)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {str(e)}")
        await websocket.send_json({"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
