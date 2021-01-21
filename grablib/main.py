"""Main.py: Home of the GrabLib class."""

import asyncio
import hashlib

import requests


class GrabLib:
    """Image Grabber: Downloads images from specified URLs."""

    def __init__(self):
        """Initialize GrabLib."""

    def __enter__(self):
        """Elevate the Self."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Eliminate the Self."""

    async def get(self, image_url):
        """Retrieve the provided URL."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, requests.get, image_url
            )
            data = response.content
            if response.status_code != 200:
                image_sha256 = "0" * 64
                data = f"Error: {response.status_code}".encode()
            else:
                sha256 = hashlib.sha256()
                sha256.update(response.content)
                image_sha256 = sha256.hexdigest()
        except Exception as ex:
            image_sha256 = "0" * 64
            data = f"Exception: {type(ex).__name__}".encode()
        return {"url": image_url, "sha256": image_sha256, "data": data}
