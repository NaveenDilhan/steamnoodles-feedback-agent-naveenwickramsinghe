"""
Sentiment Visualization Agent
Generates visualizations of sentiment trends based on user queries.
"""

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain import hub
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import re
import os


class DateRangeParser:
    """Utility class to parse natural language date ranges"""

    @staticmethod
    def parse_date_range(query: str) -> tuple:
        query_lower = query.lower()
        today = datetime.now().date()

        # Handle common phrases like "last 7 days", "past 2 weeks", etc.
        if "last" in query_lower or "past" in query_lower:
            numbers = re.findall(r'\d+', query)
            if numbers:
                days = int(numbers[0])
                if "week" in query_lower:
                    days *= 7
                elif "month" in query_lower:
                    days *= 30
                elif "year" in query_lower:
                    days *= 365
                start_date = today - timedelta(days=days)
                return start_date, today

        # Default: past 7 days
        return today - timedelta(days=7), today


class DataAnalysisTool:
    """Tool for analyzing sentiment data"""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.df = None
        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file)
            self.df['date'] = pd.to_datetime(self.df['date']).dt.date
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def run(self, query: str) -> str:
        try:
            start_date, end_date = DateRangeParser.parse_date_range(query)
            mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
            filtered_df = self.df[mask]

            if filtered_df.empty:
                return f"No data found for date range {start_date} to {end_date}"

            daily_sentiment = filtered_df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)

            result = f"Date range: {start_date} to {end_date}\n"
            result += f"Total reviews: {len(filtered_df)}\n"
            result += f"Daily sentiment breakdown:\n{daily_sentiment.to_string()}"
            return result

        except Exception as e:
            return f"Error analyzing data: {str(e)}"


class VisualizationTool:
    """Tool for creating sentiment visualizations"""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.df = None
        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file)
            self.df['date'] = pd.to_datetime(self.df['date']).dt.date
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def run(self, query: str) -> str:
        try:
            start_date, end_date = DateRangeParser.parse_date_range(query)
            mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
            filtered_df = self.df[mask]

            if filtered_df.empty:
                return f"No data found for date range {start_date} to {end_date}"

            plt.figure(figsize=(12, 8))
            daily_sentiment = filtered_df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

            daily_sentiment.plot(kind='line', ax=ax1, marker='o')
            ax1.set_title(f'Sentiment Trends Over Time ({start_date} to {end_date})')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Number of Reviews')
            ax1.legend(title='Sentiment')
            ax1.grid(True, alpha=0.3)

            daily_sentiment.plot(kind='bar', stacked=True, ax=ax2)
            ax2.set_title('Daily Sentiment Distribution')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Number of Reviews')
            ax2.legend(title='Sentiment')
            ax2.tick_params(axis='x', rotation=45)

            plt.tight_layout()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sentiment_analysis_{timestamp}.png"
            filepath = os.path.join("outputs", filename)
            os.makedirs("outputs", exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            return f"Visualization saved to {filepath}"

        except Exception as e:
            return f"Error creating visualization: {str(e)}"


class SentimentVisualizationAgent:
    """Agent for generating sentiment visualizations based on natural language queries"""

    def __init__(self, data_file: str, temperature=0.1):
        self.data_file = data_file
        self.llm = OpenAI(temperature=temperature, max_tokens=1000)

        self.data_tool = DataAnalysisTool(data_file)
        self.viz_tool = VisualizationTool(data_file)

        self.tools = [
            Tool(
                name="analyze_data",
                func=self.data_tool.run,
                description="Analyze sentiment data for a given date range"
            ),
            Tool(
                name="create_plot",
                func=self.viz_tool.run,
                description="Create and save sentiment visualization plots"
            )
        ]

        try:
            prompt = hub.pull("hwchase17/react")
        except Exception:
            prompt = PromptTemplate(
                input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
                template="""
You are a data visualization assistant for SteamNoodles restaurant.
Your job is to analyze sentiment data and create visualizations based on user queries.

You have access to these tools:
{tools}

Tool names: {tool_names}

Always follow this format:
Question: the input question
Thought: think about what you need to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}
                """
            )

        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=3
        )

    def generate_visualization(self, query: str) -> str:
        try:
            enhanced_query = f"Create a sentiment visualization for: {query}"
            result = self.agent_executor.invoke({"input": enhanced_query})

            output = result['output'] if isinstance(result, dict) and 'output' in result else str(result)

            file_pattern = r'outputs/sentiment_analysis_\d+_\d+\.png'
            match = re.search(file_pattern, output)

            if match:
                return match.group()
            else:
                return self.viz_tool.run(query)

        except Exception as e:
            print(f"Agent execution failed: {e}")
            return self.viz_tool.run(query)

    def get_data_summary(self, query: str) -> str:
        return self.data_tool.run(query)


# Example usage and testing
if __name__ == "__main__":
    data_file = "../data/restaurant_reviews.csv"

    if os.path.exists(data_file):
        agent = SentimentVisualizationAgent(data_file)

        test_queries = [
            "Show sentiment for last 7 days",
            "Create plot for past 2 weeks",
            "Visualize last month trends"
        ]

        for query in test_queries:
            print(f"Query: {query}")
            try:
                result = agent.generate_visualization(query)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")
            print("-" * 50)
    else:
        print(f"Data file not found: {data_file}")
