"""Tests for transfers tool."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.transfers import get_transfers


@pytest.mark.asyncio
async def test_get_transfers_by_player(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"player": {"id": 276, "name": "Neymar"}, "transfers": [{"date": "2017-08-03"}]},
    ])
    result = await get_transfers(player=276)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_transfers_missing_params():
    result = await get_transfers()
    assert result["success"] is False
    assert "At least one" in result["error"]
