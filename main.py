#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from agents.feedback_agent import FeedbackResponseAgent
from agents.visualization_agent import SentimentVisualizationAgent
from utils.data_generator import generate_sample_data
from config.settings import OPENAI_API_KEY

def setup_environment():
    
    if not OPENAI_API_KEY:
        print("ERROR: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in config/settings.py or as an environment variable")
        sys.exit(1)
    
    # Set the API key for OpenAI
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    print("✓ Environment setup complete")

def demo_feedback_agent():
    
    print("\n" + "="*50)
    print("DEMO: FEEDBACK RESPONSE AGENT")
    print("="*50)
    
    agent = FeedbackResponseAgent()
    
    # Sample feedback examples
    sample_reviews = [
        "The food was absolutely amazing! The noodles were perfectly cooked and the service was outstanding. Will definitely come back!",
        "Terrible experience. The food was cold, service was slow, and the restaurant was dirty. Very disappointed.",
        "The food was okay, nothing special. Service was average. Might try again sometime.",
        "Love this place! Best noodles in town and such friendly staff. Highly recommend!",
        "Food took forever to arrive and when it did, it was lukewarm. The server seemed annoyed when I asked about the delay."
    ]
    
    for i, review in enumerate(sample_reviews, 1):
        print(f"\n--- Sample Review {i} ---")
        print(f"Customer Review: {review}")
        
        response = agent.process_feedback(review)
        print(f"Sentiment: {response['sentiment']}")
        print(f"Automated Reply: {response['reply']}")
        print("-" * 40)

def demo_visualization_agent():
    
    print("\n" + "="*50)
    print("DEMO: SENTIMENT VISUALIZATION AGENT")
    print("="*50)
    
    # Generate sample data if it doesn't exist
    data_file = "data/restaurant_reviews.csv"
    if not os.path.exists(data_file):
        print("Generating sample data...")
        generate_sample_data()
        print("✓ Sample data generated")
    
    agent = SentimentVisualizationAgent(data_file)
    
    # Demo different date range queries
    queries = [
        "Show sentiment trends for the last 7 days",
        "Generate a plot for the last 14 days",
        "Create visualization for the past month",
        "Show me sentiment analysis for last 3 days"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        try:
            plot_path = agent.generate_visualization(query)
            print(f"✓ Visualization saved to: {plot_path}")
        except Exception as e:
            print(f"✗ Error generating visualization: {str(e)}")

def interactive_mode():
    
    print("\n" + "="*50)
    print("INTERACTIVE MODE")
    print("="*50)
    print("1. Test Feedback Response Agent")
    print("2. Test Sentiment Visualization Agent")
    print("3. Exit")
    
    # Initialize agents
    feedback_agent = FeedbackResponseAgent()
    
    data_file = "data/restaurant_reviews.csv"
    if not os.path.exists(data_file):
        generate_sample_data()
    viz_agent = SentimentVisualizationAgent(data_file)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n--- Feedback Response Agent ---")
                review = input("Enter customer review: ").strip()
                if review:
                    response = feedback_agent.process_feedback(review)
                    print(f"\nSentiment: {response['sentiment']}")
                    print(f"Automated Reply: {response['reply']}")
                else:
                    print("Please enter a valid review.")
            
            elif choice == "2":
                print("\n--- Sentiment Visualization Agent ---")
                query = input("Enter date range query (e.g., 'last 7 days'): ").strip()
                if query:
                    try:
                        plot_path = viz_agent.generate_visualization(query)
                        print(f"✓ Visualization saved to: {plot_path}")
                    except Exception as e:
                        print(f"✗ Error: {str(e)}")
                else:
                    print("Please enter a valid query.")
            
            elif choice == "3":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    
    print("SteamNoodles Multi-Agent Framework")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "demo":
            demo_feedback_agent()
            demo_visualization_agent()
        elif mode == "interactive":
            interactive_mode()
        elif mode == "feedback":
            demo_feedback_agent()
        elif mode == "viz":
            demo_visualization_agent()
        else:
            print(f"Unknown mode: {mode}")
            print("Available modes: demo, interactive, feedback, viz")
    else:
        print("\nRunning full demo...")
        demo_feedback_agent()
        demo_visualization_agent()
        print("\n" + "="*50)
        print("Demo complete! Run with 'interactive' for manual testing:")
        print("python main.py interactive")

if __name__ == "__main__":
    main()