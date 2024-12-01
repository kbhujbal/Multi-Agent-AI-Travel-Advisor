# 🌍 Multi-Agent RAG Travel Planner

## 👋 Welcome!

You have a **complete, production-ready Multi-Agent AI Travel Planning System** using CrewAI, RAG (Retrieval-Augmented Generation), and custom tool-calling.

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 3. Run the travel planner
python main.py
```

That's it! The system will generate a complete travel itinerary.

## 📚 Documentation Guide

### Choose Your Path:

#### 🚀 **I want to get started RIGHT NOW**
→ Read: [QUICKSTART.md](QUICKSTART.md) (5 minutes)

#### 📖 **I want to understand the complete system**
→ Read: [README.md](README.md) (20 minutes)

#### 🏗️ **I want to understand the architecture**
→ Read: [ARCHITECTURE.md](ARCHITECTURE.md) (15 minutes)

#### 📋 **I want a high-level overview**
→ Read: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) (10 minutes)

#### 📁 **I want to understand the file structure**
→ Read: [FILE_STRUCTURE.md](FILE_STRUCTURE.md) (5 minutes)

## 🎯 What This System Does

**Input:**
```
"Plan a 10-day luxury honeymoon to Italy focusing on food and history.
We want to visit Rome and Florence, staying in 5-star hotels."
```

**Output:**
- ✅ Complete day-by-day itinerary
- ✅ Flight options with prices
- ✅ Hotel recommendations
- ✅ Activities and tours matched to interests
- ✅ Transportation logistics
- ✅ Cultural tips and advice
- ✅ Budget breakdown
- ✅ Pre-trip checklist

## 🤖 How It Works

**7 AI Agents Collaborate:**

1. **Travel Manager** - Analyzes your request
2. **Flight Agent** - Finds best flights
3. **Hotel Agent** - Finds perfect accommodations
4. **Activity Agent** - Curates experiences
5. **Logistics Agent** - Plans transportation
6. **Knowledge Agent** - Provides travel advice (using RAG!)
7. **Compiler Agent** - Creates final itinerary

**Technologies:**
- 🧠 **CrewAI** - Multi-agent orchestration
- 📚 **RAG** - ChromaDB vector database for knowledge retrieval
- 🛠️ **Custom Tools** - Flight, hotel, activity search
- 🤖 **OpenAI GPT-4** - Powering the agents

## 📁 Project Structure

```
Multi Agent AI Travel Agent/
│
├── main.py                    ⭐ Run this file
├── agents/                    🤖 7 specialized agents
├── tools/                     🛠️ Custom tools (flights, hotels, RAG)
├── data/travel_knowledge/     📖 Travel documents for RAG
│
├── START_HERE.md             👈 You are here
├── QUICKSTART.md             🚀 5-minute guide
├── README.md                 📖 Complete documentation
├── ARCHITECTURE.md           🏗️ System architecture
├── PROJECT_SUMMARY.md        📋 Project overview
└── FILE_STRUCTURE.md         📁 File tree explained
```

## 🎓 Learning Path

### Beginner (First Time)

1. Read this file (you're doing it!)
2. Read [QUICKSTART.md](QUICKSTART.md)
3. Run `python main.py`
4. See the magic happen!
5. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### Intermediate (Ready to Customize)

1. Read [README.md](README.md)
2. Try different travel requests
3. Add your own travel documents to `data/travel_knowledge/`
4. Modify agents in [agents/agents.py](agents/agents.py)
5. Run `python test_tools.py` to test components

### Advanced (Ready to Build)

1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Study the tool implementations in [tools/](tools/)
3. Integrate real APIs (Amadeus, Booking.com, etc.)
4. Add new agents and capabilities
5. Build a web interface

## 🔑 Prerequisites

- **Python 3.8+**
- **OpenAI API Key** (get from https://platform.openai.com/)

That's all you need!

## 💡 Example Use Cases

### 1. Luxury Honeymoon
```
"Plan a 10-day luxury honeymoon to Italy focusing on food and history"
```

### 2. Solo Art Trip
```
"5-day trip to Paris for a solo traveler who loves art and food"
```

### 3. Family Vacation
```
"7-day family trip to Barcelona with kids - culture and beaches"
```

### 4. Your Custom Trip
```
Edit main.py and add your own request!
```

## 🛠️ What's Included

### ✅ Complete System
- 7 specialized AI agents
- 4 custom tools (3 API + 1 RAG)
- Sequential workflow orchestration
- ChromaDB vector database
- Sample travel knowledge base

### ✅ Production-Ready Code
- Modular architecture
- Type hints with Pydantic
- Error handling structure
- Comprehensive documentation
- Easy to extend and customize

### ✅ Mock Data (Ready for APIs)
- Flight search returns realistic mock data
- Hotel search returns realistic mock data
- Activity search returns realistic mock data
- **Easy to swap with real APIs** (Amadeus, Booking.com, etc.)

## 🚀 Next Steps After First Run

1. **Experiment with requests**
   - Change destinations
   - Try different durations
   - Vary budget levels
   - Test different interests

2. **Add your knowledge**
   - Create `.txt` files in `data/travel_knowledge/`
   - Add destination guides
   - Include travel tips
   - RAG automatically indexes them!

3. **Customize agents**
   - Edit personas in [agents/agents.py](agents/agents.py)
   - Adjust goals and backstories
   - See how it changes the output

4. **Integrate real APIs**
   - Replace mock data in [tools/](tools/)
   - Use Amadeus for flights
   - Use Booking.com for hotels
   - Use GetYourGuide for activities

## 📊 System Capabilities

| Feature | Status |
|---------|--------|
| Multi-Agent Orchestration | ✅ Complete |
| RAG with Vector Database | ✅ Complete |
| Custom Tool-Calling | ✅ Complete |
| Natural Language Input | ✅ Complete |
| Day-by-Day Itineraries | ✅ Complete |
| Mock API Data | ✅ Complete |
| Production API Integration | 🔧 Ready (swap mock data) |
| Web Interface | 🔮 Future (add Streamlit/Flask) |

## 🎯 Success Criteria

You'll know it's working when:
1. ✅ You run `python main.py`
2. ✅ You see agents collaborating in the console
3. ✅ You get a complete itinerary at the end
4. ✅ A file `travel_itinerary.md` is created

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not found"
**Solution:** Create `.env` file with your API key

### Error: "ModuleNotFoundError"
**Solution:** Run `pip install -r requirements.txt`

### ChromaDB Issues
**Solution:** Delete `data/chroma_db/` folder and run again

### More help?
→ See [README.md](README.md) Troubleshooting section

## 💰 Cost

**Approximate cost per itinerary:** $0.50-$1.00 (OpenAI API)

This includes:
- GPT-4 calls for all 7 agents
- Embeddings for RAG queries
- Full day-by-day itinerary generation

## 🎉 What Makes This Special

1. **Multi-Agent**: Agents with different specializations collaborate
2. **RAG**: Real knowledge retrieval, not just LLM training data
3. **Tool-Calling**: Agents can search flights, hotels, activities
4. **Production-Ready**: Clean code, modular, well-documented
5. **Extensible**: Easy to add agents, tools, and capabilities

## 📞 Support

- Check documentation files
- Review code comments
- Visit CrewAI docs: https://docs.crewai.com/
- LangChain RAG: https://python.langchain.com/docs/use_cases/question_answering/

## 🏆 You're Ready!

You have everything you need:
- ✅ Complete codebase
- ✅ Comprehensive documentation
- ✅ Example use cases
- ✅ Extension guide

**Now go plan some amazing trips!** 🌍✈️🎉

---

## 🗺️ Documentation Map

```
START_HERE.md (this file)
    ↓
    ├─→ Quick Start → QUICKSTART.md
    ├─→ Full Guide → README.md
    ├─→ Architecture → ARCHITECTURE.md
    ├─→ Overview → PROJECT_SUMMARY.md
    └─→ File Tree → FILE_STRUCTURE.md
```

**Choose your path and dive in!**

### For the Impatient:
```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key" > .env
python main.py
```

### For the Thorough:
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Read [README.md](README.md)
3. Read [ARCHITECTURE.md](ARCHITECTURE.md)

### For the Visual Learner:
1. Check [FILE_STRUCTURE.md](FILE_STRUCTURE.md)
2. Open [main.py](main.py) and read through
3. Explore [agents/agents.py](agents/agents.py)

**Happy travels!** 🚀
