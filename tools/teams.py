"""Team tools: info, statistics, seasons, countries."""

from __future__ import annotations

from api_client import api_request, require_params, _error_response

import sys
sys.path.insert(0, ".")
from server import mcp


@mcp.tool()
async def get_teams(
    id: int | None = None,
    name: str | None = None,
    league: int | None = None,
    season: int | None = None,
    country: str | None = None,
    code: str | None = None,
    venue_id: int | None = None,
    search: str | None = None,
) -> dict:
    """Get team information.

    Args:
        id: Team ID
        name: Exact team name
        league: League ID (requires season)
        season: Season year (requires league)
        country: Country name
        code: Team code (e.g., 'MAU')
        venue_id: Venue ID
        search: Search term (min 3 chars) to find teams by name

    Returns team details including name, logo, country, founded year, and venue.
    Use search_team for a simpler name-based lookup.
    """
    return await api_request("/teams", {
        "id": id, "name": name, "league": league, "season": season,
        "country": country, "code": code, "venue_id": venue_id, "search": search,
    })


@mcp.tool()
async def get_team_statistics(
    team: int,
    league: int,
    season: int,
    date: str | None = None,
) -> dict:
    """Get detailed team statistics for a specific league and season.

    Args:
        team: Team ID (required)
        league: League ID (required)
        season: Season year (required, e.g., 2024)
        date: End date for stats calculation (YYYY-MM-DD)

    Returns comprehensive stats: form, fixtures played/wins/draws/losses,
    goals scored/conceded, clean sheets, penalty stats, lineups, and cards.
    """
    err = require_params(["team", "league", "season"], {"team": team, "league": league, "season": season})
    if err:
        return _error_response(err)
    return await api_request("/teams/statistics", {
        "team": team, "league": league, "season": season, "date": date,
    })


@mcp.tool()
async def get_team_seasons(team: int) -> dict:
    """Get all available seasons for a specific team.

    Args:
        team: Team ID (required)

    Returns a list of season years the team has data for.
    """
    err = require_params(["team"], {"team": team})
    if err:
        return _error_response(err)
    return await api_request("/teams/seasons", {"team": team})


@mcp.tool()
async def get_team_countries() -> dict:
    """Get all countries that have teams in API-Football.

    Returns a list of country names and codes.
    """
    return await api_request("/teams/countries")
