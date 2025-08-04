# 🚀 Quick Start Guide

Get SteamNoodles AI running in 5 minutes!

## ⚡ Super Fast Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
**Windows:**
```cmd
set OPENAI_API_KEY=your-key-here
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY=your-key-here
```

### 3. Run Demo
```bash
python main.py
```

## 🎯 File Structure to Create

Create these folders and files in your project directory:

```
steamnoodles-ai/
├── main.py
├── requirements.txt
├── demo.py
├── setup.py
├── .env.template
├── agents/
│   ├── __init__.py
│   ├── feedback_agent.py
│   └── visualization_agent.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── utils/
    ├── __init__.py
    └── data_generator.py
```

## 📋 Commands Summary

| Command | Description |
|---------|-------------|
| `python main.py` | Run full demo |
| `python main.py interactive` | Interactive mode |
| `python main.py feedback` | Test feedback agent only |
| `python main.py viz` | Test visualization agent only |
| `python demo.py` | Comprehensive demo |
| `python setup.py` | Automated setup |

## 🔧 Troubleshooting

**Problem:** `ModuleNotFoundError`
**Solution:** Run `pip install -r requirements.txt`

**Problem:** `API key not found`
**Solution:** Set `OPENAI_API_KEY` environment variable

**Problem:** `No visualizations`
**Solution:** Ensure `outputs/` directory exists

## ✅ Success Check

You should see:
- ✅ Sentiment analysis working
- ✅ Automated responses generated  
- ✅ Visualizations saved to `outputs/`
- ✅ Sample data in `data/restaurant_reviews.csv`

## 🎉 You're Ready!

The system is now ready for production use!