"""Tests for coaches tool."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.coaches import get_coaches


@pytest.mark.asyncio
async def test_get_coaches_by_team(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"id": 1, "name": "J. Klopp", "career": []},
    ])
    result = await get_coaches(team=40)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_coaches_by_search(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"id": 4, "name": "P. Guardiola", "career": []},
    ])
    result = await get_coaches(search="Guardiola")
    assert result["success"] is True
    assert result["data"][0]["name"] == "P. Guardiola"
