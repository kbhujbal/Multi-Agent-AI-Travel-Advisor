"""
Test script to verify individual tools work correctly
Run this to test each tool independently before running the full system
"""

from tools.flight_search_tool import FlightSearchTool
from tools.hotel_search_tool import HotelSearchTool
from tools.activity_search_tool import ActivitySearchTool
from tools.travel_knowledge_rag_tool import TravelKnowledgeRAGTool
import os
from dotenv import load_dotenv


def test_flight_tool():
    """Test the flight search tool"""
    print("\n" + "=" * 80)
    print("🛫 Testing Flight Search Tool")
    print("=" * 80)

    tool = FlightSearchTool()

    result = tool._run(
        origin="New York",
        destination="Paris",
        departure_date="2024-06-15",
        return_date="2024-06-25",
        travelers=2,
        cabin_class="business"
    )

    print(result)


def test_hotel_tool():
    """Test the hotel search tool"""
    print("\n" + "=" * 80)
    print("🏨 Testing Hotel Search Tool")
    print("=" * 80)

    tool = HotelSearchTool()

    result = tool._run(
        destination="Paris",
        check_in="2024-06-15",
        check_out="2024-06-18",
        guests=2,
        min_rating=4.0,
        budget_per_night=300
    )

    print(result)


def test_activity_tool():
    """Test the activity search tool"""
    print("\n" + "=" * 80)
    print("🎭 Testing Activity Search Tool")
    print("=" * 80)

    tool = ActivitySearchTool()

    result = tool._run(
        destination="Paris",
        interests="art, food, history",
        duration_hours=4
    )

    print(result)


def test_rag_tool():
    """Test the RAG knowledge base tool"""
    print("\n" + "=" * 80)
    print("📚 Testing RAG Knowledge Base Tool")
    print("=" * 80)

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Skipping RAG test - OPENAI_API_KEY not set")
        print("Set your API key in .env to test RAG functionality")
        return

    tool = TravelKnowledgeRAGTool()

    # Test query
    result = tool._run(
        query="What are the visa requirements for Europe?",
        destination="Europe"
    )

    print(result)

    # Test another query
    print("\n" + "-" * 80)
    result = tool._run(
        query="What are some luxury travel tips?",
    )

    print(result)


def main():
    """Run all tests"""
    # Load environment variables
    load_dotenv()

    print("=" * 80)
    print("🧪 TESTING INDIVIDUAL TOOLS")
    print("=" * 80)

    try:
        # Test basic tools (no API key required)
        test_flight_tool()
        test_hotel_tool()
        test_activity_tool()

        # Test RAG tool (requires OpenAI API key)
        test_rag_tool()

        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 80)
        print("\nIf all tools worked correctly, you're ready to run main.py!")

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
