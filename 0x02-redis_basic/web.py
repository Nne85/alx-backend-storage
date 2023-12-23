#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""
import requests
import redis


redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    cached_content = redis_client.get(url)
    if cached_content:
        print("Content retrieved from cache.")
        return cached_content.decode('utf-8')

    print("Fetching content from the web...")
    response = requests.get(url)
    content = response.content.decode('utf-8')

    redis_client.setex(url, 10, content)

    access_count_key = f"count:{url}"
    redis_client.incr(access_count_key)

    return content
