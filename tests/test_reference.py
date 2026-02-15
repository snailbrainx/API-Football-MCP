"""Tests for reference data tools."""

import pytest

from tests.conftest import mock_httpx_response

import sys
sys.argv = ["test"]
from server import mcp, register_tools
register_tools()

from tools.reference import get_timezones, get_countries, get_seasons, get_leagues


@pytest.mark.asyncio
async def test_get_timezones(mock_api):
    mock_api.return_value = mock_httpx_response(data=["Europe/London", "America/New_York"])
    result = await get_timezones()
    assert result["success"] is True
    assert result["results"] == 2


@pytest.mark.asyncio
async def test_get_countries(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"name": "England", "code": "GB", "flag": "flag.png"},
    ])
    result = await get_countries(search="Eng")
    assert result["success"] is True
    assert result["data"][0]["name"] == "England"


@pytest.mark.asyncio
async def test_get_seasons(mock_api):
    mock_api.return_value = mock_httpx_response(data=[2020, 2021, 2022, 2023, 2024])
    result = await get_seasons()
    assert result["success"] is True
    assert 2024 in result["data"]


@pytest.mark.asyncio
async def test_get_leagues(mock_api):
    mock_api.return_value = mock_httpx_response(data=[
        {"league": {"id": 39, "name": "Premier League"}, "country": {"name": "England"}},
    ])
    result = await get_leagues(country="England", season=2024)
    assert result["success"] is True
    mock_api.assert_called_once()
    call_params = mock_api.call_args[1]["params"]
    assert call_params["country"] == "England"
    assert call_params["season"] == 2024
