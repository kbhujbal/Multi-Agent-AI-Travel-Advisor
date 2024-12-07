"""
Multi-Agent RAG Travel Planner - Main Orchestration Script

This is the complete, runnable system that:
1. Initializes all tools (including RAG)
2. Creates all specialized agents
3. Defines tasks for each agent
4. Orchestrates the crew workflow
5. Generates a comprehensive travel itinerary

Usage:
    python main.py

License:
    MIT License - See LICENSE file for details
"""

import os
from dotenv import load_dotenv
from crewai import Crew, Process

# Import tools
from tools.flight_search_tool import FlightSearchTool
from tools.hotel_search_tool import HotelSearchTool
from tools.activity_search_tool import ActivitySearchTool
from tools.travel_knowledge_rag_tool import TravelKnowledgeRAGTool

# Import agents
from agents.agents import (
    create_travel_manager,
    create_flight_agent,
    create_accommodation_agent,
    create_activity_agent,
    create_logistics_agent,
    create_itinerary_compiler_agent,
    create_travel_knowledge_agent
)

# Import tasks
from agents.tasks import (
    create_planning_task,
    create_flight_research_task,
    create_accommodation_research_task,
    create_activity_research_task,
    create_logistics_task,
    create_knowledge_consultation_task,
    create_itinerary_compilation_task
)


def initialize_tools():
    """
    Initialize all tools for the agents
    This includes custom API tools and the RAG tool
    """
    print("🔧 Initializing tools...")

    # API-based tools
    flight_tool = FlightSearchTool()
    hotel_tool = HotelSearchTool()
    activity_tool = ActivitySearchTool()

    # RAG tool (ChromaDB vector store)
    rag_tool = TravelKnowledgeRAGTool()

    print("✅ All tools initialized successfully\n")

    return {
        'flight_tool': flight_tool,
        'hotel_tool': hotel_tool,
        'activity_tool': activity_tool,
        'rag_tool': rag_tool
    }


def create_travel_crew(user_request: str):
    """
    Create the complete crew with all agents and tasks

    Args:
        user_request: The user's travel planning request

    Returns:
        Configured Crew ready to execute
    """
    print("👥 Creating agent crew...\n")

    # Create agents without custom tools (CrewAI 1.4.1 compatibility)
    # Agents will use their LLM capabilities and knowledge
    travel_manager = create_travel_manager(
        tools=[]
    )

    flight_agent = create_flight_agent(
        tools=[]
    )

    accommodation_agent = create_accommodation_agent(
        tools=[]
    )

    activity_agent = create_activity_agent(
        tools=[]
    )

    logistics_agent = create_logistics_agent(
        tools=[]
    )

    knowledge_agent = create_travel_knowledge_agent(
        tools=[]
    )

    itinerary_compiler = create_itinerary_compiler_agent(
        tools=[]
    )

    print("✅ Agents created successfully\n")
    print("📋 Creating tasks...\n")

    # Create tasks
    planning_task = create_planning_task(travel_manager, user_request)

    flight_task = create_flight_research_task(flight_agent, planning_task)

    accommodation_task = create_accommodation_research_task(
        accommodation_agent, planning_task
    )

    activity_task = create_activity_research_task(activity_agent, planning_task)

    logistics_task = create_logistics_task(logistics_agent, planning_task)

    # Knowledge task - extract destination from user request
    # In production, you'd parse this more intelligently
    knowledge_task = create_knowledge_consultation_task(
        knowledge_agent,
        destination="the destinations mentioned in the travel plan"
    )

    compilation_task = create_itinerary_compilation_task(
        agent=itinerary_compiler,
        planning_task=planning_task,
        flight_task=flight_task,
        accommodation_task=accommodation_task,
        activity_task=activity_task,
        logistics_task=logistics_task,
        knowledge_task=knowledge_task,
        user_request=user_request
    )

    print("✅ Tasks created successfully\n")

    # Create the crew
    crew = Crew(
        agents=[
            travel_manager,
            flight_agent,
            accommodation_agent,
            activity_agent,
            logistics_agent,
            knowledge_agent,
            itinerary_compiler
        ],
        tasks=[
            planning_task,
            flight_task,
            accommodation_task,
            activity_task,
            logistics_task,
            knowledge_task,
            compilation_task
        ],
        process=Process.sequential,  # Tasks run in sequence
        verbose=True,  # Show detailed output
        # memory=True,  # Enable memory for agents to remember context
    )

    return crew


def main():
    """
    Main execution function
    """
    # Load environment variables
    load_dotenv()

    # Verify OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        print("See .env.example for reference")
        return

    print("=" * 80)
    print("🌍 MULTI-AGENT RAG TRAVEL PLANNER")
    print("=" * 80)
    print()

    # Sample user requests (try different ones!)
    user_requests = [
        # Example 1: Romantic honeymoon
        """
        Plan a 10-day luxury honeymoon to Italy, focusing on food and history.
        We want to visit Rome and Florence, staying in 5-star hotels.
        We love wine, authentic Italian cuisine, Renaissance art, and romantic experiences.
        Budget is flexible for a once-in-a-lifetime trip.
        """,

        # Example 2: Solo art lover
        """
        Plan a 5-day trip to Paris for a solo traveler who loves art and food.
        Mid-range budget around $200/day for accommodation.
        Interested in visiting museums (especially Impressionist art),
        trying authentic French cuisine, and exploring charming neighborhoods.
        """,

        # Example 3: Family adventure
        """
        Plan a 7-day family trip to Barcelona with 2 adults and 2 kids (ages 8 and 12).
        We want a mix of culture, beaches, and kid-friendly activities.
        Budget-conscious but willing to splurge on special experiences.
        Interested in Gaudí architecture, local food markets, and Mediterranean beaches.
        """,
    ]

    # Select which request to use (change index to try different ones)
    selected_request = user_requests[1]  # Paris solo trip

    print("📝 User Request:")
    print("-" * 80)
    print(selected_request.strip())
    print("-" * 80)
    print()

    # Create and run the crew
    try:
        crew = create_travel_crew(selected_request)

        print("🚀 Starting travel planning process...\n")
        print("=" * 80)
        print()

        # Execute the crew
        result = crew.kickoff()

        print()
        print("=" * 80)
        print("✅ TRAVEL PLANNING COMPLETE!")
        print("=" * 80)
        print()
        print("📄 FINAL ITINERARY:")
        print("=" * 80)
        print(result)
        print("=" * 80)

        # Optionally save to file
        output_file = "travel_itinerary.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Travel Itinerary\n\n")
            f.write(f"## Original Request\n\n{selected_request}\n\n")
            f.write(f"## Complete Itinerary\n\n{result}\n")

        print(f"\n💾 Itinerary saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
