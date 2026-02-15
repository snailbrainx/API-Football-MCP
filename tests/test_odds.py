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
        {"fixture": {"id": 1001}, "bookmakers": []},
    ])
    result = await get_odds(fixture=1001)
    assert result["success"] is True


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
        {"id": 1, "name": "Bet365"},
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
