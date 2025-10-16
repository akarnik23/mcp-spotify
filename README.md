# Spotify MCP Server

A Micro-Context Protocol (MCP) server that provides access to Spotify's music data through the Spotify Web API. Search for tracks, artists, and get top tracks from any artist - all through natural language conversations.

## 🎵 Features

- **Search Tracks**: Find songs by name, artist, or lyrics
- **Search Artists**: Discover artists and get their information
- **Artist Top Tracks**: Get the most popular tracks for any artist

> **Note**: The Recommendations API is no longer available for new Spotify apps as of November 27, 2024. See [Spotify's announcement](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api) for more details.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Spotify Developer Account
- Spotify App credentials (Client ID and Client Secret)

### Local Development

1. **Clone and navigate to the repository:**
   ```bash
   git clone <your-repo-url>
   cd mcp-spotify
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Spotify API credentials:**
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
   ```

5. **Run the server:**
   ```bash
   python src/server.py
   ```

The server will start on `http://localhost:8000` with the MCP endpoint at `http://localhost:8000/mcp`.

## 🧩 Architecture Note (FastAPI + FastMCP Hybrid)

Note: FastMCP 2.x responses didn’t work well with Poke’s client in my testing due to response format differences. The client expects simpler JSON but errors on FastMCP’s structured content with "Cannot read properties of undefined (reading 'status')". This was reproducible with Interaction’s basic FastMCP template as well.

So for now, this server uses a hybrid architecture where:
- FastAPI endpoints deliver Poke‑compatible JSON
- `@mcp.tool()` functions exist as future‑ready wrappers
- Shared logic lives in `_http` functions to avoid duplication

To try pure FastMCP later:
1) replace the entire FastAPI main block with `mcp.run()`,
2) optionally move each `_http` function’s logic into the corresponding `@mcp.tool()` (or keep wrappers calling `_http`), and
3) remove FastAPI routes if no longer needed.

This works with Poke today while keeping a clean migration path to pure FastMCP.

## 🔑 Getting Spotify API Credentials

1. **Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)**
2. **Log in with your Spotify account**
3. **Click "Create App"**
4. **Fill in the app details:**
   - **App name**: `Your MCP Server` (or any name you prefer)
   - **App description**: `MCP server for Spotify integration`
   - **Website**: `https://spotify-mcp.onrender.com` (use your deployed URL)
   - **Redirect URI**: `https://spotify-mcp.onrender.com` (use your deployed URL)
5. **Select "Web API"** when asked about APIs/SDKs
6. **Click "Save"**
7. **Copy your `Client ID` and `Client Secret`**

**Note:** Use your deployed Render URL (not localhost) for the redirect URI since Spotify requires HTTPS for security.

## 🚢 Deployment

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/akarnik23/mcp-spotify)

**Steps:**
1. **Click the "Deploy to Render" button below** (or go to [render.com](https://render.com) and sign up/login)
2. **Connect your GitHub account to Render** (if you haven't already)
3. **Create a new Web Service:**
   - Connect this repository
   - **Name**: `spotify-mcp`
   - **Environment**: `Python 3`
   - **Plan**: `Free`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/server.py`
4. **Set environment variables:**
   - Go to your Render service dashboard
   - Click on "Environment" tab
   - Add:
     - `SPOTIFY_CLIENT_ID` = `your_client_id`
     - `SPOTIFY_CLIENT_SECRET` = `your_client_secret`
   - Click "Save Changes"
5. **Deploy!**

> Note: On Render's free tier, services go idle after ~15 minutes of inactivity and may require a manual "Deploy" to wake or to pick up the latest commit. Unlike Vercel, pushes do not auto-deploy by default.

Your server will be available at `https://spotify-mcp.onrender.com/mcp`

## 🎯 Poke Integration

1. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
2. Add the MCP URL: `https://spotify-mcp.onrender.com/mcp`
3. Give it a name like "Spotify"
4. Try: "Can you use the Spotify MCP to search tracks for 'Bohemian Rhapsody'?"

## References

- Based on the Interaction MCP server template: [MCP Server Template](https://github.com/InteractionCo/mcp-server-template/tree/main)
- Discovered via Interaction’s HackMIT challenge: [Interaction HackMIT Challenge](https://interaction.co/HackMIT)

## 🛠️ Available Tools

### `search_tracks(query, limit=10)`
Search for tracks on Spotify.

**Parameters:**
- `query` (string): Search query (song name, artist, lyrics, etc.)
- `limit` (int, optional): Number of results to return (1-50, default: 10)

**Example:**
```python
search_tracks("Bohemian Rhapsody", 5)
```

### `search_artists(query, limit=10)`
Search for artists on Spotify.

**Parameters:**
- `query` (string): Search query (artist name, genre, etc.)
- `limit` (int, optional): Number of results to return (1-50, default: 10)

**Example:**
```python
search_artists("Queen", 3)
```

### `get_artist_top_tracks(artist_id, market="US")`
Get the top tracks for a specific artist.

**Parameters:**
- `artist_id` (string): Spotify artist ID
- `market` (string, optional): Market code (default: "US")

**Example:**
```python
get_artist_top_tracks("1dfeR4HaWDbWqFHLkxsg1d")  # Queen's artist ID
```


## 🧪 Testing

Test the server locally:

```bash
# Test health endpoint
curl http://localhost:8000/

# Test MCP endpoint
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

## 📝 Notes

- **Rate Limiting**: The Spotify API has rate limits. The server includes automatic token refresh.
- **Authentication**: Uses Spotify's Client Credentials flow (no user login required).
- **Data Format**: All responses are in JSON format for easy integration.
- **Error Handling**: Comprehensive error handling with descriptive error messages.

