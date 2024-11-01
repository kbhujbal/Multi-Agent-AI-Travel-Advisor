"""
CrewAI-native tools for the travel planner
These tools use CrewAI's BaseTool class and work with CrewAI 1.4.1
"""

from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import random


# Flight Search Tool
class FlightSearchInput(BaseModel):
    """Input for FlightSearchTool"""
    origin: str = Field(..., description="Origin city or airport")
    destination: str = Field(..., description="Destination city or airport")
    departure_date: str = Field(..., description="Departure date YYYY-MM-DD")
    travelers: int = Field(default=1, description="Number of travelers")
    cabin_class: str = Field(default="economy", description="economy, premium_economy, business, or first")


class FlightSearchTool(BaseTool):
    name: str = "Search Flights"
    description: str = "Search for flight options between two destinations with pricing and details"
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(self, origin: str, destination: str, departure_date: str, travelers: int = 1, cabin_class: str = "economy") -> str:
        """Execute flight search"""
        airlines = ["Delta", "United", "Air France", "British Airways", "Lufthansa"]
        base_price = 500 if "europe" in destination.lower() or "paris" in destination.lower() else 300

        multipliers = {"economy": 1.0, "premium_economy": 1.6, "business": 3.5, "first": 6.0}
        price_mult = multipliers.get(cabin_class, 1.0)

        flights = []
        for i in range(3):
            airline = random.choice(airlines)
            price = round(base_price * price_mult * random.uniform(0.8, 1.3), 2)
            duration = random.randint(6, 15)
            flights.append(
                f"- {airline} #{random.randint(100,999)}: ${price}/person, "
                f"{duration}h {random.randint(0,55)}m, {random.randint(0,2)} layover(s)"
            )

        result = f"✈️ Flight Options ({origin} → {destination} on {departure_date}):\n"
        result += "\n".join(flights)
        result += f"\n\nFor {travelers} traveler(s) in {cabin_class} class"
        return result


# Hotel Search Tool
class HotelSearchInput(BaseModel):
    """Input for HotelSearchTool"""
    destination: str = Field(..., description="Destination city")
    check_in: str = Field(..., description="Check-in date YYYY-MM-DD")
    check_out: str = Field(..., description="Check-out date YYYY-MM-DD")
    guests: int = Field(default=2, description="Number of guests")
    min_rating: float = Field(default=3.0, description="Minimum rating 1-5")


class HotelSearchTool(BaseTool):
    name: str = "Search Hotels"
    description: str = "Search for hotel accommodations with ratings and pricing"
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(self, destination: str, check_in: str, check_out: str, guests: int = 2, min_rating: float = 3.0) -> str:
        """Execute hotel search"""
        from datetime import datetime
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days

        hotel_names = ["Grand Palace Hotel", "Boutique Suites", "Royal Inn", "Elegant Residence", "Luxury Stay"]
        hotels = []

        for i in range(4):
            rating = round(random.uniform(max(min_rating, 3.5), 5.0), 1)
            price_per_night = round(random.uniform(80, 250), 2)
            total = price_per_night * nights

            hotels.append(
                f"- {random.choice(hotel_names)}: {rating}⭐ "
                f"(${price_per_night}/night, ${total:.2f} for {nights} nights)"
            )

        result = f"🏨 Hotels in {destination} ({check_in} to {check_out}):\n"
        result += "\n".join(hotels)
        return result


# Activity Search Tool
class ActivitySearchInput(BaseModel):
    """Input for ActivitySearchTool"""
    destination: str = Field(..., description="Destination city")
    interests: str = Field(..., description="Comma-separated interests (art, food, history, etc)")
    duration_hours: int = Field(default=4, description="Preferred duration in hours")


class ActivitySearchTool(BaseTool):
    name: str = "Search Activities"
    description: str = "Search for tours, activities, and experiences based on interests"
    args_schema: Type[BaseModel] = ActivitySearchInput

    def _run(self, destination: str, interests: str, duration_hours: int = 4) -> str:
        """Execute activity search"""
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

        result = f"🎭 Activities in {destination} ({interests}):\n"
        result += "\n".join(activities)
        return result


# Travel Knowledge Tool
class TravelKnowledgeInput(BaseModel):
    """Input for TravelKnowledgeTool"""
    query: str = Field(..., description="Question about travel, visa, culture, etc")
    destination: Optional[str] = Field(default=None, description="Specific destination (optional)")


class TravelKnowledgeTool(BaseTool):
    name: str = "Get Travel Knowledge"
    description: str = "Get travel tips, visa requirements, cultural information, and best practices for destinations"
    args_schema: Type[BaseModel] = TravelKnowledgeInput

    def _run(self, query: str, destination: Optional[str] = None) -> str:
        """Retrieve travel knowledge"""
        knowledge = {
            "visa": "For US citizens traveling to Europe: No visa required for stays up to 90 days. ETIAS required starting 2024.",
            "currency": "Euro (€) used in most EU countries. Credit cards widely accepted. Notify your bank before traveling.",
            "tipping": "Europe: 5-10% in restaurants (often included). Round up taxi fares. Not mandatory like in US.",
            "packing": "Essentials: Valid passport, travel insurance, comfortable shoes, layers, universal adapter, document copies.",
            "paris": "Best time: April-June, Sept-Oct. Must-see: Eiffel Tower, Louvre. Transport: Metro efficient. Learn basic French.",
            "italy": "Best time: April-June, Sept-Oct. Rome (3-4 days), Florence (2-3 days), Venice (2 days). Dinner after 8pm.",
            "museums": "Book online in advance. Skip-the-line worth it. Many have free/reduced days. Arrive early."
        }

        query_lower = query.lower()
        dest_lower = destination.lower() if destination else ""

        results = []
        for key, info in knowledge.items():
            if key in query_lower or key in dest_lower:
                results.append(info)

        if not results:
            results.append("Research your destination, respect local customs, stay aware, purchase travel insurance.")

        result = f"📚 Travel Knowledge"
        if destination:
            result += f" for {destination}"
        result += f":\n\n" + "\n\n".join(results)

        return result
