"""Trophies tool: player and coach trophies."""

from __future__ import annotations

from api_client import api_request, require_at_least_one, _error_response

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_trophies(
    player: int | None = None,
    coach: int | None = None,
) -> dict:
    """Get trophies won by a player or coach.

    Args:
        player: Player ID
        coach: Coach ID

    At least one parameter is required.
    Returns list of trophies with league/competition name, country, season,
    and place (Winner, Runner-up, etc.).
    """
    err = require_at_least_one(["player", "coach"], {"player": player, "coach": coach})
    if err:
        return _error_response(err)
    return await api_request("/trophies", {"player": player, "coach": coach})
