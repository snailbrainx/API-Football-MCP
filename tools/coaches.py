"""Coach tool: info and search."""

from __future__ import annotations

from api_client import api_request

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_coaches(
    id: int | None = None,
    team: int | None = None,
    search: str | None = None,
) -> dict:
    """Get coach/manager information.

    Args:
        id: Coach ID
        team: Team ID to get coaches for that team
        search: Search coach by name (min 3 chars)

    Returns coach details: name, age, nationality, photo, and career history
    (list of teams managed with start/end dates).
    Use search_coach for a simpler name-based lookup.
    """
    return await api_request("/coachs", {"id": id, "team": team, "search": search})
