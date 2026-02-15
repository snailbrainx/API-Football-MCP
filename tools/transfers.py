"""Transfer tool: transfer history."""

from __future__ import annotations

from api_client import api_request, require_at_least_one, _error_response

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_transfers(
    player: int | None = None,
    team: int | None = None,
) -> dict:
    """Get transfer history for a player or team.

    Args:
        player: Player ID
        team: Team ID

    At least one parameter is required.
    Returns transfer records with date, type (free, loan, transfer fee),
    and the teams involved (from/to).
    """
    err = require_at_least_one(["player", "team"], {"player": player, "team": team})
    if err:
        return _error_response(err)
    return await api_request("/transfers", {"player": player, "team": team})
