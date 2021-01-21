"""Test_main.py: Test GrabLib."""

import pytest
import requests

import grablib

pytestmark = pytest.mark.asyncio


class TestGrabLib:
    """Test the GrabLib module."""

    async def test_get(self, mocker):
        """Test retrieval of URL."""
        mocker.patch("grablib.main.requests.get")
        fake_image_data = b"\x00\x00\x00\x00"
        response = mocker.MagicMock()
        response.status_code = 200
        response.content = fake_image_data
        grablib.main.requests.get.return_value = response
        with grablib.GrabLib() as grabber:
            actual = await grabber.get("http://fake.com/image.jpg")
            expected = {
                "url": "http://fake.com/image.jpg",
                "sha256": (
                    "df3f619804a92fdb4057192dc43dd748"
                    "ea778adc52bc498ce80524c014b81119"
                ),
                "data": fake_image_data,
            }
        grablib.main.requests.get.assert_called_with(
            "http://fake.com/image.jpg"
        )
        assert actual == expected

    async def test_get_error(self, mocker):
        """Test error handling with URL retrieval."""
        mocker.patch("grablib.main.requests.get")
        error_msg = b"404 Error: File not found."
        response = mocker.MagicMock()
        response.status_code = 404
        response.content = error_msg
        grablib.main.requests.get.return_value = response
        with grablib.GrabLib() as grabber:
            actual = await grabber.get("http://fake.com/image.jpg")
            expected = {
                "url": "http://fake.com/image.jpg",
                "sha256": "0" * 64,
                "data": b"Error: 404",
            }
        assert actual == expected

    async def test_get_exceptions(self, mocker):
        """Test exception handling with URL retrieval."""
        mocker.patch("grablib.main.requests.get")
        grablib.main.requests.get.side_effect = [
            requests.exceptions.ConnectionError,
            requests.exceptions.ProxyError,
            requests.exceptions.SSLError,
        ]
        response_messages = [
            b"Exception: ConnectionError",
            b"Exception: ProxyError",
            b"Exception: SSLError",
        ]
        with grablib.GrabLib() as grabber:
            for response_message in response_messages:
                actual = await grabber.get("http://fake.com/image.jpg")
                expected = {
                    "url": "http://fake.com/image.jpg",
                    "sha256": "0" * 64,
                    "data": response_message,
                }
                assert actual == expected
