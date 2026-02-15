"""Tests for predictions tool."""

import pytest
from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.predictions import get_predictions


@pytest.mark.asyncio
async def test_get_predictions(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"predictions": {"winner": {"id": 33, "name": "Manchester United"}}, "teams": {}},
    ])
    result = await get_predictions(fixture=1035050)
    assert result["success"] is True


@pytest.mark.asyncio
async def test_get_predictions_missing_fixture():
    result = await get_predictions(fixture=None)
    assert result["success"] is False
    assert "fixture" in result["error"].lower()
