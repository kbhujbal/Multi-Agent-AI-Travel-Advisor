"""
Hotel Search Tool - Searches for accommodations with mock data
In production, integrate with Booking.com, Airbnb, or Hotels.com API
"""

from langchain.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import random


class HotelSearchInput(BaseModel):
    """Input schema for Hotel Search Tool"""
    destination: str = Field(..., description="Destination city or area")
    check_in: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    guests: int = Field(1, description="Number of guests")
    min_rating: float = Field(3.0, description="Minimum hotel rating (1-5 stars)")
    budget_per_night: Optional[float] = Field(None, description="Maximum budget per night in USD")


class HotelSearchTool(BaseTool):
    name: str = "Hotel Search Tool"
    description: str = (
        "Searches for hotels and accommodations in a specific destination. "
        "Returns options with prices, ratings, amenities, and location information. "
        "Use this tool to find suitable accommodations for travelers."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int = 1,
        min_rating: float = 3.0,
        budget_per_night: Optional[float] = None
    ) -> str:
        """
        Execute hotel search

        In production, integrate with:
        - Booking.com API
        - Airbnb API
        - Hotels.com API
        - Expedia API
        """

        # Calculate number of nights
        from datetime import datetime
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days

        # Mock hotel data
        hotel_types = ["Hotel", "Boutique Hotel", "Resort", "Apartment", "B&B"]
        neighborhoods = ["City Center", "Historic District", "Waterfront", "Old Town", "Arts Quarter"]

        hotels = []
        for i in range(5):
            rating = round(random.uniform(min_rating, 5.0), 1)
            price_per_night = self._calculate_price(destination, rating)

            # Filter by budget
            if budget_per_night and price_per_night > budget_per_night:
                price_per_night = random.uniform(budget_per_night * 0.7, budget_per_night)

            hotel = {
                "name": f"{random.choice(['Grand', 'Royal', 'Imperial', 'Elegant', 'Boutique'])} "
                        f"{random.choice(['Palace', 'Inn', 'Suites', 'Hotel', 'Residence'])}",
                "type": random.choice(hotel_types),
                "rating": rating,
                "reviews": random.randint(200, 2000),
                "price_per_night": round(price_per_night, 2),
                "total_price": round(price_per_night * nights, 2),
                "neighborhood": random.choice(neighborhoods),
                "distance_to_center": round(random.uniform(0.2, 3.5), 1),
                "amenities": self._get_amenities(rating, price_per_night),
                "room_type": self._get_room_type(guests),
                "cancellation": "Free cancellation" if random.random() > 0.3 else "Non-refundable",
                "breakfast_included": random.random() > 0.4
            }
            hotels.append(hotel)

        # Sort by rating then price
        hotels.sort(key=lambda x: (-x["rating"], x["price_per_night"]))

        # Format response
        result = f"## Hotel Search Results\n\n"
        result += f"**Destination:** {destination}\n"
        result += f"**Check-in:** {check_in}\n"
        result += f"**Check-out:** {check_out}\n"
        result += f"**Nights:** {nights}\n"
        result += f"**Guests:** {guests}\n\n"

        for idx, hotel in enumerate(hotels, 1):
            result += f"### Option {idx}: {hotel['name']} ({hotel['type']})\n"
            result += f"- **Rating:** {hotel['rating']}⭐ ({hotel['reviews']} reviews)\n"
            result += f"- **Location:** {hotel['neighborhood']} - {hotel['distance_to_center']}km to center\n"
            result += f"- **Price:** ${hotel['price_per_night']:.2f}/night\n"
            result += f"- **Total:** ${hotel['total_price']:.2f} ({nights} nights)\n"
            result += f"- **Room Type:** {hotel['room_type']}\n"
            result += f"- **Breakfast:** {'Included' if hotel['breakfast_included'] else 'Not included'}\n"
            result += f"- **Cancellation:** {hotel['cancellation']}\n"
            result += f"- **Amenities:** {', '.join(hotel['amenities'])}\n\n"

        return result

    def _calculate_price(self, destination: str, rating: float) -> float:
        """Calculate price based on destination and rating"""
        base_prices = {
            "paris": 150,
            "london": 160,
            "rome": 120,
            "tokyo": 130,
            "new york": 180,
            "barcelona": 110,
            "dubai": 140
        }

        # Get base price or default
        base = 100
        for city, price in base_prices.items():
            if city in destination.lower():
                base = price
                break

        # Rating multiplier
        rating_multiplier = 0.5 + (rating / 5.0) * 1.5

        return base * rating_multiplier

    def _get_amenities(self, rating: float, price: float) -> list:
        """Get amenities based on hotel quality"""
        basic = ["WiFi", "Air Conditioning"]
        standard = basic + ["Restaurant", "Room Service", "24-hour Front Desk"]
        premium = standard + ["Spa", "Fitness Center", "Pool", "Concierge"]
        luxury = premium + ["Rooftop Bar", "Valet Parking", "Executive Lounge", "Airport Shuttle"]

        if rating >= 4.5 and price > 200:
            return luxury
        elif rating >= 4.0:
            return premium
        elif rating >= 3.5:
            return standard
        else:
            return basic

    def _get_room_type(self, guests: int) -> str:
        """Determine room type based on guests"""
        if guests == 1:
            return "Single Room / Queen Bed"
        elif guests == 2:
            return "Double Room / King Bed"
        elif guests <= 4:
            return "Family Suite / 2 Bedrooms"
        else:
            return f"Large Suite / {(guests + 1) // 2} Bedrooms"
