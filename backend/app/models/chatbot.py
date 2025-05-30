"""
Chatbot model for the arXiv CS Expert Chatbot.
This module implements the core chatbot functionality.
"""

from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama  # Using the community version for compatibility
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

from app.mcp.arxiv_client import ArxivMCPClient

class Chatbot:
    """
    A chatbot that leverages arXiv data via MCP to provide expert responses
    on computer science topics.
    """

    def __init__(self, model_name="llama3.1:8b"):
        """
        Initialize the chatbot with the specified LLM model.

        Args:
            model_name (str): The name of the Ollama model to use.
        """
        # Initialize the LLM with a higher temperature for more creative responses
        self.llm = Ollama(
            model=model_name,
            temperature=0.7  # Add some creativity
        )

        # Initialize the MCP client
        self.arxiv_client = ArxivMCPClient()

        # Set up memory for conversation history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Set up tools for the agent (only used for paper summarization)
        self.tools = self._create_tools()

        # Initialize the agent with error handling (only used for paper summarization)
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )

    def _create_tools(self):
        """
        Create tools for the agent to use.

        Returns:
            list: A list of Tool objects.
        """
        download_tool = Tool(
            name="download_paper",
            func=self.arxiv_client.download_paper,
            description="Download a specific arXiv paper. Input should be a paper ID (e.g., '2401.12345')."
        )

        analyze_tool = Tool(
            name="analyze_paper",
            func=self.arxiv_client.analyze_paper,
            description="Analyze a specific arXiv paper. Input should be a paper ID (e.g., '2401.12345')."
        )

        return [download_tool, analyze_tool]

    def _parse_intent(self, query):
        """
        Parse the user's intent from the query.

        Args:
            query (str): The user's query.

        Returns:
            tuple: (intent, content)
        """
        query = query.lower().strip()

        if query.startswith("explain "):
            return "explain", query[len("explain "):]
        elif query.startswith("summarize "):
            return "summarize", query[len("summarize "):]

        # If no specific command is detected, treat as a general question
        return "general", query

    def process_query(self, query):
        """
        Process a user query and return a response.

        Args:
            query (str): The user's query.

        Returns:
            dict: Response containing text and possibly sources.
        """
        intent, content = self._parse_intent(query)

        try:
            if intent == "explain":
                # Use a more direct prompt that doesn't require the agent to search for papers
                prompt = f"""
                Explain the computer science concept: {content}

                Important: Provide a direct explanation based on your knowledge.
                Do NOT try to search for or download papers about this topic.
                Focus on giving a clear, concise explanation with examples if appropriate.

                At the end of your explanation, include 2-3 relevant research papers that someone could read to learn more.
                Format each paper reference on a new line exactly like this:
                Paper Title | Author1, Author2 | Year | arXiv:XXXX.XXXXX

                For papers without an arXiv ID, just omit that part:
                Paper Title | Author1, Author2 | Year

                Make sure to separate each field with the | character.
                """
                response = self.llm.invoke(prompt)

                # Extract sources from the response
                sources = self._extract_sources(response)

                return {
                    "response": response,
                    "sources": sources
                }

            elif intent == "summarize":
                # Check if content is a paper ID or title
                if content.startswith("20") and "." in content:  # Likely a paper ID
                    # Use the agent for paper summarization
                    response = self.agent.invoke({"input": f"Summarize the arXiv paper with ID {content}"})

                    # Create a source for the summarized paper
                    paper_info = self.arxiv_client.analyze_paper(content)

                    # Clean up the arXiv ID to ensure it's in the correct format
                    clean_arxiv_id = content.lower().replace("arxiv:", "").split("v")[0].strip()

                    sources = [{
                        "id": content,
                        "title": paper_info.get("title", f"Paper {content}"),
                        "authors": paper_info.get("authors", ["Unknown"]),
                        "url": f"https://arxiv.org/abs/{clean_arxiv_id}",
                        "year": paper_info.get("year", "")
                    }]

                    return {
                        "response": response["output"],
                        "sources": sources
                    }
                else:
                    # Use a more direct prompt for topic summarization
                    prompt = f"""
                    Provide a summary of research on the topic: '{content}'

                    Important: Give a general overview of the field based on your knowledge.
                    Focus on key concepts, major developments, and current state of research.

                    At the end of your summary, include 2-3 relevant research papers that someone could read to learn more.
                    Format each paper reference on a new line exactly like this:
                    Paper Title | Author1, Author2 | Year | arXiv:XXXX.XXXXX

                    For papers without an arXiv ID, just omit that part:
                    Paper Title | Author1, Author2 | Year

                    Make sure to separate each field with the | character.
                    """
                    response = self.llm.invoke(prompt)

                    # Extract sources from the response
                    sources = self._extract_sources(response)

                    return {
                        "response": response,
                        "sources": sources
                    }

            else:  # General query
                # Use a more direct prompt for general questions
                prompt = f"""
                Answer this computer science question: {content}

                Important: Provide a direct answer based on your knowledge.
                Be clear, concise, and accurate. Include examples if helpful.

                At the end of your answer, include 1-2 relevant research papers that someone could read to learn more.
                Format each paper reference on a new line exactly like this:
                Paper Title | Author1, Author2 | Year | arXiv:XXXX.XXXXX

                For papers without an arXiv ID, just omit that part:
                Paper Title | Author1, Author2 | Year

                Make sure to separate each field with the | character.
                """
                response = self.llm.invoke(prompt)

                # Extract sources from the response
                sources = self._extract_sources(response)

                return {
                    "response": response,
                    "sources": sources
                }

        except Exception as e:
            import traceback
            print(f"Error in process_query: {str(e)}")
            print(traceback.format_exc())
            return {"response": f"I'm sorry, I encountered an error while processing your query. Please try again with a different question or rephrase your current one."}

    def _extract_sources(self, text):
        """
        Extract sources from the response text.

        Args:
            text (str): The response text.

        Returns:
            list: A list of source objects.
        """
        import re
        import uuid

        # Define a pattern to match paper references
        # Looking for patterns like: Title | Authors | Year | arXiv ID
        # The pattern is designed to match lines that have the specific format with | separators
        pattern = r"([^|\n]+)\s*\|\s*([^|\n]+)\s*\|\s*([^|\n]+)(?:\s*\|\s*([^|\n]+))?"

        # Find all matches
        matches = re.findall(pattern, text)

        sources = []
        for match in matches:
            title = match[0].strip()
            authors = [author.strip() for author in match[1].split(',')]
            year = match[2].strip()
            # Extract and clean arXiv ID if present
            arxiv_id = None
            if len(match) > 3 and match[3].strip():
                # Look for patterns like arXiv:XXXX.XXXXX or just XXXX.XXXXX
                arxiv_text = match[3].strip()
                if "arxiv" in arxiv_text.lower():
                    # Extract the ID part after "arXiv:"
                    import re
                    arxiv_match = re.search(r'arxiv:?(\d+\.\d+)', arxiv_text.lower())
                    if arxiv_match:
                        arxiv_id = arxiv_match.group(1)
                    else:
                        arxiv_id = arxiv_text
                else:
                    # Check if it looks like an arXiv ID (XXXX.XXXXX)
                    import re
                    arxiv_match = re.search(r'(\d+\.\d+)', arxiv_text)
                    if arxiv_match:
                        arxiv_id = arxiv_match.group(1)
                    else:
                        arxiv_id = arxiv_text

            # Create a URL based on arXiv ID if available
            if arxiv_id:
                # Clean up the arXiv ID to ensure it's in the correct format
                # Remove any "arXiv:" prefix and any version suffix like "v1"
                clean_arxiv_id = arxiv_id.lower().replace("arxiv:", "").split("v")[0].strip()

                # Check if it looks like a valid arXiv ID (typically has a dot or slash)
                if "." in clean_arxiv_id or "/" in clean_arxiv_id:
                    url = f"https://arxiv.org/abs/{clean_arxiv_id}"
                else:
                    # If it doesn't look like a valid arXiv ID, use a search URL
                    url = f"https://arxiv.org/search/?query={clean_arxiv_id}&searchtype=all"
            else:
                # For non-arXiv papers, create a more specific search URL
                # Include title and authors for better results
                search_query = f"{title} {' '.join(authors[:2])} {year}".replace(' ', '+')
                url = f"https://scholar.google.com/scholar?q={search_query}"

            sources.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "authors": authors,
                "url": url,
                "year": year
            })

        return sources
