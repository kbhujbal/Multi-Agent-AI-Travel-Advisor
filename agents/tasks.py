"""
Task Definitions for Multi-Agent Travel Planner
Each task defines what an agent should accomplish
"""

from crewai import Task, Agent
from typing import Optional


def create_planning_task(agent: Agent, user_request: str) -> Task:
    """
    Manager's initial planning task
    Analyzes user request and creates high-level plan
    """
    return Task(
        description=(
            f"Analyze this travel request and break it down into specific requirements:\n\n"
            f"{user_request}\n\n"
            f"Extract and clarify:\n"
            f"1. Destination(s) - which cities/countries\n"
            f"2. Duration - how many days/nights\n"
            f"3. Travel dates or timeframe\n"
            f"4. Number of travelers and any special requirements\n"
            f"5. Budget level (luxury, mid-range, budget)\n"
            f"6. Key interests and priorities (food, history, art, adventure, relaxation, etc.)\n"
            f"7. Any specific requirements mentioned (dietary, accessibility, etc.)\n\n"
            f"Create a high-level planning framework that other agents will use."
        ),
        expected_output=(
            "A structured breakdown of the travel requirements including destinations, "
            "duration, dates, traveler profile, budget level, interests, and any special "
            "requirements. Include a suggested high-level itinerary structure (e.g., "
            "'3 days Rome, 2 days Florence, 3 days Venice')."
        ),
        agent=agent
    )


def create_flight_research_task(agent: Agent, planning_context: Optional[str] = None) -> Task:
    """
    Flight agent's research task
    Finds best flight options
    """
    return Task(
        description=(
            f"Based on the travel plan, research and recommend flight options.\n\n"
            f"Find flights that:\n"
            f"1. Match the departure dates and destinations\n"
            f"2. Fit the budget level (economy, business, first class)\n"
            f"3. Optimize for the best combination of price, duration, and convenience\n"
            f"4. Consider layovers and total travel time\n\n"
            f"Provide at least 2-3 options with different price/convenience tradeoffs.\n"
            f"Include details on baggage, amenities, and booking recommendations."
        ),
        expected_output=(
            "Detailed flight recommendations with at least 3 options including: "
            "airlines, flight numbers, departure/arrival times, duration, layovers, "
            "prices, baggage allowance, and amenities. Include a clear recommendation "
            "for the best option and explain why."
        ),
        agent=agent,
        context=[planning_context] if planning_context else []
    )


def create_accommodation_research_task(agent: Agent, planning_context: Optional[str] = None) -> Task:
    """
    Accommodation agent's research task
    Finds hotels and lodging
    """
    return Task(
        description=(
            f"Based on the travel plan, research and recommend accommodations.\n\n"
            f"For each destination/city in the itinerary:\n"
            f"1. Find 2-3 hotel/accommodation options\n"
            f"2. Match the budget level and traveler preferences\n"
            f"3. Consider location (proximity to attractions, safety, neighborhood character)\n"
            f"4. Evaluate amenities, ratings, and reviews\n"
            f"5. Check availability for the specified dates\n\n"
            f"Prioritize accommodations that enhance the overall trip experience."
        ),
        expected_output=(
            "Detailed accommodation recommendations for each city/destination including: "
            "hotel names, ratings, prices per night and total, location/neighborhood, "
            "distance to main attractions, amenities, room types, cancellation policies, "
            "and breakfast inclusion. Include a clear recommendation for each destination."
        ),
        agent=agent,
        context=[planning_context] if planning_context else []
    )


def create_activity_research_task(agent: Agent, planning_context: Optional[str] = None) -> Task:
    """
    Activity agent's research task
    Finds tours, attractions, and experiences
    """
    return Task(
        description=(
            f"Based on the travel plan and traveler interests, curate activities and experiences.\n\n"
            f"For each destination:\n"
            f"1. Identify must-see attractions aligned with traveler interests\n"
            f"2. Find highly-rated tours and unique experiences\n"
            f"3. Include a mix of: iconic sights, cultural experiences, food/dining, and hidden gems\n"
            f"4. Consider pacing - don't over-schedule\n"
            f"5. Note any activities that need advance booking\n\n"
            f"Create enough options for the entire trip duration with some flexibility."
        ),
        expected_output=(
            "Comprehensive list of activities, tours, and experiences for each destination "
            "including: activity names, categories, durations, prices, ratings, descriptions, "
            "what's included, booking requirements, and recommendations for which days they "
            "would work best. Organize by destination and interest category."
        ),
        agent=agent,
        context=[planning_context] if planning_context else []
    )


def create_logistics_task(agent: Agent, planning_context: Optional[str] = None) -> Task:
    """
    Logistics agent's task
    Plans ground transportation
    """
    return Task(
        description=(
            f"Based on the travel plan, organize all ground transportation and logistics.\n\n"
            f"Plan transportation for:\n"
            f"1. Airport to first hotel (and hotel to airport at end)\n"
            f"2. Between cities (trains, buses, flights, car rental)\n"
            f"3. Within each city (metro, taxis, walking, bike rentals)\n"
            f"4. Day trips if applicable\n\n"
            f"For each segment provide:\n"
            f"- Best transportation method and why\n"
            f"- Estimated cost and duration\n"
            f"- Booking requirements\n"
            f"- Practical tips (where to catch train, metro lines, etc.)\n"
        ),
        expected_output=(
            "Complete transportation plan covering all logistics including: airport transfers, "
            "inter-city transport with schedules and prices, local transportation recommendations "
            "for each city, metro/transit tips, and any transport passes worth buying. Include "
            "estimated travel times and costs."
        ),
        agent=agent,
        context=[planning_context] if planning_context else []
    )


def create_knowledge_consultation_task(agent: Agent, destination: str) -> Task:
    """
    Knowledge agent's task
    Provides expert advice via RAG
    """
    return Task(
        description=(
            f"Provide comprehensive travel knowledge and advice for: {destination}\n\n"
            f"Research and provide information on:\n"
            f"1. Visa requirements and entry procedures\n"
            f"2. Cultural etiquette and customs\n"
            f"3. Best time to visit and weather considerations\n"
            f"4. Currency, payment methods, and tipping practices\n"
            f"5. Safety tips and travel advisories\n"
            f"6. Packing recommendations\n"
            f"7. Local customs and dining etiquette\n"
            f"8. Any destination-specific tips\n\n"
            f"Use the travel knowledge base to provide accurate, detailed information."
        ),
        expected_output=(
            "Comprehensive travel guide covering visa/entry requirements, cultural etiquette, "
            "best times to visit, currency/payment info, safety tips, packing suggestions, "
            "local customs, and insider tips. All information should be specific and actionable."
        ),
        agent=agent
    )


def create_itinerary_compilation_task(
    agent: Agent,
    planning_task: Task,
    flight_task: Task,
    accommodation_task: Task,
    activity_task: Task,
    logistics_task: Task,
    knowledge_task: Task,
    user_request: str
) -> Task:
    """
    Final compilation task
    Assembles everything into complete itinerary
    """
    return Task(
        description=(
            f"Create a comprehensive, day-by-day travel itinerary using all research from specialist agents.\n\n"
            f"Original request: {user_request}\n\n"
            f"Your itinerary must:\n"
            f"1. Be organized day-by-day with clear structure\n"
            f"2. Include all flight details (outbound and return)\n"
            f"3. Show accommodation for each night with check-in/check-out\n"
            f"4. Schedule activities logically (group by neighborhood, consider timing)\n"
            f"5. Include all transportation between locations\n"
            f"6. Build in realistic timing and some flexibility\n"
            f"7. Note any advance bookings required\n"
            f"8. Include estimated daily costs\n"
            f"9. Add insider tips and cultural notes\n"
            f"10. Provide a budget summary at the end\n\n"
            f"Make it detailed, easy to follow, and exciting to read!"
        ),
        expected_output=(
            "A complete, beautifully formatted day-by-day itinerary including:\n"
            f"- Trip Overview (destinations, dates, duration)\n"
            f"- Flight Details (outbound and return)\n"
            f"- Daily Breakdown with:\n"
            f"  * Morning/Afternoon/Evening activities\n"
            f"  * Transportation between activities\n"
            f"  * Meal recommendations\n"
            f"  * Estimated timing for each activity\n"
            f"  * Accommodation details for each night\n"
            f"- Practical Information (visa, currency, tips, packing)\n"
            f"- Budget Summary (flights, hotels, activities, food, transport)\n"
            f"- Pre-Trip Checklist (bookings to make, what to pack)\n\n"
            f"Format should be clear, detailed, and ready to use."
        ),
        agent=agent,
        context=[planning_task, flight_task, accommodation_task, activity_task, logistics_task, knowledge_task]
    )
