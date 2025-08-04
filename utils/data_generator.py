"""
Sample Data Generator
Generates realistic restaurant review data for testing
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_sample_data(num_reviews=200, days_back=30):
    """
    Generate sample restaurant review data
    
    Args:
        num_reviews (int): Number of reviews to generate
        days_back (int): Number of days back from today
        
    Returns:
        str: Path to generated CSV file
    """
    
    # Sample review texts categorized by sentiment
    positive_reviews = [
        "Absolutely amazing food! The noodles were perfectly cooked and the flavors were incredible.",
        "Outstanding service and delicious food. Will definitely be back!",
        "Best noodles in town! The staff was friendly and the atmosphere was great.",
        "Loved everything about this place. The portions were generous and the taste was fantastic.",
        "Excellent dining experience. The food arrived quickly and was still hot.",
        "Great value for money. The noodles were fresh and the service was top-notch.",
        "Amazing flavors! The chef really knows what they're doing.",
        "Perfect place for a quick lunch. The food is consistently good.",
        "Highly recommend the spicy noodles. The ambiance is also very nice.",
        "Fantastic restaurant! The staff was attentive and the food was delicious.",
        "The best noodle soup I've ever had. Coming back next week for sure!",
        "Great food, great service, great prices. What more could you ask for?",
        "The noodles were cooked to perfection. Loved the variety of toppings.",
        "Wonderful dining experience. The restaurant is clean and the food is fresh.",
        "Outstanding quality and fantastic taste. This place never disappoints!"
    ]
    
    negative_reviews = [
        "Terrible experience. The food was cold and the service was slow.",
        "Very disappointing. The noodles were overcooked and bland.",
        "Poor service and mediocre food. Won't be coming back.",
        "The food took forever to arrive and when it did, it was lukewarm.",
        "Expensive for what you get. The portions were small and tasteless.",
        "The restaurant was dirty and the staff seemed uninterested.",
        "Worst noodles I've ever had. The broth was too salty.",
        "Terrible customer service. The waiters were rude and inattentive.",
        "The food was greasy and unappetizing. Very disappointing.",
        "Long wait times and mediocre food. Not worth the money.",
        "The noodles were mushy and the vegetables were wilted.",
        "Poor hygiene standards. The tables were dirty and sticky.",
        "Overpriced and underwhelming. The food lacked flavor completely.",
        "Bad experience overall. The food was cold and the service was terrible.",
        "Would not recommend. The quality has really gone downhill."
    ]
    
    neutral_reviews = [
        "The food was okay, nothing special but not bad either.",
        "Average experience. The noodles were decent and the service was fine.",
        "It's an okay place for a quick meal. Nothing outstanding though.",
        "The food was alright. Service could be better but it's acceptable.",
        "Decent noodles but nothing to write home about.",
        "Average restaurant with average food. It's fine for a casual meal.",
        "The food was satisfactory. Not great, not terrible.",
        "It's an okay place. The noodles were decent and the price was fair.",
        "Nothing special but gets the job done. Food was okay.",
        "The service was average and the food was standard.",
        "Decent place for lunch. The noodles were okay, nothing more.",
        "It's fine. Not the best I've had but not the worst either.",
        "Average food and service. It's an okay option in the area.",
        "The noodles were decent. Nothing exceptional but edible.",
        "Fair enough. The food was okay and the staff was polite."
    ]
    
    # Generate random reviews
    reviews_data = []
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    
    for i in range(num_reviews):
        # Random date within range
        random_days = random.randint(0, days_back)
        review_date = start_date + timedelta(days=random_days)
        
        # Random sentiment distribution (more realistic)
        sentiment_choice = random.choices(
            ['positive', 'negative', 'neutral'],
            weights=[0.5, 0.3, 0.2],  # 50% positive, 30% negative, 20% neutral
            k=1
        )[0]
        
        # Select review text based on sentiment
        if sentiment_choice == 'positive':
            review_text = random.choice(positive_reviews)
        elif sentiment_choice == 'negative':
            review_text = random.choice(negative_reviews)
        else:
            review_text = random.choice(neutral_reviews)
        
        # Add some variation to reviews
        variations = [
            " The restaurant atmosphere was pleasant.",
            " Staff was professional.",
            " Good location and easy to find.",
            " Parking was convenient.",
            " Clean restrooms.",
            " Music was at a good volume.",
            ""
        ]
        
        if random.random() < 0.3:  # 30% chance to add variation
            review_text += random.choice(variations)
        
        reviews_data.append({
            'date': review_date,
            'review_text': review_text,
            'sentiment': sentiment_choice,
            'review_id': f'R{i+1:04d}',
            'customer_id': f'C{random.randint(1000, 9999)}'
        })
    
    # Create DataFrame
    df = pd.DataFrame(reviews_data)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    csv_path = 'data/restaurant_reviews.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"Generated {num_reviews} sample reviews")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Sentiment distribution:")
    print(df['sentiment'].value_counts())
    print(f"Data saved to: {csv_path}")
    
    return csv_path

def add_more_reviews(additional_reviews=50):
    """Add more reviews to existing dataset"""
    csv_path = 'data/restaurant_reviews.csv'
    
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        existing_count = len(existing_df)
        
        # Generate additional reviews
        generate_sample_data(existing_count + additional_reviews, days_back=45)
        print(f"Added {additional_reviews} more reviews to existing dataset")
    else:
        print("No existing dataset found. Generating new dataset...")
        generate_sample_data(additional_reviews)

if __name__ == "__main__":
    # Generate sample data when run directly
    generate_sample_data()