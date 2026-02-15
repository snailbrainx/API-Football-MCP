"""Predictions tool: match predictions."""

from __future__ import annotations

from api_client import api_request, require_params, _error_response

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_predictions(fixture: int) -> dict:
    """Get match prediction for a fixture.

    Args:
        fixture: Fixture ID (required)

    Returns prediction data including: winner prediction, win/draw percentages,
    advice text, goals predictions, team comparison stats (form, attack, defense),
    and head-to-head summary.
    """
    err = require_params(["fixture"], {"fixture": fixture})
    if err:
        return _error_response(err)
    return await api_request("/predictions", {"fixture": fixture})
