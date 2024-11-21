"""
Agents package for Multi-Agent Travel Planner
"""

from .agents import (
    create_travel_manager,
    create_flight_agent,
    create_accommodation_agent,
    create_activity_agent,
    create_logistics_agent,
    create_itinerary_compiler_agent,
    create_travel_knowledge_agent
)

from .tasks import (
    create_planning_task,
    create_flight_research_task,
    create_accommodation_research_task,
    create_activity_research_task,
    create_logistics_task,
    create_knowledge_consultation_task,
    create_itinerary_compilation_task
)

__all__ = [
    'create_travel_manager',
    'create_flight_agent',
    'create_accommodation_agent',
    'create_activity_agent',
    'create_logistics_agent',
    'create_itinerary_compiler_agent',
    'create_travel_knowledge_agent',
    'create_planning_task',
    'create_flight_research_task',
    'create_accommodation_research_task',
    'create_activity_research_task',
    'create_logistics_task',
    'create_knowledge_consultation_task',
    'create_itinerary_compilation_task'
]
