# SteamNoodles Multi-Agent Framework

A sophisticated AI-powered system for analyzing customer feedback and generating automated responses with sentiment visualization capabilities.

## Developer details

Name: Naveen Dilhan Wickramasinghe
University: NSBM Green University

## 🚀 Features

### Agent 1: Customer Feedback Response Agent
- **Sentiment Analysis**: Automatically classifies customer reviews as positive, negative, or neutral
- **Automated Responses**: Generates personalized, context-aware replies to customer feedback
- **Batch Processing**: Can handle multiple reviews simultaneously

### Agent 2: Sentiment Visualization Agent  
- **Natural Language Queries**: Accepts date range queries like "last 7 days" or "past month"
- **Dynamic Visualizations**: Creates line plots and bar charts showing sentiment trends
- **Multi-format Support**: Generates both trend lines and stacked bar charts

## 📋 Prerequisites

- Python 3.11.9 (tested version)
- OpenAI API Key
- Visual Studio Code (recommended)

## 🛠️ Installation

### 1. Clone or Download the Project
```bash
# Create project directory
mkdir steamnoodles-ai
cd steamnoodles-ai
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

**Option 1: Environment Variable (Recommended)**
```bash
# Windows
set OPENAI_API_KEY=your-api-key-here

# macOS/Linux
export OPENAI_API_KEY=your-api-key-here
```

**Option 2: .env File**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

**Option 3: Direct Configuration**
Edit `config/settings.py` and add your API key:
```python
OPENAI_API_KEY = 'your-api-key-here'
```

## 📁 Project Structure

```
steamnoodles-ai/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .env                      # Environment variables (create this)
├── agents/
│   ├── __init__.py
│   ├── feedback_agent.py     # Feedback Response Agent
│   └── visualization_agent.py # Sentiment Visualization Agent
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration settings
├── utils/
│   ├── __init__.py
│   └── data_generator.py     # Sample data generator
├── data/
│   └── restaurant_reviews.csv # Generated sample data
└── outputs/
    └── sentiment_analysis_*.png # Generated visualizations
```

## 🚀 Usage

### Quick Start (Full Demo)
```bash
python main.py
```

### Interactive Mode
```bash
python main.py interactive
```

### Test Individual Agents
```bash
# Test only Feedback Response Agent
python main.py feedback

# Test only Sentiment Visualization Agent  
python main.py viz

# Run complete demo
python main.py demo
```

## 🧪 Testing Each Agent

### 1. Feedback Response Agent

**Sample Input:**
```python
review = "The food was absolutely amazing! The noodles were perfectly cooked and the service was outstanding."
```

**Expected Output:**
```python
{
    "sentiment": "positive",
    "reply": "Thank you so much for your wonderful feedback! We're thrilled to hear you enjoyed our noodles and service. We look forward to welcoming you back soon!"
}
```

### 2. Sentiment Visualization Agent

**Sample Queries:**
- `"Show sentiment trends for the last 7 days"`
- `"Generate a plot for the past 2 weeks"`
- `"Create visualization for the last month"`
- `"Show me sentiment analysis for last 3 days"`

**Expected Output:**
- Generated PNG file in `outputs/` directory
- Console message: `"✓ Visualization saved to: outputs/sentiment_analysis_20241203_143022.png"`

## 📊 Sample Data

The system automatically generates realistic sample data including:
- **200+ restaurant reviews** spanning 30 days
- **Realistic sentiment distribution**: 50% positive, 30% negative, 20% neutral
- **Varied review content** covering food quality, service, and ambiance
- **Date-time stamps** for trend analysis

## 🎯 Example Outputs

### Feedback Response Examples

**Positive Review:**
```
Input: "Amazing food and excellent service! Will definitely come back!"
Sentiment: positive
Reply: "Thank you so much for your wonderful review! We're delighted you enjoyed your experience and look forward to serving you again soon!"
```

**Negative Review:**
```
Input: "The noodles were cold and the service was terrible. Very disappointed."
Sentiment: negative  
Reply: "We sincerely apologize for your disappointing experience. This is not the standard we strive for. Please contact our manager so we can make this right."
```

**Neutral Review:**
```
Input: "Food was okay, nothing special but not bad either."
Sentiment: neutral
Reply: "Thank you for your feedback. We appreciate you taking the time to review us and hope to exceed your expectations on your next visit!"
```

### Visualization Examples

The system generates comprehensive charts showing:
- **Line plots**: Sentiment trends over time
- **Stacked bar charts**: Daily sentiment distribution
- **Multiple metrics**: Total reviews, daily breakdowns, percentage distributions

## 🔧 Customization

### Modify Response Templates
Edit `agents/feedback_agent.py` to customize automated responses:
```python
# Update the prompt template in FeedbackResponseAgent.__init__()
```

### Adjust Visualization Styles
Edit `agents/visualization_agent.py` to change chart appearance:
```python
# Modify matplotlib/seaborn styling options
plt.style.use('your-preferred-style')
```

### Change Data Generation
Edit `utils/data_generator.py` to modify sample data:
```python
# Adjust review content, date ranges, sentiment distributions
```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Found**
```
ERROR: OpenAI API key not found!
```
**Solution**: Set your OpenAI API key using one of the methods in step 4 of installation.

**2. Import Errors**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

**3. No Visualizations Generated**
```
No data found for date range
```
**Solution**: Run the data generator first: `python utils/data_generator.py`

**4. Permission Errors**
```
PermissionError: [Errno 13] Permission denied: 'outputs/'
```
**Solution**: Ensure the script has write permissions to create the `outputs/` directory.

### Debug Mode

Enable verbose logging by editing `config/settings.py`:
```python
AGENT_VERBOSE = True
```

## 📈 Performance Notes

- **Response Time**: Feedback analysis typically takes 2-3 seconds per review
- **Visualization Generation**: Chart creation takes 5-10 seconds depending on data size
- **Batch Processing**: Can handle 50+ reviews efficiently in batch mode
- **Memory Usage**: Moderate memory usage, suitable for datasets up to 10,000 reviews

## 🔒 Security Notes

- **API Key Protection**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files for local development
- **Data Privacy**: Sample data is generated locally and contains no real customer information

## 🚀 Advanced Usage

### Custom Date Ranges
```python
from agents.visualization_agent import SentimentVisualizationAgent

agent = SentimentVisualizationAgent('data/restaurant_reviews.csv')
plot_path = agent.generate_visualization("Show trends from December 1 to December 15")
```

### Batch Feedback Processing
```python
from agents.feedback_agent import FeedbackResponseAgent

agent = FeedbackResponseAgent()
reviews = ["Review 1", "Review 2", "Review 3"]
results = agent.batch_process(reviews)
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error messages carefully
3. Ensure all dependencies are properly installed
4. Verify your OpenAI API key is valid and has sufficient credits

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🎉 Getting Started Checklist

- [ ] Python 3.11.9 installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed via `pip install -r requirements.txt`
- [ ] OpenAI API key configured
- [ ] Project structure created
- [ ] Run `python main.py` successfully
- [ ] Generated sample visualizations in `outputs/` directory

