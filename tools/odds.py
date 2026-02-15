"""Odds tools: pre-match odds, live odds, bookmakers, bet types, mapping."""

from __future__ import annotations

from api_client import api_request

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_odds(
    fixture: int | None = None,
    league: int | None = None,
    season: int | None = None,
    date: str | None = None,
    timezone: str | None = None,
    page: int | None = None,
    bookmaker: int | None = None,
    bet: int | None = None,
) -> dict:
    """Get pre-match betting odds.

    Args:
        fixture: Fixture ID
        league: League ID (requires season)
        season: Season year (requires league)
        date: Date (YYYY-MM-DD)
        timezone: Timezone
        page: Page number (results are paginated)
        bookmaker: Bookmaker ID filter
        bet: Bet type ID filter

    At least one filter should be provided.
    Returns odds from various bookmakers for different bet types.
    """
    return await api_request("/odds", {
        "fixture": fixture, "league": league, "season": season,
        "date": date, "timezone": timezone, "page": page,
        "bookmaker": bookmaker, "bet": bet,
    })


@mcp.tool()
async def get_live_odds(
    fixture: int | None = None,
    league: int | None = None,
    bet: int | None = None,
) -> dict:
    """Get live/in-play betting odds.

    Args:
        fixture: Fixture ID
        league: League ID
        bet: Bet type ID filter

    Returns live odds that update during matches.
    """
    return await api_request("/odds/live", {
        "fixture": fixture, "league": league, "bet": bet,
    })


@mcp.tool()
async def get_odds_mapping(page: int | None = None) -> dict:
    """Get mapping of fixtures available in the odds endpoint.

    Args:
        page: Page number (results are paginated)

    Returns list of fixture IDs that have odds data available.
    """
    return await api_request("/odds/mapping", {"page": page})


@mcp.tool()
async def get_bookmakers(
    id: int | None = None,
    search: str | None = None,
) -> dict:
    """Get available bookmakers.

    Args:
        id: Bookmaker ID
        search: Search bookmaker by name (min 3 chars)

    Returns list of bookmakers with ID and name.
    """
    return await api_request("/odds/bookmakers", {"id": id, "search": search})


@mcp.tool()
async def get_bet_types(
    id: int | None = None,
    search: str | None = None,
) -> dict:
    """Get available bet types.

    Args:
        id: Bet type ID
        search: Search bet type by name (min 3 chars)

    Returns list of bet types with ID and name (e.g., 'Match Winner', 'Over/Under').
    """
    return await api_request("/odds/bets", {"id": id, "search": search})
