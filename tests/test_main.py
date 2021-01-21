import pytest
import asyncio
import json

import imgrab
import requests

pytestmark = pytest.mark.asyncio

class TestImGrab:
    """Test the ImGrab module."""
    async def test_get(self, mocker):
        """Test retrieval of URL."""
        mocker.patch("imgrab.main.requests.get")
        fake_image_data = b"\x00\x00\x00\x00"
        response = mocker.MagicMock()
        response.status_code = 200
        response.content = fake_image_data
        imgrab.main.requests.get.return_value = response
        with imgrab.ImGrab() as grabber:
            actual = await grabber.get("http://fake.com/image.jpg")
            expected = {
                "url": "http://fake.com/image.jpg",
                "sha256": (
                    "df3f619804a92fdb4057192dc43dd748"
                    "ea778adc52bc498ce80524c014b81119"
                ),
                "data": fake_image_data
            }
        imgrab.main.requests.get.assert_called_with(
            "http://fake.com/image.jpg"
        )
        assert actual == expected
    
    async def test_get_error(self, mocker):
        """Test error handling with URL retrieval."""
        mocker.patch("imgrab.main.requests.get")
        error_msg = b"404 Error: File not found."
        response = mocker.MagicMock()
        response.status_code = 404
        response.content = error_msg
        imgrab.main.requests.get.return_value = response
        with imgrab.ImGrab() as grabber:
            actual = await grabber.get("http://fake.com/image.jpg")
            expected = {
                "url": "http://fake.com/image.jpg",
                "sha256": "0" * 64,
                "data": b"Error: 404",
            }
        assert actual == expected
    
    async def test_get_exceptions(self, mocker):
        """Test exception handling with URL retrieval."""
        mocker.patch("imgrab.main.requests.get")
        imgrab.main.requests.get.side_effect = [
            requests.exceptions.ConnectionError,
            requests.exceptions.ProxyError,
            requests.exceptions.SSLError,
        ]
        response_messages = [
            b"Exception: ConnectionError",
            b"Exception: ProxyError",
            b"Exception: SSLError",
        ]
        with imgrab.ImGrab() as grabber:
            for index in range(len(response_messages)):
                actual = await grabber.get("http://fake.com/image.jpg")
                expected = {
                    "url": "http://fake.com/image.jpg",
                    "sha256": "0" * 64,
                    "data": response_messages[index],
                }
                assert actual == expected