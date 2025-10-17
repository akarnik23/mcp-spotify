#!/usr/bin/env python3
"""
Spotify MCP Server
A FastMCP server that provides access to Spotify's music data.
"""

import os
import json
import time
import httpx
from typing import Dict, Any, Optional
from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Spotify MCP Server")

# Spotify API configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_API_BASE = "https://api.spotify.com/v1"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Global variable to store access token
access_token = None
token_expires_at = 0

def get_spotify_token() -> Optional[str]:
    """Get a fresh Spotify access token using client credentials flow."""
    global access_token, token_expires_at
    
    # Check if we have a valid token
    if access_token and time.time() < token_expires_at:
        return access_token
    
    # Debug logging
    print(f"SPOTIFY_CLIENT_ID: {'SET' if SPOTIFY_CLIENT_ID else 'NOT SET'}")
    print(f"SPOTIFY_CLIENT_SECRET: {'SET' if SPOTIFY_CLIENT_SECRET else 'NOT SET'}")
    
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("ERROR: Missing Spotify API credentials")
        return None
    
    try:
        # Request access token
        auth_response = httpx.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": SPOTIFY_CLIENT_ID,
                "client_secret": SPOTIFY_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10.0
        )
        auth_response.raise_for_status()
        
        token_data = auth_response.json()
        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        token_expires_at = time.time() + expires_in - 60  # Refresh 1 minute early
        
        return access_token
        
    except Exception as e:
        print(f"Error getting Spotify token: {e}")
        return None

def make_spotify_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make an authenticated request to the Spotify API."""
    token = get_spotify_token()
    if not token:
        return {"error": "Unable to authenticate with Spotify API"}
    
    try:
        url = f"{SPOTIFY_API_BASE}{endpoint}"
        print(f"Making request to: {url}")
        print(f"With params: {params}")
        print(f"With token: {token[:20]}...")
        # Construct full URL with params for debugging
        from urllib.parse import urlencode
        full_url = f"{url}?{urlencode(params or {})}"
        print(f"Full URL with params: {full_url}")
        
        response = httpx.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params=params or {},
            timeout=15.0
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text[:200]}...")
        print(f"Response headers: {dict(response.headers)}")
        
        response.raise_for_status()
        return response.json()
        
    except httpx.RequestError as e:
        print(f"Request error: {str(e)}")
        return {"error": f"Request failed: {str(e)}"}
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return {"error": f"Spotify API error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}


# Recommendations API removed - no longer available for new Spotify apps as of November 27, 2024

@mcp.tool()
def search_tracks(query: str, limit: int = 10) -> str:
    """Search for tracks on Spotify.
    
    Args:
        query: Search query (song name, artist, lyrics, etc.)
        limit: Number of results to return (default: 10, max: 50)
    
    Returns:
        JSON string with track data
    """
    if not query.strip():
        return json.dumps({"error": "Query cannot be empty"})
    
    # Limit to reasonable range
    limit = max(1, min(limit, 50))
    
    result = make_spotify_request("/search", {
        "q": query,
        "type": "track",
        "limit": limit
    })
    
    if "error" in result:
        return json.dumps(result)
    
    # Format the response
    tracks = result.get("tracks", {}).get("items", [])
    formatted_tracks = []
    
    for track in tracks:
        artists = [artist["name"] for artist in track.get("artists", [])]
        formatted_track = {
            "name": track.get("name", "Unknown"),
            "artists": artists,
            "album": track.get("album", {}).get("name", "Unknown"),
            "duration_ms": track.get("duration_ms", 0),
            "popularity": track.get("popularity", 0),
            "preview_url": track.get("preview_url"),
            "external_urls": track.get("external_urls", {}),
            "id": track.get("id")
        }
        formatted_tracks.append(formatted_track)
    
    return json.dumps({
        "tracks": formatted_tracks,
        "total": result.get("tracks", {}).get("total", 0)
    })

@mcp.tool()
def search_artists(query: str, limit: int = 10) -> str:
    """Search for artists on Spotify.
    
    Args:
        query: Search query (artist name, genre, etc.)
        limit: Number of results to return (default: 10, max: 50)
    
    Returns:
        JSON string with artist data
    """
    if not query.strip():
        return json.dumps({"error": "Query cannot be empty"})
    
    # Limit to reasonable range
    limit = max(1, min(limit, 50))
    
    result = make_spotify_request("/search", {
        "q": query,
        "type": "artist",
        "limit": limit
    })
    
    if "error" in result:
        return json.dumps(result)
    
    # Format the response
    artists = result.get("artists", {}).get("items", [])
    formatted_artists = []
    
    for artist in artists:
        formatted_artist = {
            "name": artist.get("name", "Unknown"),
            "genres": artist.get("genres", []),
            "popularity": artist.get("popularity", 0),
            "followers": artist.get("followers", {}).get("total", 0),
            "external_urls": artist.get("external_urls", {}),
            "id": artist.get("id"),
            "images": artist.get("images", [])
        }
        formatted_artists.append(formatted_artist)
    
    return json.dumps({
        "artists": formatted_artists,
        "total": result.get("artists", {}).get("total", 0)
    })

@mcp.tool()
def get_artist_top_tracks(artist_id: str, market: str = "US") -> str:
    """Get the top tracks for a specific artist.
    
    Args:
        artist_id: Spotify artist ID
        market: Market code (default: "US")
    
    Returns:
        JSON string with top tracks data
    """
    if not artist_id.strip():
        return json.dumps({"error": "Artist ID cannot be empty"})
    
    result = make_spotify_request(f"/artists/{artist_id}/top-tracks", {
        "market": market
    })
    
    if "error" in result:
        return json.dumps(result)
    
    # Format the response
    tracks = result.get("tracks", [])
    formatted_tracks = []
    
    for track in tracks:
        artists = [artist["name"] for artist in track.get("artists", [])]
        formatted_track = {
            "name": track.get("name", "Unknown"),
            "artists": artists,
            "album": track.get("album", {}).get("name", "Unknown"),
            "duration_ms": track.get("duration_ms", 0),
            "popularity": track.get("popularity", 0),
            "preview_url": track.get("preview_url"),
            "external_urls": track.get("external_urls", {}),
            "id": track.get("id")
        }
        formatted_tracks.append(formatted_track)
    
    return json.dumps({"tracks": formatted_tracks})

# Note: Recommendations API is no longer available for new Spotify apps as of November 27, 2024
# See: https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        stateless_http=True
    )
