"""Tests for trophies tool."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.trophies import get_trophies


@pytest.mark.asyncio
async def test_get_trophies_by_player(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"league": "La Liga", "country": "Spain", "season": "2018/2019", "place": "Winner"},
    ])
    result = await get_trophies(player=276)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_trophies_missing_params():
    result = await get_trophies()
    assert result["success"] is False
    assert "At least one" in result["error"]
