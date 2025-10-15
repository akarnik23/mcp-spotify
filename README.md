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

## 🌐 Deployment on Render

### Prerequisites

- GitHub account
- Spotify API credentials (see above)

### Steps

1. **Click the "Deploy to Render" button below** (or go to [render.com](https://render.com) and sign up/login)

2. **Connect your GitHub account** if you haven't already

3. **Configure the service:**
   - **Name**: `spotify-mcp`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/server.py`

4. **Add environment variables:**
   - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID
   - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret

5. **Click "Create Web Service"**

6. **Wait for deployment to complete**

Your Spotify MCP server will be available at `https://spotify-mcp.onrender.com/mcp`

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/akarnik23/mcp-spotify)

## 🎯 Poke Integration

1. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
2. Add the MCP URL: `https://spotify-mcp.onrender.com/mcp`
3. Give it a name like "Spotify"
4. Test with: "Tell the subagent to use the Spotify integration's search_tracks tool"

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

### `get_artist_albums(artist_id, limit=20, include_groups="album,single,compilation")`
Get albums for a specific artist.

**Parameters:**
- `artist_id` (string): Spotify artist ID
- `limit` (int, optional): Number of results to return (1-50, default: 20)
- `include_groups` (string, optional): Album types to include (default: "album,single,compilation")

**Example:**
```python
get_artist_albums("1dfeR4HaWDbWqFHLkxsg1d", 10)
```

### `get_recommendations(seed_artists="", seed_genres="", seed_tracks="", limit=20)`
Get track recommendations based on artists, genres, or tracks.

**Parameters:**
- `seed_artists` (string, optional): Comma-separated artist IDs
- `seed_genres` (string, optional): Comma-separated genre names
- `seed_tracks` (string, optional): Comma-separated track IDs
- `limit` (int, optional): Number of recommendations (1-100, default: 20)

**Example:**
```python
get_recommendations(seed_artists="1dfeR4HaWDbWqFHLkxsg1d", limit=10)
```

### `get_playlist_tracks(playlist_id, limit=20)`
Get tracks from a specific playlist.

**Parameters:**
- `playlist_id` (string): Spotify playlist ID
- `limit` (int, optional): Number of tracks to return (1-100, default: 20)

**Example:**
```python
get_playlist_tracks("37i9dQZF1DXcBWIGoYBM5M", 10)  # Today's Top Hits
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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
