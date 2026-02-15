"""Standings tool: league tables."""

from __future__ import annotations

from api_client import api_request, require_params, _error_response

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_standings(
    league: int,
    season: int,
    team: int | None = None,
) -> dict:
    """Get league standings/table.

    Args:
        league: League ID (required)
        season: Season year (required, e.g., 2024)
        team: Team ID to get only that team's standing

    Returns the full league table with rank, team, points, wins, draws, losses,
    goals for/against, goal difference, and form.
    """
    err = require_params(["league", "season"], {"league": league, "season": season})
    if err:
        return _error_response(err)
    return await api_request("/standings", {
        "league": league, "season": season, "team": team,
    })
