"""Tests for venues tool."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.venues import get_venues


@pytest.mark.asyncio
async def test_get_venues_by_search(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"id": 556, "name": "Old Trafford", "city": "Manchester", "capacity": 76212},
    ])
    result = await get_venues(search="Old Trafford")
    assert result["success"] is True
    assert result["data"][0]["name"] == "Old Trafford"


@pytest.mark.asyncio
async def test_get_venues_by_country(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"id": 1, "name": "Wembley", "city": "London"},
    ])
    result = await get_venues(country="England")
    assert result["success"] is True
