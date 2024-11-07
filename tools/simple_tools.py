"""
Simple function-based tools for CrewAI 1.4.1
These tools work as simple Python functions that agents can call
"""

from langchain.tools import tool
from typing import Optional
import random
from datetime import datetime


@tool
def search_flights(origin: str, destination: str, departure_date: str, travelers: int = 1, cabin_class: str = "economy") -> str:
    """
    Search for flights between two destinations.

    Args:
        origin: Origin city or airport code
        destination: Destination city or airport code
        departure_date: Departure date in YYYY-MM-DD format
        travelers: Number of travelers
        cabin_class: economy, premium_economy, business, or first

    Returns:
        Flight options with prices and details
    """
    airlines = ["Delta", "United", "Air France", "British Airways", "Lufthansa"]
    base_price = 500 if "europe" in destination.lower() or "paris" in destination.lower() else 300

    multipliers = {"economy": 1.0, "premium_economy": 1.6, "business": 3.5, "first": 6.0}
    price_mult = multipliers.get(cabin_class, 1.0)

    flights = []
    for i in range(3):
        airline = random.choice(airlines)
        price = round(base_price * price_mult * random.uniform(0.8, 1.3), 2)
        duration = random.randint(6, 15)

        flights.append(f"- {airline} Flight #{random.randint(100,999)}: ${price}/person, "
                      f"{duration}h {random.randint(0,55)}m, "
                      f"{random.randint(0,2)} layover(s)")

    result = f"Flight options from {origin} to {destination} on {departure_date}:\n"
    result += "\n".join(flights)
    result += f"\n\nFor {travelers} traveler(s) in {cabin_class} class"
    return result


@tool
def search_hotels(destination: str, check_in: str, check_out: str, guests: int = 2, min_rating: float = 3.0) -> str:
    """
    Search for hotels in a destination.

    Args:
        destination: City or area to search
        check_in: Check-in date YYYY-MM-DD
        check_out: Check-out date YYYY-MM-DD
        guests: Number of guests
        min_rating: Minimum hotel rating (1-5)

    Returns:
        Hotel options with ratings and prices
    """
    from datetime import datetime
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days

    hotel_names = ["Grand Palace Hotel", "Boutique Suites", "Royal Inn", "Elegant Residence"]
    hotels = []

    for i in range(4):
        rating = round(random.uniform(max(min_rating, 3.5), 5.0), 1)
        price_per_night = round(random.uniform(80, 250), 2)
        total = price_per_night * nights

        hotels.append(f"- {random.choice(hotel_names)}: {rating}⭐ "
                     f"(${price_per_night}/night, ${total:.2f} total for {nights} nights)")

    result = f"Hotels in {destination} ({check_in} to {check_out}):\n"
    result += "\n".join(hotels)
    return result


@tool
def search_activities(destination: str, interests: str, duration_hours: int = 4) -> str:
    """
    Search for activities and tours in a destination.

    Args:
        destination: City or area
        interests: Comma-separated interests (e.g., "art, food, history")
        duration_hours: Preferred duration in hours

    Returns:
        Activity recommendations with details
    """
    interest_list = [i.strip().lower() for i in interests.split(",")]

    activities_by_type = {
        "art": ["Museum Skip-the-Line Tour", "Art Gallery Walk", "Street Art Tour"],
        "food": ["Food Walking Tour", "Cooking Class", "Wine Tasting", "Gourmet Dinner"],
        "history": ["Historical Walking Tour", "Ancient Sites Tour", "Museum Guided Tour"],
        "culture": ["Cultural Walking Tour", "Local Market Tour", "Traditional Performance"]
    }

    activities = []
    for interest in interest_list[:3]:
        if interest in activities_by_type:
            activity = random.choice(activities_by_type[interest])
            price = round(random.uniform(45, 150), 2)
            rating = round(random.uniform(4.2, 5.0), 1)
            activities.append(f"- {activity}: {rating}⭐, ${price}/person, ~{duration_hours}hrs")

    if not activities:
        activities.append(f"- City Highlights Tour: 4.5⭐, $65/person, ~{duration_hours}hrs")
        activities.append(f"- Walking Tour: 4.7⭐, $45/person, ~{duration_hours}hrs")

    result = f"Activities in {destination} for interests ({interests}):\n"
    result += "\n".join(activities)
    return result


@tool
def get_travel_knowledge(query: str, destination: Optional[str] = None) -> str:
    """
    Get travel tips, visa requirements, cultural information, and best practices.

    Args:
        query: Question or topic to search for
        destination: Optional specific destination

    Returns:
        Relevant travel knowledge and tips
    """
    # Simplified knowledge base - in production this would use RAG
    knowledge = {
        "visa": "For US citizens traveling to Europe (Schengen Area): No visa required for stays up to 90 days. "
                "ETIAS authorization will be required starting 2024. Always check current requirements before travel.",

        "currency": "Euro (€) is used in most European countries. Credit cards widely accepted. "
                   "Notify your bank before traveling. Exchange rate varies, check current rates.",

        "tipping": "In Europe: 5-10% in restaurants (often service included). Round up taxi fares. "
                  "Tips appreciated but not mandatory like in US.",

        "packing": "Essentials: Valid passport (6+ months validity), travel insurance, comfortable walking shoes, "
                  "layers for varying temperatures, universal power adapter, copies of important documents.",

        "paris": "Best time: April-June, Sept-Oct. Must-see: Eiffel Tower, Louvre, Notre-Dame. "
                "Food: Try bistros, boulangeries. Transport: Metro is efficient. "
                "Tips: Learn basic French phrases, many museums closed Tuesdays.",

        "italy": "Best time: April-June, Sept-Oct. Avoid August (peak tourist). "
                "Must-see: Rome (3-4 days), Florence (2-3 days), Venice (2 days). "
                "Food: Cappuccino only before 11am, dinner after 8pm. "
                "Transport: High-speed trains between cities.",

        "museums": "Book tickets online in advance for popular museums. Skip-the-line tickets worth it. "
                  "Many museums offer free/reduced entry on certain days. Arrive early to avoid crowds."
    }

    query_lower = query.lower()
    dest_lower = destination.lower() if destination else ""

    # Match query keywords to knowledge
    results = []
    for key, info in knowledge.items():
        if key in query_lower or key in dest_lower:
            results.append(info)

    if not results:
        results.append("General tip: Research your destination, respect local customs, "
                      "stay aware of your surroundings, and purchase travel insurance.")

    result = f"Travel Knowledge"
    if destination:
        result += f" for {destination}"
    result += f":\n\n" + "\n\n".join(results)

    return result
