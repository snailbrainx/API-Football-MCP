"""Sidelined tool: injury/absence history."""

from __future__ import annotations

from api_client import api_request, require_at_least_one, _error_response

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_sidelined(
    player: int | None = None,
    coach: int | None = None,
) -> dict:
    """Get sidelined (injury/absence) history for a player or coach.

    Args:
        player: Player ID
        coach: Coach ID

    At least one parameter is required.
    Returns list of absences with type (injury description), start date, and end date.
    """
    err = require_at_least_one(["player", "coach"], {"player": player, "coach": coach})
    if err:
        return _error_response(err)
    return await api_request("/sidelined", {"player": player, "coach": coach})
