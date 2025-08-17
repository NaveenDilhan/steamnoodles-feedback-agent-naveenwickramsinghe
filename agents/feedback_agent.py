from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
import json
import re

class SentimentResponseParser(BaseOutputParser):
    """Custom parser for sentiment analysis and response generation"""
    
    def parse(self, text: str) -> dict:
        """Parse LLM output to extract sentiment and response"""
        try:
            
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            
            sentiment_match = re.search(r'sentiment["\s]*:["\s]*([^",\n]+)', text, re.IGNORECASE)
            response_match = re.search(r'response["\s]*:["\s]*([^",\n]+)', text, re.IGNORECASE)
            
            sentiment = sentiment_match.group(1).strip().lower() if sentiment_match else "neutral"
            response_text = response_match.group(1).strip() if response_match else "Thank you for your feedback!"
            
            
            if "positive" in sentiment or "good" in sentiment or "great" in sentiment:
                sentiment = "positive"
            elif "negative" in sentiment or "bad" in sentiment or "poor" in sentiment:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "response": response_text
            }
            
        except Exception as e:
            print(f"Parsing error: {e}")
            return {
                "sentiment": "neutral",
                "response": "Thank you for your feedback. We appreciate your input!"
            }

class FeedbackResponseAgent:
    """Agent for processing customer feedback and generating responses"""
    
    def __init__(self, temperature=0.7):
        """Initialize the feedback response agent"""
        self.llm = OpenAI(temperature=temperature, max_tokens=200)
        self.parser = SentimentResponseParser()
        
        
        self.prompt_template = PromptTemplate(
            input_variables=["feedback"],
            template="""
You are a customer service AI for SteamNoodles restaurant. Analyze the customer feedback and provide:
1. Sentiment classification (positive, negative, or neutral)
2. A professional, empathetic response

Customer Feedback: "{feedback}"

Please respond in this exact JSON format:
{{
    "sentiment": "positive/negative/neutral",
    "response": "Your professional response here"
}}

Guidelines for responses:
- For POSITIVE feedback: Thank them warmly, express appreciation, invite them back
- For NEGATIVE feedback: Apologize sincerely, acknowledge concerns, offer to make it right
- For NEUTRAL feedback: Thank them politely, encourage future visits

Keep responses concise (1-2 sentences), professional, and personalized to their specific feedback.
            """
        )
        
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            output_parser=self.parser
        )
    
    def process_feedback(self, feedback_text: str) -> dict:
        """
        Process customer feedback and generate automated response
        
        Args:
            feedback_text (str): Customer feedback text
            
        Returns:
            dict: Contains sentiment and automated reply
        """
        try:
            if not feedback_text.strip():
                return {
                    "sentiment": "neutral",
                    "reply": "Thank you for taking the time to provide feedback!"
                }
            
            
            result = self.chain.run(feedback=feedback_text)
            
            # Ensure we have the expected format
            if isinstance(result, dict):
                return {
                    "sentiment": result.get("sentiment", "neutral"),
                    "reply": result.get("response", "Thank you for your feedback!")
                }
            else:
                return {
                    "sentiment": "neutral",
                    "reply": str(result)
                }
                
        except Exception as e:
            print(f"Error processing feedback: {e}")
            return {
                "sentiment": "neutral",
                "reply": "Thank you for your feedback. We appreciate your input and will use it to improve our service!"
            }
    
    def batch_process(self, feedback_list: list) -> list:
        """
        Process multiple feedback entries at once
        
        Args:
            feedback_list (list): List of feedback texts
            
        Returns:
            list: List of processed results
        """
        results = []
        for feedback in feedback_list:
            result = self.process_feedback(feedback)
            results.append({
                "original_feedback": feedback,
                "sentiment": result["sentiment"],
                "reply": result["reply"]
            })
        return results


if __name__ == "__main__":
    
    agent = FeedbackResponseAgent()
    
    test_reviews = [
        "Amazing food and excellent service! Will definitely come back!",
        "The noodles were cold and the service was terrible. Very disappointed.",
        "Food was okay, nothing special but not bad either."
    ]
    
    for review in test_reviews:
        print(f"Review: {review}")
        response = agent.process_feedback(review)
        print(f"Sentiment: {response['sentiment']}")
        print(f"Reply: {response['reply']}")
        print("-" * 50)