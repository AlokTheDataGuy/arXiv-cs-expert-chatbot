"""
Test script for the arXiv CS Expert Chatbot.
This script tests the core functionality of the chatbot.
"""

import os
import sys
from app.models.chatbot import Chatbot
from app.mcp.arxiv_client import ArxivMCPClient

def test_arxiv_client():
    """Test the arXiv MCP client."""
    print("Testing arXiv MCP client...")
    
    client = ArxivMCPClient()
    
    # Test search
    print("\nTesting search_papers...")
    results = client.search_papers("neural networks", max_results=2)
    print(f"Found {len(results)} papers")
    for paper in results:
        print(f"- {paper['title']} by {', '.join(paper['authors'])}")
    
    # Test download
    print("\nTesting download_paper...")
    paper_id = "2103.12112"  # This is a simulated paper ID
    content = client.download_paper(paper_id)
    print(f"Downloaded paper {paper_id}, content length: {len(content)} characters")
    
    # Test analyze
    print("\nTesting analyze_paper...")
    analysis = client.analyze_paper(paper_id)
    print(f"Analyzed paper {paper_id}")
    print(f"Key concepts: {', '.join(analysis['key_concepts'])}")
    print(f"Main contributions: {len(analysis['main_contributions'])}")
    
    print("\narXiv MCP client tests completed successfully!")

def test_chatbot():
    """Test the chatbot functionality."""
    print("\nTesting chatbot...")
    
    chatbot = Chatbot()
    
    # Test explain
    print("\nTesting 'explain' functionality...")
    response = chatbot.process_query("explain neural networks")
    print(f"Response: {response['response'][:100]}...")
    
    # Test search
    print("\nTesting 'search' functionality...")
    response = chatbot.process_query("search quantum computing")
    print(f"Response: {response['response'][:100]}...")
    
    # Test summarize
    print("\nTesting 'summarize' functionality...")
    response = chatbot.process_query("summarize 2105.08123")
    print(f"Response: {response['response'][:100]}...")
    
    # Test visualize
    print("\nTesting 'visualize' functionality...")
    response = chatbot.process_query("visualize binary tree")
    print(f"Response: {response['response']}")
    if 'image' in response:
        print(f"Image: {response['image']}")
    
    print("\nChatbot tests completed successfully!")

if __name__ == "__main__":
    # Create images directory if it doesn't exist
    os.makedirs("static/images", exist_ok=True)
    
    # Run tests
    test_arxiv_client()
    test_chatbot()
    
    print("\nAll tests completed successfully!")
