"""
Activity & Tour Search Tool - Finds attractions, tours, and experiences
In production, integrate with GetYourGuide, Viator, or TripAdvisor API
"""

from langchain.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import random


class ActivitySearchInput(BaseModel):
    """Input schema for Activity Search Tool"""
    destination: str = Field(..., description="Destination city or area")
    interests: str = Field(..., description="User interests (e.g., 'food, history, art, adventure')")
    date: Optional[str] = Field(None, description="Specific date for the activity (YYYY-MM-DD)")
    duration_hours: Optional[int] = Field(None, description="Preferred duration in hours")


class ActivitySearchTool(BaseTool):
    name: str = "Activity Search Tool"
    description: str = (
        "Searches for activities, tours, attractions, and experiences in a destination. "
        "Returns options based on user interests like food, history, art, adventure, etc. "
        "Use this tool to find things to do and see at the destination."
    )
    args_schema: Type[BaseModel] = ActivitySearchInput

    def _run(
        self,
        destination: str,
        interests: str,
        date: Optional[str] = None,
        duration_hours: Optional[int] = None
    ) -> str:
        """
        Execute activity search

        In production, integrate with:
        - GetYourGuide API
        - Viator API
        - TripAdvisor Experiences
        - Airbnb Experiences
        """

        # Parse interests
        interest_list = [i.strip().lower() for i in interests.split(",")]

        # Generate activities based on interests
        activities = []

        # Activity database by category
        activity_db = self._get_activity_database(destination)

        # Match activities to interests
        for interest in interest_list:
            if interest in activity_db:
                activities.extend(random.sample(
                    activity_db[interest],
                    min(2, len(activity_db[interest]))
                ))

        # If no matches, add general activities
        if not activities and "general" in activity_db:
            activities.extend(random.sample(activity_db["general"], 3))

        # Add details to activities
        detailed_activities = []
        for activity in activities[:6]:  # Limit to 6 activities
            details = self._enrich_activity(activity, duration_hours)
            detailed_activities.append(details)

        # Format response
        result = f"## Activity & Tour Options in {destination}\n\n"
        result += f"**Interests:** {interests}\n"
        if date:
            result += f"**Date:** {date}\n"
        result += "\n"

        for idx, activity in enumerate(detailed_activities, 1):
            result += f"### {idx}. {activity['name']}\n"
            result += f"- **Category:** {activity['category']}\n"
            result += f"- **Duration:** {activity['duration']}\n"
            result += f"- **Price:** ${activity['price']}/person\n"
            result += f"- **Rating:** {activity['rating']}⭐ ({activity['reviews']} reviews)\n"
            result += f"- **Description:** {activity['description']}\n"
            result += f"- **Included:** {activity['included']}\n"
            result += f"- **Meeting Point:** {activity['meeting_point']}\n"
            result += f"- **Availability:** {activity['availability']}\n\n"

        return result

    def _get_activity_database(self, destination: str) -> dict:
        """Get activity database for destination"""
        # Generic activities by category
        activities = {
            "food": [
                "Food Walking Tour",
                "Cooking Class with Local Chef",
                "Wine Tasting Experience",
                "Street Food Tour",
                "Gourmet Dinner Experience"
            ],
            "history": [
                "Historical Walking Tour",
                "Museum Guided Tour",
                "Ancient Sites Exploration",
                "Historical Palace Visit",
                "Archaeological Tour"
            ],
            "art": [
                "Art Museum Skip-the-Line Tour",
                "Street Art Tour",
                "Contemporary Gallery Visit",
                "Art Workshop",
                "Artist Studio Tour"
            ],
            "adventure": [
                "Hot Air Balloon Ride",
                "Hiking and Nature Tour",
                "Water Sports Experience",
                "Bike Tour",
                "Kayaking Adventure"
            ],
            "culture": [
                "Cultural Walking Tour",
                "Traditional Performance Show",
                "Local Market Tour",
                "Neighborhood Discovery",
                "Cultural Workshop"
            ],
            "general": [
                "Hop-On Hop-Off Bus Tour",
                "City Highlights Tour",
                "Panoramic City Tour",
                "Private City Guide",
                "Photography Tour"
            ]
        }

        return activities

    def _enrich_activity(self, activity_name: str, duration_hours: Optional[int]) -> dict:
        """Add details to activity"""
        categories = ["Food & Drink", "History & Culture", "Art & Museums", "Adventure", "Sightseeing"]

        # Determine category from name
        category = "General"
        if any(word in activity_name.lower() for word in ["food", "cooking", "wine", "dinner"]):
            category = "Food & Drink"
        elif any(word in activity_name.lower() for word in ["history", "museum", "ancient", "palace"]):
            category = "History & Culture"
        elif any(word in activity_name.lower() for word in ["art", "gallery", "artist"]):
            category = "Art & Museums"
        elif any(word in activity_name.lower() for word in ["adventure", "hiking", "sports", "bike"]):
            category = "Adventure"

        # Generate details
        duration = duration_hours if duration_hours else random.choice([2, 3, 4, 5, 6, 8])
        rating = round(random.uniform(4.2, 5.0), 1)
        base_price = random.choice([45, 65, 85, 120, 150, 200])

        descriptions = {
            "Food & Drink": "Discover authentic local cuisine and culinary traditions with expert guides. Taste regional specialties and learn about food culture.",
            "History & Culture": "Explore historical landmarks and cultural heritage sites. Learn fascinating stories from knowledgeable local historians.",
            "Art & Museums": "Immerse yourself in art and creativity. Visit world-class collections with expert art historians.",
            "Adventure": "Experience thrilling outdoor activities and explore nature. Perfect for adventure seekers.",
            "General": "Discover the highlights and hidden gems of the city with experienced local guides."
        }

        included_items = {
            "Food & Drink": "Local guide, food tastings, beverages, recipe booklet",
            "History & Culture": "Professional guide, skip-the-line access, headphones, entrance fees",
            "Art & Museums": "Art historian guide, skip-the-line tickets, museum entrance",
            "Adventure": "Professional instructor, safety equipment, photos, insurance",
            "General": "Expert guide, transportation, entrance fees, small group"
        }

        return {
            "name": activity_name,
            "category": category,
            "duration": f"{duration} hours",
            "price": base_price,
            "rating": rating,
            "reviews": random.randint(150, 1500),
            "description": descriptions.get(category, descriptions["General"]),
            "included": included_items.get(category, "Professional guide, entrance fees"),
            "meeting_point": random.choice([
                "Central Meeting Point - Details provided after booking",
                "Hotel pickup available",
                "Main Square - By the fountain",
                "Tourist Information Center"
            ]),
            "availability": random.choice([
                "Daily tours at 9:00 AM and 2:00 PM",
                "Available Monday to Saturday",
                "Daily departures",
                "Flexible scheduling available"
            ])
        }
