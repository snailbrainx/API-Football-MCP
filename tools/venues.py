"""Venue tool: stadium info and search."""

from __future__ import annotations

from api_client import api_request

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_venues(
    id: int | None = None,
    name: str | None = None,
    city: str | None = None,
    country: str | None = None,
    search: str | None = None,
) -> dict:
    """Get venue/stadium information.

    Args:
        id: Venue ID
        name: Exact venue name
        city: City name
        country: Country name
        search: Search venues by name (min 3 chars)

    Returns venue details: name, address, city, country, capacity, surface, and image.
    Use search_venue for a simpler name-based lookup.
    """
    return await api_request("/venues", {
        "id": id, "name": name, "city": city,
        "country": country, "search": search,
    })
