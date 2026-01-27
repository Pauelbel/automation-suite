import os
from core.api.rest_client import  RestApiClient


def test_posts():
    url = os.environ.get("REST_URL")
    result = RestApiClient.get(url + "/posts")

def test_users():
    url = os.environ.get("REST_URL")
    result = RestApiClient.get(url + "/users")
    assert result[0]['address']['city'] == "Gwenborough"
