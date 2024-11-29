# 🚀 Quick Start Guide

Get your Multi-Agent RAG Travel Planner running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- CrewAI (agent framework)
- LangChain (RAG components)
- ChromaDB (vector database)
- OpenAI (LLM)

## Step 2: Set Up Environment

```bash
# Run setup script
python setup.py
```

This creates necessary directories and checks your installation.

## Step 3: Add Your OpenAI API Key

Edit the `.env` file:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

## Step 4: Test Individual Tools (Optional)

```bash
python test_tools.py
```

This tests each tool independently to make sure everything works.

## Step 5: Run the Planner!

```bash
python main.py
```

The system will:
1. Initialize all tools and agents
2. Process the sample travel request
3. Generate a complete itinerary
4. Save it to `travel_itinerary.md`

## 📝 Customize Your Request

Edit [main.py](main.py) around line 155:

```python
# Change this to test different requests
selected_request = user_requests[0]  # Try 0, 1, or 2

# Or add your own:
custom_request = """
Plan a 10-day adventure trip to Japan focusing on traditional culture
and modern technology. I want to visit Tokyo, Kyoto, and Osaka...
"""
```

## 🎯 What Happens When You Run It?

1. **Travel Manager** analyzes your request
2. **Flight Agent** searches for flights
3. **Accommodation Agent** finds hotels
4. **Activity Agent** discovers tours and experiences
5. **Logistics Agent** plans transportation
6. **Knowledge Agent** provides cultural tips (using RAG!)
7. **Itinerary Compiler** creates your final plan

## 📊 Expected Output

You'll see:
- Real-time agent thinking and collaboration in the console
- A complete day-by-day itinerary at the end
- A saved markdown file with all details

Example:
```
🌍 MULTI-AGENT RAG TRAVEL PLANNER
===============================================

🔧 Initializing tools...
✅ All tools initialized successfully

👥 Creating agent crew...
✅ Agents created successfully

🚀 Starting travel planning process...

[Agents work together...]

✅ TRAVEL PLANNING COMPLETE!

📄 FINAL ITINERARY:
[Your personalized travel plan]

💾 Itinerary saved to: travel_itinerary.md
```

## 🔧 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created `.env` file
- Add your actual API key (starts with `sk-`)

### "ModuleNotFoundError"
- Run: `pip install -r requirements.txt`

### ChromaDB Errors
- Delete `data/chroma_db/` folder
- Run the script again

## 🎓 Understanding the Code

### Key Files:

- **[main.py](main.py)** - Main orchestration, start here
- **[tools/](tools/)** - All custom tools (flights, hotels, RAG)
- **[agents/agents.py](agents/agents.py)** - Agent definitions
- **[agents/tasks.py](agents/tasks.py)** - Task definitions

### How RAG Works:

1. **Documents** in `data/travel_knowledge/` (auto-created)
2. **ChromaDB** creates vector embeddings
3. **Agents query** the knowledge base
4. **Relevant info** retrieved and used in planning

## 🚀 Next Steps

1. **Try different requests** - Edit main.py
2. **Add travel documents** - Put .txt files in `data/travel_knowledge/`
3. **Integrate real APIs** - Replace mock data in tools
4. **Customize agents** - Edit roles and backstories

## 💡 Pro Tips

- The more detailed your request, the better the itinerary
- Mention specific interests (food, history, art, adventure)
- Specify budget level for better recommendations
- Check the saved .md file for the complete formatted itinerary

## 📚 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review code comments in each file
- Visit CrewAI docs: https://docs.crewai.com/

---

**Ready to plan your next adventure?** 🌍✈️

Run: `python main.py`
