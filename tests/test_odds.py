"""Tests for odds tools."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.odds import get_odds, get_live_odds, get_odds_mapping, get_bookmakers, get_bet_types


@pytest.mark.asyncio
async def test_get_odds(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {
            "fixture": {"id": 1001, "date": "2025-01-01T20:00:00+00:00"},
            "league": {"id": 39, "name": "Premier League"},
            "update": "2025-01-01T18:00:00+00:00",
            "bookmakers": [
                {
                    "id": 6,
                    "name": "Bet365",
                    "bets": [
                        {
                            "id": 1,
                            "name": "Match Winner",
                            "values": [
                                {"value": "Home", "odd": "1.50"},
                                {"value": "Draw", "odd": "3.80"},
                                {"value": "Away", "odd": "6.00"},
                            ],
                        }
                    ],
                }
            ],
        },
    ])
    result = await get_odds(fixture=1001)
    assert result["success"] is True
    assert result["data"][0]["fixture_id"] == 1001
    assert result["data"][0]["odds"][0]["bet_name"] == "Match Winner"
    assert result["data"][0]["odds"][0]["bookmakers"][0]["name"] == "Bet365"


@pytest.mark.asyncio
async def test_get_odds_simplifies_response(mock_api):
    """Verify the simplifier groups odds by bet type."""
    mock_api.return_value = mock_httpx_response(data=[
        {
            "fixture": {"id": 1001, "date": "2025-01-01T20:00:00+00:00"},
            "league": {"id": 39, "name": "Premier League"},
            "update": "2025-01-01T18:00:00+00:00",
            "bookmakers": [
                {
                    "id": 6, "name": "Bet365",
                    "bets": [
                        {"id": 1, "name": "Match Winner", "values": [{"value": "Home", "odd": "1.50"}]},
                        {"id": 5, "name": "Goals Over/Under", "values": [{"value": "Over 2.5", "odd": "1.80"}]},
                    ],
                },
            ],
        },
    ])
    result = await get_odds(fixture=1001)
    assert result["success"] is True
    odds = result["data"][0]["odds"]
    assert len(odds) == 2
    bet_names = {o["bet_name"] for o in odds}
    assert bet_names == {"Match Winner", "Goals Over/Under"}


@pytest.mark.asyncio
async def test_get_odds_requires_filter():
    result = await get_odds()
    assert result["success"] is False
    assert "required" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_live_odds(mock_api):
    mock_api.return_value = mock_httpx_response(data=[])
    result = await get_live_odds(fixture=1001)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_odds_mapping(mock_api):
    mock_api.return_value = mock_httpx_response(data=[{"fixture": {"id": 1}}])
    result = await get_odds_mapping(page=1)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_bookmakers(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"id": 6, "name": "Bet365"},
    ])
    result = await get_bookmakers()
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_bet_types(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"id": 1, "name": "Match Winner"},
    ])
    result = await get_bet_types()
    assert result["success"] is True
