"""
Flight Search Tool - Searches for flights with mock data
In production, integrate with Amadeus, Skyscanner, or Google Flights API
"""

from langchain.tools import BaseTool
from typing import Type, Optional, List, Dict
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
import random


class FlightSearchInput(BaseModel):
    """Input schema for Flight Search Tool"""
    origin: str = Field(..., description="Origin city or airport code (e.g., 'New York' or 'JFK')")
    destination: str = Field(..., description="Destination city or airport code (e.g., 'Paris' or 'CDG')")
    departure_date: str = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: Optional[str] = Field(None, description="Return date in YYYY-MM-DD format (optional for one-way)")
    travelers: int = Field(1, description="Number of travelers")
    cabin_class: str = Field("economy", description="Cabin class: economy, premium_economy, business, first")


class FlightSearchTool(BaseTool):
    name: str = "Flight Search Tool"
    description: str = (
        "Searches for available flights between two destinations. "
        "Returns flight options with airlines, prices, durations, and layover information. "
        "Use this tool to find the best flight options for travelers."
    )
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        travelers: int = 1,
        cabin_class: str = "economy"
    ) -> str:
        """
        Execute flight search

        In production, this would call:
        - Amadeus API: https://developers.amadeus.com/
        - Skyscanner API: https://skyscanner.github.io/slate/
        - Google Flights via SerpAPI
        """

        # Mock flight data (replace with real API calls)
        airlines = ["Delta", "United", "Air France", "British Airways", "Lufthansa", "Emirates"]

        # Generate mock flights
        flights = []
        base_price = self._calculate_base_price(origin, destination, cabin_class)

        for i in range(3):
            airline = random.choice(airlines)
            duration = random.randint(6, 15)
            layovers = random.randint(0, 2)
            price_variance = random.uniform(0.8, 1.3)

            flight = {
                "flight_number": f"{airline[:2].upper()}{random.randint(100, 999)}",
                "airline": airline,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "departure_time": f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}",
                "arrival_time": f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}",
                "duration": f"{duration}h {random.randint(0, 55)}m",
                "layovers": layovers,
                "layover_cities": self._get_layover_cities(origin, destination, layovers),
                "price_per_person": round(base_price * price_variance, 2),
                "total_price": round(base_price * price_variance * travelers, 2),
                "cabin_class": cabin_class,
                "baggage": "1 checked bag included" if cabin_class != "economy" else "Carry-on only",
                "amenities": self._get_amenities(cabin_class)
            }
            flights.append(flight)

        # Sort by price
        flights.sort(key=lambda x: x["price_per_person"])

        # Format response
        result = f"## Flight Search Results\n\n"
        result += f"**Route:** {origin} → {destination}\n"
        result += f"**Departure Date:** {departure_date}\n"
        if return_date:
            result += f"**Return Date:** {return_date}\n"
        result += f"**Travelers:** {travelers}\n"
        result += f"**Class:** {cabin_class.replace('_', ' ').title()}\n\n"

        for idx, flight in enumerate(flights, 1):
            result += f"### Option {idx}: {flight['airline']} - ${flight['price_per_person']:.2f}/person\n"
            result += f"- **Flight:** {flight['flight_number']}\n"
            result += f"- **Departure:** {flight['departure_time']}\n"
            result += f"- **Arrival:** {flight['arrival_time']}\n"
            result += f"- **Duration:** {flight['duration']}\n"
            result += f"- **Layovers:** {flight['layovers']}"
            if flight['layovers'] > 0:
                result += f" ({', '.join(flight['layover_cities'])})"
            result += "\n"
            result += f"- **Total Price:** ${flight['total_price']:.2f} (for {travelers} traveler(s))\n"
            result += f"- **Baggage:** {flight['baggage']}\n"
            result += f"- **Amenities:** {flight['amenities']}\n\n"

        if return_date:
            result += f"\n**Note:** Return flight options available for {return_date}. "
            result += "Round-trip prices are approximately 1.8x one-way prices.\n"

        return result

    def _calculate_base_price(self, origin: str, destination: str, cabin_class: str) -> float:
        """Calculate base price based on route and class"""
        # Simple distance-based pricing (mock)
        base = 300

        # International routes cost more
        international_keywords = ["Europe", "Asia", "Africa", "Australia", "Paris", "London", "Tokyo", "Rome"]
        if any(keyword.lower() in f"{origin} {destination}".lower() for keyword in international_keywords):
            base = 800

        # Class multipliers
        multipliers = {
            "economy": 1.0,
            "premium_economy": 1.6,
            "business": 3.5,
            "first": 6.0
        }

        return base * multipliers.get(cabin_class, 1.0)

    def _get_layover_cities(self, origin: str, destination: str, layovers: int) -> List[str]:
        """Get mock layover cities"""
        if layovers == 0:
            return []

        hub_cities = ["Atlanta", "Chicago", "Dubai", "Amsterdam", "Frankfurt", "Istanbul"]
        return random.sample(hub_cities, min(layovers, len(hub_cities)))

    def _get_amenities(self, cabin_class: str) -> str:
        """Get amenities based on cabin class"""
        amenities = {
            "economy": "Standard seat, meals for purchase",
            "premium_economy": "Extra legroom, complimentary meals and drinks",
            "business": "Lie-flat seats, premium meals, lounge access, priority boarding",
            "first": "Private suites, gourmet dining, chauffeur service, premium lounge"
        }
        return amenities.get(cabin_class, "Standard")
