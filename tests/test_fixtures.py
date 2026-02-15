"""Tests for fixture tools."""

import pytest

from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.fixtures import (
    get_fixtures, get_rounds, get_head_to_head,
    get_fixture_statistics, get_fixture_events,
    get_fixture_lineups, get_fixture_player_stats,
)


@pytest.mark.asyncio
async def test_get_fixtures_by_date(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"fixture": {"id": 1001}, "teams": {"home": {"name": "Team A"}, "away": {"name": "Team B"}}},
    ])
    result = await get_fixtures(date="2025-01-15")
    assert result["success"] is True
    call_params = mock_api.call_args[1]["params"]
    assert call_params["date"] == "2025-01-15"


@pytest.mark.asyncio
async def test_get_fixtures_live(mock_api):
    mock_api.return_value = mock_httpx_response(data=[])
    result = await get_fixtures(live="all")
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_fixtures_from_to_mapped(mock_api):
    """Test that from_date and to_date are mapped to 'from' and 'to' API params."""
    mock_api.return_value = mock_httpx_response(data=[])
    result = await get_fixtures(league=39, season=2024, from_date="2025-01-01", to_date="2025-01-31")
    assert result["success"] is True
    call_params = mock_api.call_args[1]["params"]
    assert call_params["from"] == "2025-01-01"
    assert call_params["to"] == "2025-01-31"


@pytest.mark.asyncio
async def test_get_rounds(mock_api):
    mock_api.return_value = mock_httpx_response(data=["Regular Season - 1", "Regular Season - 2"])
    result = await get_rounds(league=39, season=2024)
    assert result["success"] is True
    assert result["results"] == 2


@pytest.mark.asyncio
async def test_get_rounds_missing_params():
    result = await get_rounds(league=None, season=2024)
    assert result["success"] is False


@pytest.mark.asyncio
async def test_get_head_to_head(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"fixture": {"id": 100}}, {"fixture": {"id": 200}},
    ])
    result = await get_head_to_head(h2h="33-34")
    assert result["success"] is True
    assert result["results"] == 2


@pytest.mark.asyncio
async def test_get_head_to_head_missing_h2h():
    result = await get_head_to_head(h2h=None)
    assert result["success"] is False
    assert "h2h" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_fixture_statistics(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"team": {"id": 33}, "statistics": [{"type": "Shots on Goal", "value": 5}]},
    ])
    result = await get_fixture_statistics(fixture=1035050)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_fixture_statistics_missing_fixture():
    result = await get_fixture_statistics(fixture=None)
    assert result["success"] is False


@pytest.mark.asyncio
async def test_get_fixture_events(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"time": {"elapsed": 23}, "type": "Goal", "player": {"name": "Test"}},
    ])
    result = await get_fixture_events(fixture=1035050)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_fixture_lineups(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"team": {"id": 33}, "formation": "4-3-3", "startXI": []},
    ])
    result = await get_fixture_lineups(fixture=1035050)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_fixture_player_stats(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"team": {"id": 33}, "players": [{"player": {"name": "Test"}, "statistics": []}]},
    ])
    result = await get_fixture_player_stats(fixture=1035050)
    assert result["success"] is True
