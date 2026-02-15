"""Tests for standings tool."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.standings import get_standings


@pytest.mark.asyncio
async def test_get_standings(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"league": {"standings": [[{"rank": 1, "team": {"name": "Arsenal"}, "points": 50}]]}},
    ])
    result = await get_standings(league=39, season=2024)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_standings_missing_params():
    result = await get_standings(league=None, season=2024)
    assert result["success"] is False
    assert "league" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_standings_with_team_filter(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"league": {"standings": [[{"rank": 5, "team": {"id": 33, "name": "Man Utd"}, "points": 35}]]}},
    ])
    result = await get_standings(league=39, season=2024, team=33)
    assert result["success"] is True
    call_params = mock_api.call_args[1]["params"]
    assert call_params["team"] == 33
