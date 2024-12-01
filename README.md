# 🌍 Multi-Agent RAG Travel Planner

A sophisticated AI travel planning system that uses multiple specialized agents working together to create comprehensive, personalized travel itineraries. Built with CrewAI and featuring RAG (Retrieval-Augmented Generation) for up-to-date travel information.

## 🎯 Features

- **Multi-Agent Architecture**: 7 specialized AI agents collaborate to plan your trip
- **RAG Implementation**: ChromaDB vector database for retrieving travel knowledge
- **Real-time Tools**: Flight, hotel, and activity search capabilities (mock APIs, ready for production integration)
- **Comprehensive Planning**: Covers flights, accommodations, activities, logistics, and cultural tips
- **Natural Language Input**: Describe your dream trip in plain English

## 🏗️ System Architecture

### Agents

1. **Travel Planning Manager** (Orchestrator)
   - Analyzes user requests and breaks them down
   - Coordinates all other agents
   - Ensures comprehensive coverage

2. **Flight Research Specialist**
   - Finds best flight options
   - Compares prices, durations, and layovers
   - Considers traveler preferences

3. **Accommodation Specialist**
   - Researches hotels and lodging
   - Matches properties to budget and preferences
   - Considers location and amenities

4. **Activities & Experiences Curator**
   - Finds tours, attractions, and experiences
   - Matches activities to interests
   - Balances must-see sights with hidden gems

5. **Travel Logistics Coordinator**
   - Plans ground transportation
   - Optimizes routes and timing
   - Handles practical details

6. **Travel Knowledge Expert**
   - Provides visa, cultural, and practical information
   - Uses RAG to access comprehensive travel database
   - Answers destination-specific questions

7. **Itinerary Compiler & Optimizer**
   - Synthesizes all research into final plan
   - Creates day-by-day itinerary
   - Ensures logical flow and optimal timing

### Communication Flow

```
User Request
     ↓
Travel Manager (analyzes & plans)
     ↓
   ┌─────────────────────────────────┐
   ↓         ↓         ↓         ↓         ↓
Flight   Hotels   Activities  Logistics  Knowledge
   ↓         ↓         ↓         ↓         ↓
   └─────────────────────────────────┘
                  ↓
        Itinerary Compiler
                  ↓
         Final Itinerary
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone or download this project**

```bash
cd "Multi Agent AI Travel Agent"
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment**

```bash
# Run setup script
python setup.py

# Edit .env file and add your API key
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the planner**

```bash
python main.py
```

## 📁 Project Structure

```
Multi Agent AI Travel Agent/
│
├── main.py                          # Main orchestration script
├── setup.py                         # Setup and initialization
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
│
├── agents/
│   ├── agents.py                   # Agent definitions
│   └── tasks.py                    # Task definitions
│
├── tools/
│   ├── flight_search_tool.py      # Flight search API tool
│   ├── hotel_search_tool.py       # Hotel search API tool
│   ├── activity_search_tool.py    # Activity search API tool
│   └── travel_knowledge_rag_tool.py # RAG tool with ChromaDB
│
└── data/
    ├── travel_knowledge/           # Travel documents for RAG
    └── chroma_db/                  # ChromaDB vector store
```

## 🛠️ How It Works

### 1. Tools (RAG + API)

#### Custom API Tools

Each tool follows the CrewAI `BaseTool` pattern:

```python
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class FlightSearchInput(BaseModel):
    origin: str = Field(..., description="Origin city")
    destination: str = Field(..., description="Destination city")
    # ... more fields

class FlightSearchTool(BaseTool):
    name: str = "Flight Search Tool"
    description: str = "Searches for flights..."
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(self, origin: str, destination: str, ...) -> str:
        # API call logic here (currently mocked)
        return formatted_results
```

#### RAG Tool with ChromaDB

```python
class TravelKnowledgeRAGTool(BaseTool):
    # Initializes ChromaDB vector store
    # Loads travel documents
    # Performs similarity search

    def _run(self, query: str, destination: str = None) -> str:
        results = self._vectorstore.similarity_search(query, k=3)
        return formatted_results
```

### 2. Agent Creation

```python
agent = Agent(
    role="Flight Research Specialist",
    goal="Find the best flight options...",
    backstory="You are a flight booking expert...",
    tools=[flight_search_tool],
    verbose=True,
    allow_delegation=False
)
```

### 3. Task Definition

```python
task = Task(
    description="Research and recommend flight options...",
    expected_output="Detailed flight recommendations...",
    agent=flight_agent,
    context=[planning_task]  # Use output from previous task
)
```

### 4. Crew Orchestration

```python
crew = Crew(
    agents=[manager, flight_agent, hotel_agent, ...],
    tasks=[planning_task, flight_task, hotel_task, ...],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()  # Execute the workflow
```

## 💡 Usage Examples

### Example 1: Luxury Honeymoon

```python
user_request = """
Plan a 10-day luxury honeymoon to Italy, focusing on food and history.
We want to visit Rome and Florence, staying in 5-star hotels.
We love wine, authentic Italian cuisine, Renaissance art, and romantic experiences.
Budget is flexible for a once-in-a-lifetime trip.
"""
```

### Example 2: Solo Art Trip

```python
user_request = """
Plan a 5-day trip to Paris for a solo traveler who loves art and food.
Mid-range budget around $200/day for accommodation.
Interested in visiting museums (especially Impressionist art),
trying authentic French cuisine, and exploring charming neighborhoods.
"""
```

### Example 3: Family Adventure

```python
user_request = """
Plan a 7-day family trip to Barcelona with 2 adults and 2 kids (ages 8 and 12).
We want a mix of culture, beaches, and kid-friendly activities.
Budget-conscious but willing to splurge on special experiences.
"""
```

## 🔧 Customization

### Adding Your Own Travel Documents

1. Create `.txt` files in `data/travel_knowledge/`
2. Add destination guides, tips, or any travel information
3. Run the script - ChromaDB will automatically index new documents

Example document:

```
# Tokyo Travel Guide

Best Time to Visit:
- Spring (March-May): Cherry blossoms
- Fall (September-November): Pleasant weather

Transportation:
- JR Pass: Unlimited train travel
- Tokyo Metro: Efficient subway system
...
```

### Integrating Real APIs

Replace mock data in tool files:

**Flight Search** - Integrate with:
- Amadeus API: https://developers.amadeus.com/
- Skyscanner API
- Google Flights via SerpAPI

**Hotel Search** - Integrate with:
- Booking.com API
- Hotels.com API
- Airbnb API

**Activities** - Integrate with:
- GetYourGuide API
- Viator API
- TripAdvisor Experiences

### Customizing Agents

Edit `agents/agents.py`:

```python
def create_custom_agent(tools):
    return Agent(
        role="Your Custom Role",
        goal="Your specific goal...",
        backstory="Agent's background...",
        tools=tools,
        verbose=True
    )
```

## 📊 Output

The system generates:

1. **Console Output**: Real-time agent collaboration and reasoning
2. **Final Itinerary**: Comprehensive day-by-day plan
3. **Saved File**: `travel_itinerary.md` with complete details

Example output structure:

```
# Trip Overview
- Destinations: Paris
- Duration: 5 days
- Dates: [Based on request]

# Flight Details
[Outbound and return flights with all details]

# Day-by-Day Itinerary

## Day 1: Arrival & Le Marais
- Morning: Arrive at CDG, transfer to hotel
- Afternoon: Explore Le Marais neighborhood
- Evening: Dinner at traditional bistro

[... continues for all days]

# Budget Summary
- Flights: $800
- Accommodation: $1,000
- Activities: $400
- Food: $600
Total: $2,800

# Practical Information
[Visa, currency, tips, packing list]
```

## 🧪 Testing Different Scenarios

In `main.py`, change the `selected_request` index:

```python
user_requests = [
    # Example 1: Luxury honeymoon
    "...",
    # Example 2: Solo art trip
    "...",
    # Example 3: Family adventure
    "...",
]

selected_request = user_requests[0]  # Change index to test different requests
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```
   Error: OPENAI_API_KEY not found
   ```
   - Solution: Add your key to `.env` file

2. **ChromaDB Issues**
   ```
   Error initializing vector store
   ```
   - Solution: Delete `data/chroma_db/` and run again

3. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'crewai'
   ```
   - Solution: Run `pip install -r requirements.txt`

## 🚀 Next Steps

### Production Enhancements

1. **Real API Integration**
   - Replace mock data with actual API calls
   - Add API key management
   - Implement rate limiting and caching

2. **Enhanced RAG**
   - Add more travel documents
   - Implement semantic search improvements
   - Use different embedding models

3. **User Interface**
   - Build web interface (Streamlit/Flask)
   - Add interactive itinerary editing
   - Enable PDF export

4. **Advanced Features**
   - Multi-language support
   - Real-time price tracking
   - Collaborative planning for groups
   - Integration with calendar apps

5. **Error Handling**
   - Retry logic for API failures
   - Fallback options for unavailable services
   - Better validation of user inputs

## 📚 Learn More

- **CrewAI Documentation**: https://docs.crewai.com/
- **LangChain RAG**: https://python.langchain.com/docs/use_cases/question_answering/
- **ChromaDB**: https://docs.trychroma.com/

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software for personal or commercial purposes.

## 🙋 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Consult CrewAI documentation

---

**Happy Travels!** ✈️🌍🎉
