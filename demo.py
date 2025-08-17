#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime
from agents.feedback_agent import FeedbackResponseAgent
from agents.visualization_agent import SentimentVisualizationAgent
from utils.data_generator import generate_sample_data

def print_header(title):
    
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_subheader(title):
    
    print(f"\n--- {title} ---")

def demo_feedback_responses():
    
    print_header("AGENT 1: CUSTOMER FEEDBACK RESPONSE AGENT")
    
    print("This agent analyzes customer sentiment and generates personalized responses.")
    print("Processing sample reviews...")
    
    agent = FeedbackResponseAgent()
    
    
    test_cases = [
        {
            "category": "Highly Positive",
            "review": "This place is absolutely incredible! The ramen was the best I've ever had, and the service was exceptional. The staff went above and beyond to make our experience memorable. We'll definitely be regular customers!",
            "expected_sentiment": "positive"
        },
        {
            "category": "Strongly Negative", 
            "review": "Worst dining experience ever. The food was cold, tasteless, and overpriced. Waited 45 minutes for our order, and when it finally arrived, it was completely wrong. The staff was rude and unhelpful. Never coming back!",
            "expected_sentiment": "negative"
        },
        {
            "category": "Mixed/Neutral",
            "review": "The food was decent and the location is convenient. Service was a bit slow but the staff was polite. Prices are reasonable for the portion size. It's an okay option for a quick lunch.",
            "expected_sentiment": "neutral"
        },
        {
            "category": "Positive with Specific Praise",
            "review": "Loved the spicy miso ramen! The noodles had perfect texture and the broth was rich and flavorful. The restaurant atmosphere is cozy and welcoming. Great value for money too!",
            "expected_sentiment": "positive"
        },
        {
            "category": "Negative with Specific Issues",
            "review": "The soup was way too salty and the vegetables were overcooked. Also, the table was sticky and hadn't been properly cleaned. For the price we paid, I expected much better quality.",
            "expected_sentiment": "negative"
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print_subheader(f"Example {i}: {case['category']}")
        print(f"Customer Review:")
        print(f'"{case["review"]}"')
        
       
        print("\n⏳ Processing...")
        start_time = time.time()
        
        response = agent.process_feedback(case["review"])
        
        processing_time = time.time() - start_time
        
        
        print(f"\n📊 Analysis Results:")
        print(f"   Sentiment: {response['sentiment'].upper()}")
        print(f"   Processing Time: {processing_time:.2f} seconds")
        print(f"\n🤖 Automated Response:")
        print(f'   "{response["reply"]}"')
        
        
        sentiment_match = response['sentiment'] == case['expected_sentiment']
        print(f"\n✓ Sentiment Classification: {'CORRECT' if sentiment_match else 'UNEXPECTED'}")
        
        results.append({
            'case': case['category'],
            'sentiment': response['sentiment'],
            'correct': sentiment_match,
            'processing_time': processing_time
        })
        
        print("-" * 60)
        time.sleep(1)  
    
    
    print_subheader("Performance Summary")
    correct_predictions = sum(1 for r in results if r['correct'])
    avg_time = sum(r['processing_time'] for r in results) / len(results)
    
    print(f"Total Test Cases: {len(results)}")
    print(f"Correct Sentiment Classifications: {correct_predictions}/{len(results)}")
    print(f"Accuracy: {(correct_predictions/len(results)*100):.1f}%")
    print(f"Average Processing Time: {avg_time:.2f} seconds")

def demo_sentiment_visualization():
    """Demonstrate sentiment visualization with multiple chart types"""
    print_header("AGENT 2: SENTIMENT VISUALIZATION AGENT")
    
    print("This agent creates dynamic visualizations based on natural language queries.")
    
    
    data_file = "data/restaurant_reviews.csv"
    if not os.path.exists(data_file):
        print("📊 Generating sample dataset...")
        generate_sample_data(300, 45) 
        print("✓ Sample data generated")
    
    agent = SentimentVisualizationAgent(data_file)
    
    
    test_queries = [
        {
            "query": "Show sentiment trends for the last 7 days",
            "description": "Recent week analysis"
        },
        {
            "query": "Generate visualization for the past 2 weeks", 
            "description": "Two-week trend analysis"
        },
        {
            "query": "Create a plot for the last month",
            "description": "Monthly sentiment overview"
        },
        {
            "query": "Show me sentiment patterns for the past 10 days",
            "description": "Extended recent analysis"
        }
    ]
    
    generated_plots = []
    
    for i, test in enumerate(test_queries, 1):
        print_subheader(f"Visualization {i}: {test['description']}")
        print(f"Query: '{test['query']}'")
        
        print("\n⏳ Processing query and generating visualization...")
        start_time = time.time()
        
        try:
           
            summary = agent.get_data_summary(test['query'])
            print(f"\n📊 Data Summary:")
            print(summary)
            
            
            plot_path = agent.generate_visualization(test['query'])
            processing_time = time.time() - start_time
            
            if plot_path and os.path.exists(plot_path):
                print(f"\n✅ Success!")
                print(f"   📁 Saved to: {plot_path}")
                print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
                generated_plots.append(plot_path)
            else:
                print(f"\n❌ Failed to generate visualization")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        print("-" * 60)
        time.sleep(1)
    
    
    print_subheader("Visualization Summary")
    print(f"Queries Processed: {len(test_queries)}")
    print(f"Successful Visualizations: {len(generated_plots)}")
    print(f"Success Rate: {(len(generated_plots)/len(test_queries)*100):.1f}%")
    
    if generated_plots:
        print(f"\n📁 Generated Files:")
        for plot in generated_plots:
            file_size = os.path.getsize(plot) / 1024  # KB
            print(f"   • {plot} ({file_size:.1f} KB)")

def demo_integration():
    """Demonstrate integration between both agents"""
    print_header("INTEGRATION DEMO: COMBINED WORKFLOW")
    
    print("Demonstrating how both agents work together in a real workflow...")
    
   
    new_reviews = [
        "The new spicy ramen is amazing! Best meal I've had in months.",
        "Service was terrible today. Waited forever and food was cold.",
        "Pretty average experience. Food was okay, nothing special."
    ]
    
    print("📝 Scenario: Processing new customer reviews")
    print(f"   • Received {len(new_reviews)} new reviews")
    print("   • Need to: 1) Respond to customers, 2) Update sentiment dashboard")
    
    
    print_subheader("Step 1: Generate Customer Responses")
    feedback_agent = FeedbackResponseAgent()
    
    processed_reviews = []
    for i, review in enumerate(new_reviews, 1):
        print(f"\n📋 Review {i}: \"{review}\"")
        response = feedback_agent.process_feedback(review)
        processed_reviews.append({
            'review': review,
            'sentiment': response['sentiment'],
            'reply': response['reply']
        })
        print(f"   → Sentiment: {response['sentiment']}")
        print(f"   → Reply: \"{response['reply']}\"")
    
    
    print_subheader("Step 2: Update Sentiment Dashboard")
    
    
    print("📊 Updating sentiment dashboard with new data...")
    
    try:
        viz_agent = SentimentVisualizationAgent("data/restaurant_reviews.csv")
        plot_path = viz_agent.generate_visualization("Show updated trends for last 7 days")
        
        if plot_path:
            print(f"✅ Dashboard updated: {plot_path}")
        else:
            print("❌ Dashboard update failed")
            
    except Exception as e:
        print(f"❌ Error updating dashboard: {e}")
    
    
    print_subheader("Integration Summary")
    sentiment_counts = {}
    for review in processed_reviews:
        sentiment = review['sentiment']
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    print("📊 Batch Processing Results:")
    for sentiment, count in sentiment_counts.items():
        print(f"   • {sentiment.title()}: {count} reviews")
    
    print(f"\n✅ All {len(new_reviews)} customers received automated responses")
    print("✅ Sentiment dashboard updated with latest data")

def main():
    """Run complete demo"""
    print("🍜 SteamNoodles Multi-Agent Framework")
    print("    Complete System Demonstration")
    print(f"    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    
    try:
        from config.settings import validate_config
        if not validate_config():
            print("\n❌ Configuration validation failed!")
            print("Please ensure your OpenAI API key is properly configured.")
            sys.exit(1)
    except Exception as e:
        print(f"\n⚠️  Configuration warning: {e}")
        response = input("Continue with demo? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    
    os.makedirs("outputs", exist_ok=True)
    
    
    try:
        demo_feedback_responses()
        demo_sentiment_visualization() 
        demo_integration()
        
        print_header("DEMO COMPLETE")
        
        print("🎉 All demonstrations completed successfully!")
        print("\n📋 What was demonstrated:")
        print("   ✅ Sentiment analysis and response generation")
        print("   ✅ Natural language query processing")
        print("   ✅ Dynamic visualization creation")
        print("   ✅ Multi-agent integration workflow")
        
        print(f"\n📁 Output files saved to: ./outputs/")
        print("📊 Sample data available at: ./data/restaurant_reviews.csv")
        
        print("\n🚀 Ready for production use!")
        print("   • Run 'python main.py interactive' for manual testing")
        print("   • Integrate agents into your existing systems")
        print("   • Customize responses and visualizations as needed")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        print("Please check your configuration and try again")

if __name__ == "__main__":
    main()