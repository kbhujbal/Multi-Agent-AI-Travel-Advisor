# 🏗️ System Architecture

## Overview

The Multi-Agent RAG Travel Planner is built using a **hierarchical multi-agent architecture** where specialized agents collaborate to solve a complex travel planning task. The system combines **Tool-Calling** for real-time data and **RAG (Retrieval-Augmented Generation)** for knowledge retrieval.

## Core Components

### 1. Agent Layer

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAVEL PLANNING MANAGER                   │
│                      (Orchestrator)                          │
│  • Analyzes user requests                                    │
│  • Coordinates specialist agents                             │
│  • Ensures comprehensive coverage                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ FLIGHT AGENT  │    │ HOTEL AGENT   │    │ACTIVITY AGENT │
│               │    │               │    │               │
│ • Flight Tool │    │ • Hotel Tool  │    │• Activity Tool│
│               │    │               │    │• RAG Tool     │
└───────────────┘    └───────────────┘    └───────────────┘
        ↓                     ↓                     ↓
        └─────────────────────┼─────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
┌───────────────┐                          ┌───────────────┐
│LOGISTICS AGENT│                          │KNOWLEDGE AGENT│
│               │                          │               │
│ • RAG Tool    │                          │ • RAG Tool    │
└───────────────┘                          └───────────────┘
        ↓                                           ↓
        └─────────────────────┬─────────────────────┘
                              ↓
                   ┌──────────────────────┐
                   │ ITINERARY COMPILER   │
                   │                      │
                   │ • Synthesizes all    │
                   │   agent outputs      │
                   │ • Creates final plan │
                   └──────────────────────┘
```

### 2. Tool Layer

```
┌─────────────────────────────────────────────────────────────┐
│                         TOOLS                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  API-Based Tools (Mock → Production APIs)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Flight Tool  │  │  Hotel Tool  │  │ Activity Tool│     │
│  │              │  │              │  │              │     │
│  │ • Search     │  │ • Search     │  │ • Search     │     │
│  │ • Compare    │  │ • Filter     │  │ • Filter     │     │
│  │ • Recommend  │  │ • Recommend  │  │ • Recommend  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  RAG-Based Tool (Vector Database)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Travel Knowledge RAG Tool                    │  │
│  │                                                       │  │
│  │  ┌──────────────┐    ┌──────────────┐              │  │
│  │  │   Documents  │ → │  ChromaDB    │ → Retrieval  │  │
│  │  │   (.txt)     │    │ Vector Store │              │  │
│  │  └──────────────┘    └──────────────┘              │  │
│  │                                                       │  │
│  │  • Visa information                                  │  │
│  │  • Cultural tips                                     │  │
│  │  • Destination guides                                │  │
│  │  • Travel best practices                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3. Data Flow

```
┌──────────────┐
│ User Request │
│  (Natural    │
│  Language)   │
└──────┬───────┘
       ↓
┌──────────────────────────────────────────┐
│ 1. PLANNING PHASE                        │
│    Travel Manager analyzes request       │
│    Extracts: destinations, dates,        │
│    budget, interests                     │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│ 2. RESEARCH PHASE (Parallel)             │
│    ┌─────────────────────────────────┐   │
│    │ Flight Agent  → Flight options  │   │
│    │ Hotel Agent   → Hotel options   │   │
│    │ Activity Agent→ Activities      │   │
│    │ Logistics     → Transportation  │   │
│    │ Knowledge     → Cultural tips   │   │
│    └─────────────────────────────────┘   │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│ 3. COMPILATION PHASE                     │
│    Itinerary Compiler synthesizes:       │
│    • All research findings               │
│    • Creates day-by-day plan             │
│    • Optimizes timing & logistics        │
│    • Adds budget summary                 │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────┐
│Final Itinerary│
│  (Markdown)   │
└───────────────┘
```

## Agent Communication

### Sequential Process

The system uses CrewAI's **Sequential Process**:

1. Tasks execute in order
2. Each task can access outputs from previous tasks via `context`
3. Shared state is maintained throughout the workflow

```python
Task(
    description="...",
    agent=flight_agent,
    context=[planning_task]  # Access planning task output
)
```

### Inter-Agent Communication

```
Planning Task Output
        ↓
    ┌───────┐
    │Context│ → Flight Task
    │ Store │ → Hotel Task
    │       │ → Activity Task
    │       │ → Logistics Task
    │       │ → Knowledge Task
    └───────┘
        ↓
All Task Outputs → Compilation Task
```

## RAG Implementation Details

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Document Loading                                    │
│     ┌─────────────────────────────────────┐            │
│     │  data/travel_knowledge/*.txt        │            │
│     │  • Europe.txt                       │            │
│     │  • Italy.txt                        │            │
│     │  • Packing.txt                      │            │
│     │  • Luxury Travel.txt                │            │
│     └────────────┬────────────────────────┘            │
│                  ↓                                       │
│  2. Text Splitting                                      │
│     ┌─────────────────────────────────────┐            │
│     │  RecursiveCharacterTextSplitter     │            │
│     │  • Chunk size: 1000 chars           │            │
│     │  • Overlap: 200 chars               │            │
│     └────────────┬────────────────────────┘            │
│                  ↓                                       │
│  3. Embedding                                           │
│     ┌─────────────────────────────────────┐            │
│     │  OpenAI Embeddings                  │            │
│     │  • Model: text-embedding-ada-002    │            │
│     └────────────┬────────────────────────┘            │
│                  ↓                                       │
│  4. Vector Storage                                      │
│     ┌─────────────────────────────────────┐            │
│     │  ChromaDB                           │            │
│     │  • Persistent storage               │            │
│     │  • Fast similarity search           │            │
│     └────────────┬────────────────────────┘            │
│                  ↓                                       │
│  5. Retrieval                                           │
│     ┌─────────────────────────────────────┐            │
│     │  Query → Similarity Search          │            │
│     │  Returns top-k relevant chunks      │            │
│     │  (k=3 by default)                   │            │
│     └─────────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### RAG Tool Usage Pattern

```python
# Agent asks a question
agent_query = "What are visa requirements for Italy?"

# RAG Tool processes
1. Convert query to embedding
2. Search vector database for similar content
3. Retrieve top 3 relevant chunks
4. Return formatted results

# Agent uses retrieved information
agent incorporates knowledge into response
```

## Tool Implementation Pattern

All tools follow the **CrewAI BaseTool** pattern:

```python
from crewai_tools import BaseTool
from pydantic import BaseModel

class ToolInput(BaseModel):
    """Typed input schema"""
    param1: str = Field(..., description="...")
    param2: int = Field(default=1, description="...")

class CustomTool(BaseTool):
    name: str = "Tool Name"
    description: str = "What this tool does..."
    args_schema: Type[BaseModel] = ToolInput

    def _run(self, param1: str, param2: int) -> str:
        # Tool logic here
        result = perform_search(param1, param2)
        return formatted_result
```

## Agent-Task Relationship

```
Agent Definition (Who)
┌─────────────────────────┐
│ • Role                  │
│ • Goal                  │
│ • Backstory             │
│ • Tools (what they use) │
│ • Capabilities          │
└───────────┬─────────────┘
            │
            ↓
Task Definition (What to do)
┌─────────────────────────┐
│ • Description           │
│ • Expected Output       │
│ • Context (dependencies)│
│ • Agent (who does it)   │
└─────────────────────────┘
```

Example:

```python
# WHO: Define the agent
flight_agent = Agent(
    role="Flight Research Specialist",
    tools=[flight_search_tool]
)

# WHAT: Define the task
flight_task = Task(
    description="Find best flights...",
    agent=flight_agent,
    context=[planning_task]
)
```

## File Structure & Responsibilities

```
Multi Agent AI Travel Agent/
│
├── main.py                  ← Entry point, orchestrates everything
│   • Initializes tools
│   • Creates agents & tasks
│   • Runs the crew
│
├── agents/
│   ├── agents.py           ← Agent definitions (WHO)
│   │   • 7 specialist agents
│   │   • Roles, goals, backstories
│   │
│   └── tasks.py            ← Task definitions (WHAT)
│       • 7 corresponding tasks
│       • Descriptions & expected outputs
│
├── tools/
│   ├── flight_search_tool.py      ← Flight API tool
│   ├── hotel_search_tool.py       ← Hotel API tool
│   ├── activity_search_tool.py    ← Activity API tool
│   └── travel_knowledge_rag_tool.py ← RAG tool
│
└── data/
    ├── travel_knowledge/   ← Documents for RAG
    └── chroma_db/          ← Vector database (auto-generated)
```

## Execution Flow

### Initialization Phase

```
1. Load environment (.env)
2. Initialize tools
   ├─ Create FlightSearchTool instance
   ├─ Create HotelSearchTool instance
   ├─ Create ActivitySearchTool instance
   └─ Create TravelKnowledgeRAGTool instance
       └─ Initialize ChromaDB
           └─ Load/create vector store
3. Create agents (assign tools)
4. Create tasks (assign agents + context)
5. Build crew (agents + tasks)
```

### Execution Phase

```
crew.kickoff()
    ↓
For each task in sequential order:
    1. Agent receives task description
    2. Agent analyzes what tools to use
    3. Agent calls tools with parameters
    4. Tools return results
    5. Agent processes results
    6. Agent generates output
    7. Output added to context
    ↓
Final task receives all context
    ↓
Compilation agent creates itinerary
    ↓
Return final result
```

## Scalability & Extensions

### Adding New Agents

```python
# 1. Create agent function in agents/agents.py
def create_budget_optimizer(tools):
    return Agent(
        role="Budget Optimization Specialist",
        goal="Find cost-saving opportunities...",
        backstory="...",
        tools=tools
    )

# 2. Create corresponding task in agents/tasks.py
def create_budget_optimization_task(agent):
    return Task(
        description="Analyze all costs and find savings...",
        agent=agent
    )

# 3. Add to crew in main.py
budget_agent = create_budget_optimizer([...])
budget_task = create_budget_optimization_task(budget_agent)
```

### Adding New Tools

```python
# 1. Create tool file: tools/weather_tool.py
class WeatherTool(BaseTool):
    name = "Weather Forecast Tool"
    # ... implementation

# 2. Initialize in main.py
weather_tool = WeatherTool()

# 3. Assign to relevant agents
activity_agent = create_activity_agent(
    tools=[activity_tool, weather_tool]
)
```

### Adding New Documents to RAG

```
1. Create .txt file in data/travel_knowledge/
2. Add content (destination guides, tips, etc.)
3. Delete data/chroma_db/ to force rebuild
4. Run main.py - ChromaDB auto-indexes new docs
```

## Production Considerations

### 1. API Integration

Replace mock data with real APIs:

```python
# tools/flight_search_tool.py
def _run(self, origin, destination, ...):
    # Instead of mock data:
    # return self._generate_mock_flights()

    # Use real API:
    amadeus = AmadeusAPI(api_key=os.getenv("AMADEUS_KEY"))
    flights = amadeus.search_flights(
        origin=origin,
        destination=destination,
        ...
    )
    return self._format_results(flights)
```

### 2. Caching

Implement caching to reduce API calls:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def search_flights(origin, destination, date):
    # Expensive API call
    pass
```

### 3. Error Handling

Add robust error handling:

```python
def _run(self, ...):
    try:
        result = api_call()
    except APIError as e:
        return fallback_result()
    except RateLimitError:
        time.sleep(retry_after)
        return self._run(...)  # Retry
```

### 4. Async Processing

For better performance:

```python
# Run independent research tasks in parallel
import asyncio

async def run_research_parallel():
    results = await asyncio.gather(
        flight_research(),
        hotel_research(),
        activity_research()
    )
```

## Key Design Decisions

### Why CrewAI?

✅ Built specifically for multi-agent collaboration
✅ Clear agent roles and task definitions
✅ Sequential and hierarchical processes
✅ Easy tool integration
✅ Active development and community

### Why ChromaDB for RAG?

✅ Simple to set up and use
✅ Persistent storage
✅ Fast similarity search
✅ Good Python integration
✅ Lightweight (no separate server needed)

### Why Sequential Process?

✅ Clear dependencies (flights before logistics)
✅ Each agent builds on previous work
✅ Easier to debug and understand
✅ More predictable output quality

Alternative: Hierarchical process with a manager delegating tasks

## Performance Metrics

Typical execution time (with mocked APIs):
- Tool initialization: 5-10 seconds
- Planning task: 10-15 seconds
- Research tasks (5 agents): 30-60 seconds
- Compilation: 20-30 seconds
- **Total: ~90-120 seconds**

With real APIs: 3-5 minutes (depends on API response times)

## Security Considerations

1. **API Keys**: Always use environment variables
2. **Input Validation**: Sanitize user inputs
3. **Rate Limiting**: Implement for API calls
4. **Data Privacy**: Don't log sensitive information
5. **Vector Store**: Secure ChromaDB data directory

---

**This architecture provides a solid foundation for building production-ready multi-agent travel planning systems!**
