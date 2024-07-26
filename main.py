from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import os
import base64
from requests import post, get 
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

app = FastAPI()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print(client_id, client_secret)

description = """
This app will be able to:

- Get an authorisation token for Spotify's developer API (_implemented_).
- Get information on an artist by name (_implemented_).
- Get an artist's top 10 songs from their name (_implemented_).
- Get recommendations for other artist based on a desired "danceability" index. (_in_progress_).
"""
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Calum Wilmot Python API Test",
        version="0.0.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://developer.spotify.com/images/guidelines/design/logos.svg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
    
@app.get("/artist_search")
def artist_search(artist_name):
    token = get_token()
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    final_url = url + "?" + query
    result = get(final_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result[0]

@app.get("/get_songs_by_artist")
def get_songs_by_artist(token, artist_id):
     token = get_token()
     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
     headers = get_auth_header(token)
     result = get(url, headers=headers)
     json_result = json.loads(result.content)["tracks"]
     return json_result

# def get_recommendations_by_danceability(token, target_danceability, seed_genres):
#      url = f"https://api.spotify.com/v1/recommendations?seed_genres={seed_genres}&target_danceability={target_danceability}"
#      headers = get_auth_header(token)
#      result = get(url, headers=headers)
#      json_result = json.loads(result.content)
#      return json_result


token = get_token()
# result_name = input("Please input artist name:")
# result = artist_search(token, result_name)
# artist_id = (result["id"])
# songs = get_songs_by_artist(token, artist_id)
# get_recommendations_by_danceability(token, 0.8, ['Country'])

# for id, song in enumerate(songs):
#     print(f"{id+1}. {song['name']}")
# print(result)

