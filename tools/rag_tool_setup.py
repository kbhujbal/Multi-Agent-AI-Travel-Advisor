"""
RAG Tool Setup using CrewAI's built-in RagTool
"""

from crewai_tools import RagTool
import os


def create_travel_rag_tool():
    """
    Create a RAG tool for travel knowledge using CrewAI's RagTool

    This tool will index documents from data/travel_knowledge/ directory
    and allow agents to search for relevant travel information.
    """
    knowledge_base_path = "./data/travel_knowledge"

    # Ensure directory exists
    os.makedirs(knowledge_base_path, exist_ok=True)

    # Create sample documents if they don't exist
    _create_sample_documents(knowledge_base_path)

    # Create RAG tool pointing to the knowledge base directory
    rag_tool = RagTool(
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model="gpt-4",
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model="text-embedding-3-small",
                ),
            ),
        )
    )

    return rag_tool


def _create_sample_documents(knowledge_base_path):
    """Create sample travel knowledge documents"""
    documents = {
        "europe_travel.txt": """
        TRAVEL TIPS FOR EUROPE

        Visa Requirements:
        - US citizens can travel to most EU countries for up to 90 days without a visa
        - ETIAS authorization will be required starting 2024
        - Always check specific country requirements

        Currency:
        - Euro (€) is used in 20 EU countries
        - Credit cards widely accepted
        - Notify your bank before traveling

        Transportation:
        - Trains are efficient and connect major cities
        - Consider a Eurail pass for multiple countries
        - Metro systems in major cities are excellent

        Cultural Etiquette:
        - Tipping: 5-10% in restaurants
        - Dress modestly when visiting religious sites
        - Learn basic phrases in local language
        """,

        "paris_guide.txt": """
        PARIS TRAVEL GUIDE

        Best Time to Visit:
        - April to June: Pleasant weather, fewer crowds
        - September to October: Beautiful fall colors
        - Avoid peak summer (July-August)

        Top Attractions:
        - Eiffel Tower: Book tickets online in advance
        - Louvre Museum: Wednesday/Friday open late
        - Notre-Dame: Currently under reconstruction
        - Versailles: Full day trip required

        Food & Dining:
        - Boulangeries: Fresh bread and pastries daily
        - Cafés: Pay more to sit, cheaper at the bar
        - Markets: Marché Bastille (Thursday/Sunday)
        - Dinner: Typically after 8 PM

        Transportation:
        - Metro: Efficient, buy carnet (10 tickets) for savings
        - Museum Pass: Skip lines at 60+ attractions
        - Walking: Many areas best explored on foot
        """,

        "luxury_travel.txt": """
        LUXURY TRAVEL TIPS

        Accommodations:
        - 5-star hotels and boutique properties
        - Consider hotel loyalty programs
        - Book suites for special occasions

        Dining:
        - Michelin-starred restaurants (book months ahead)
        - Private chef experiences
        - Wine pairing dinners

        Transportation:
        - Business/First class flights
        - Private airport transfers
        - Chauffeur services

        Experiences:
        - Private museum tours after hours
        - Exclusive wine tastings
        - Helicopter tours
        - Personal guides
        """
    }

    for filename, content in documents.items():
        filepath = os.path.join(knowledge_base_path, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())

    print(f"✅ Created {len(documents)} sample travel documents in {knowledge_base_path}")
