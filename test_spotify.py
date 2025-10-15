#!/usr/bin/env python3
"""
Test script for the Spotify MCP Server
"""

import requests
import json
import time

# Configuration
TUNNEL_URL = "https://spotify-test.loca.lt"  # Update this with your local tunnel URL
MCP_ENDPOINT = f"{TUNNEL_URL}/mcp"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(TUNNEL_URL, timeout=10)
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def test_mcp_tools():
    """Test MCP tools list"""
    print("\n🔍 Testing MCP tools list...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        response = requests.post(MCP_ENDPOINT, json=payload, timeout=10)
        print(f"✅ Tools list: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
                print(f"📋 Available tools ({len(tools)}):")
                for tool in tools:
                    print(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
            else:
                print(f"Response: {data}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Tools list failed: {e}")

def test_search_tracks():
    """Test track search"""
    print("\n🔍 Testing track search...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "search_tracks",
                "arguments": {
                    "query": "Bohemian Rhapsody",
                    "limit": 3
                }
            }
        }
        response = requests.post(MCP_ENDPOINT, json=payload, timeout=15)
        print(f"✅ Track search: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "content" in data["result"]:
                content = json.loads(data["result"]["content"][0]["text"])
                if "tracks" in content:
                    tracks = content["tracks"]
                    print(f"🎵 Found {len(tracks)} tracks:")
                    for i, track in enumerate(tracks[:3], 1):
                        print(f"  {i}. {track.get('name', 'Unknown')} by {', '.join(track.get('artists', []))}")
                else:
                    print(f"Response: {content}")
            else:
                print(f"Response: {data}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Track search failed: {e}")

def test_search_artists():
    """Test artist search"""
    print("\n🔍 Testing artist search...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search_artists",
                "arguments": {
                    "query": "Queen",
                    "limit": 2
                }
            }
        }
        response = requests.post(MCP_ENDPOINT, json=payload, timeout=15)
        print(f"✅ Artist search: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "content" in data["result"]:
                content = json.loads(data["result"]["content"][0]["text"])
                if "artists" in content:
                    artists = content["artists"]
                    print(f"🎤 Found {len(artists)} artists:")
                    for i, artist in enumerate(artists[:2], 1):
                        print(f"  {i}. {artist.get('name', 'Unknown')} - {artist.get('followers', 0):,} followers")
                        print(f"     Genres: {', '.join(artist.get('genres', [])[:3])}")
                else:
                    print(f"Response: {content}")
            else:
                print(f"Response: {data}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Artist search failed: {e}")

def test_recommendations():
    """Test recommendations"""
    print("\n🔍 Testing recommendations...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_recommendations",
                "arguments": {
                    "seed_genres": "rock,pop",
                    "limit": 3
                }
            }
        }
        response = requests.post(MCP_ENDPOINT, json=payload, timeout=15)
        print(f"✅ Recommendations: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "content" in data["result"]:
                content = json.loads(data["result"]["content"][0]["text"])
                if "tracks" in content:
                    tracks = content["tracks"]
                    print(f"🎯 Got {len(tracks)} recommendations:")
                    for i, track in enumerate(tracks[:3], 1):
                        print(f"  {i}. {track.get('name', 'Unknown')} by {', '.join(track.get('artists', []))}")
                else:
                    print(f"Response: {content}")
            else:
                print(f"Response: {data}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Recommendations failed: {e}")

def main():
    """Run all tests"""
    print("🎵 Spotify MCP Server Test Suite")
    print("=" * 40)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    test_health()
    test_mcp_tools()
    test_search_tracks()
    test_search_artists()
    test_recommendations()
    
    print("\n✅ Test suite completed!")
    print("\n💡 To test locally:")
    print("1. Start the server: python src/server.py")
    print("2. Start local tunnel: npx localtunnel --port 8000")
    print("3. Update TUNNEL_URL in this script")
    print("4. Run: python test_spotify.py")

if __name__ == "__main__":
    main()
