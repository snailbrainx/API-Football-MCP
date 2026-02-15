"""Tests for player tools."""

import pytest

from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.players import (
    get_players, get_player_squads, get_player_seasons,
    get_top_scorers, get_top_assists, get_top_yellow_cards, get_top_red_cards,
)


@pytest.mark.asyncio
async def test_get_players_by_id(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"player": {"id": 276, "name": "Neymar"}, "statistics": []},
    ])
    result = await get_players(id=276, season=2024)
    assert result["success"] is True
    assert result["data"][0]["player"]["name"] == "Neymar"


@pytest.mark.asyncio
async def test_get_player_squads(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"team": {"id": 33}, "players": [{"id": 1, "name": "Player 1"}]},
    ])
    result = await get_player_squads(team=33)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_player_seasons(mock_api):
    mock_api.return_value = mock_httpx_response(data=[2018, 2019, 2020, 2021])
    result = await get_player_seasons(player=276)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_top_scorers(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"player": {"id": 1100, "name": "E. Haaland"}, "statistics": [{"goals": {"total": 27}}]},
    ])
    result = await get_top_scorers(league=39, season=2024)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_top_scorers_missing_params():
    result = await get_top_scorers(league=None, season=2024)
    assert result["success"] is False
    assert "league" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_top_assists(mock_api):
    mock_api.return_value = mock_httpx_response(data=[{"player": {"name": "Test"}}])
    result = await get_top_assists(league=39, season=2024)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_top_yellow_cards(mock_api):
    mock_api.return_value = mock_httpx_response(data=[{"player": {"name": "Test"}}])
    result = await get_top_yellow_cards(league=39, season=2024)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_top_red_cards(mock_api):
    mock_api.return_value = mock_httpx_response(data=[{"player": {"name": "Test"}}])
    result = await get_top_red_cards(league=39, season=2024)
    assert result["success"] is True
