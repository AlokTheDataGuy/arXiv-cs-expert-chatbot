"""
Visualization utilities for the arXiv CS Expert Chatbot.
This module provides functions for generating visualizations of computer science concepts.
"""

import os
import sys
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except (ImportError, Exception):
    GRAPHVIZ_AVAILABLE = False

from langchain_community.llms import Ollama

def generate_diagram(description, output_path):
    """
    Generate a diagram based on a description.

    Args:
        description (str): Description of the concept to visualize.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the generated image.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Check if Graphviz is available
    if not GRAPHVIZ_AVAILABLE:
        return _create_text_image(description, output_path)

    # For complex diagrams, we can use the LLM to generate the Graphviz DOT code
    try:
        llm = Ollama(model="llama3.1:8b")

        prompt = f"""
        Generate Graphviz DOT code to visualize the following computer science concept:
        {description}

        The DOT code should be simple and clear, focusing on the key elements of the concept.
        Only return the DOT code without any explanations or markdown formatting.
        """

        try:
            # Get DOT code from LLM
            dot_code = llm.invoke(prompt).strip()

            # Clean up the DOT code if needed
            if "```" in dot_code:
                # Extract code from markdown code block if present
                dot_code = dot_code.split("```")[1]
                if dot_code.startswith("dot") or dot_code.startswith("graphviz"):
                    dot_code = "\n".join(dot_code.split("\n")[1:])
                dot_code = dot_code.strip()

            # Create a Graphviz object from the DOT code
            try:
                # Try to use the DOT code directly
                graph = graphviz.Source(dot_code)
                graph.render(outfile=output_path, cleanup=True)
                return output_path
            except Exception as e:
                # If there's an error with the DOT code, fall back to a simple diagram
                print(f"Error rendering DOT code: {e}")
                try:
                    graph = _create_fallback_diagram(description)
                    graph.render(outfile=output_path, cleanup=True)
                    return output_path
                except Exception as e2:
                    print(f"Error rendering fallback diagram: {e2}")
                    return _create_text_image(description, output_path)

        except Exception as e:
            # If there's an error with the LLM, fall back to a simple diagram
            print(f"Error generating DOT code: {e}")
            try:
                graph = _create_fallback_diagram(description)
                graph.render(outfile=output_path, cleanup=True)
                return output_path
            except Exception as e2:
                print(f"Error rendering fallback diagram: {e2}")
                return _create_text_image(description, output_path)

    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return _create_text_image(description, output_path)


def _create_text_image(description, output_path):
    """
    Create a simple text image when Graphviz is not available.

    Args:
        description (str): Description of the concept to visualize.
        output_path (str): Path to save the generated image.

    Returns:
        str: Path to the generated image.
    """
    # Create a simple image with text
    width, height = 800, 600
    background_color = (255, 255, 255)  # White
    text_color = (0, 0, 0)  # Black

    # Create a new image with white background
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Add a title
    title = f"Visualization of: {description}"
    draw.text((width/2, 50), title, fill=text_color, font=font, anchor="mm")

    # Add a message about Graphviz
    message = "Graphviz is not installed or not in PATH."
    draw.text((width/2, 100), message, fill=text_color, font=font, anchor="mm")

    # Add instructions
    instructions = [
        "To enable diagram generation:",
        "1. Install Graphviz from https://graphviz.org/download/",
        "2. Add Graphviz bin directory to your PATH",
        "3. Restart the application"
    ]

    y_position = 150
    for line in instructions:
        draw.text((width/2, y_position), line, fill=text_color, font=font, anchor="mm")
        y_position += 30

    # Add a description of the concept
    y_position = 300
    draw.text((width/2, y_position), "Concept Description:", fill=text_color, font=font, anchor="mm")
    y_position += 40

    # Wrap the description text
    wrapped_text = textwrap.wrap(description, width=60)
    for line in wrapped_text:
        draw.text((width/2, y_position), line, fill=text_color, font=font, anchor="mm")
        y_position += 30

    # Save the image
    img.save(output_path)

    return output_path

def _create_fallback_diagram(description):
    """
    Create a simple fallback diagram when the LLM-generated DOT code fails.

    Args:
        description (str): Description of the concept to visualize.

    Returns:
        graphviz.Digraph: A simple diagram.
    """
    # Create a simple diagram based on common CS concepts
    dot = graphviz.Digraph(comment=f'Visualization of: {description}')

    # Add nodes and edges based on keywords in the description
    description_lower = description.lower()

    if "neural network" in description_lower or "deep learning" in description_lower:
        # Create a simple neural network diagram
        dot.node('input', 'Input Layer')
        dot.node('hidden1', 'Hidden Layer 1')
        dot.node('hidden2', 'Hidden Layer 2')
        dot.node('output', 'Output Layer')

        dot.edge('input', 'hidden1')
        dot.edge('hidden1', 'hidden2')
        dot.edge('hidden2', 'output')

    elif "algorithm" in description_lower or "sorting" in description_lower:
        # Create a simple algorithm flowchart
        dot.node('start', 'Start')
        dot.node('input', 'Input Data')
        dot.node('process', 'Process Data')
        dot.node('decision', 'Decision')
        dot.node('output', 'Output Result')
        dot.node('end', 'End')

        dot.edge('start', 'input')
        dot.edge('input', 'process')
        dot.edge('process', 'decision')
        dot.edge('decision', 'output', label='Yes')
        dot.edge('decision', 'process', label='No')
        dot.edge('output', 'end')

    elif "data structure" in description_lower or "tree" in description_lower:
        # Create a simple tree diagram
        dot.node('root', 'Root')
        dot.node('left', 'Left Child')
        dot.node('right', 'Right Child')
        dot.node('left_left', 'Left Left')
        dot.node('left_right', 'Left Right')
        dot.node('right_left', 'Right Left')
        dot.node('right_right', 'Right Right')

        dot.edge('root', 'left')
        dot.edge('root', 'right')
        dot.edge('left', 'left_left')
        dot.edge('left', 'left_right')
        dot.edge('right', 'right_left')
        dot.edge('right', 'right_right')

    elif "quantum" in description_lower:
        # Create a simple quantum circuit diagram
        dot.node('q0', 'Qubit 0')
        dot.node('q1', 'Qubit 1')
        dot.node('h', 'H Gate')
        dot.node('cx', 'CNOT Gate')
        dot.node('m', 'Measurement')

        dot.edge('q0', 'h')
        dot.edge('h', 'cx')
        dot.edge('q1', 'cx')
        dot.edge('cx', 'm')

    else:
        # Generic concept diagram
        dot.node('concept', description)
        dot.node('component1', 'Component 1')
        dot.node('component2', 'Component 2')
        dot.node('component3', 'Component 3')

        dot.edge('concept', 'component1')
        dot.edge('concept', 'component2')
        dot.edge('concept', 'component3')
        dot.edge('component1', 'component2')
        dot.edge('component2', 'component3')
        dot.edge('component3', 'component1')

    return dot
