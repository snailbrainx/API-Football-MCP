"""Tests for team tools."""

import pytest

from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.teams import get_teams, get_team_statistics, get_team_seasons, get_team_countries


@pytest.mark.asyncio
async def test_get_teams_by_id(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"team": {"id": 33, "name": "Manchester United"}, "venue": {"name": "Old Trafford"}},
    ])
    result = await get_teams(id=33)
    assert result["success"] is True
    assert result["data"][0]["team"]["id"] == 33


@pytest.mark.asyncio
async def test_get_team_statistics_success(mock_api):
    mock_api.return_value = mock_httpx_response(data={"form": "WWDLW"}, results=11)
    result = await get_team_statistics(team=33, league=39, season=2024)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_team_statistics_missing_params():
    result = await get_team_statistics(team=33, league=None, season=2024)
    assert result["success"] is False
    assert "league" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_team_seasons(mock_api):
    mock_api.return_value = mock_httpx_response(data=[2020, 2021, 2022, 2023, 2024])
    result = await get_team_seasons(team=33)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_team_countries(mock_api):
    mock_api.return_value = mock_httpx_response(data=["England", "Spain", "France"])
    result = await get_team_countries()
    assert result["success"] is True
