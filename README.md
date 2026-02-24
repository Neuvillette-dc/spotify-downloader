
<!--- mdformat-toc start --slug=github --->

<div align="center">

# spotDL (Neuvillette Edition)

**spotDL** finds songs from Spotify (and CSV files) on YouTube and downloads them - along with high-quality album art, synced lyrics, and rich metadata.

[![MIT License](https://img.shields.io/github/license/Neuvillette-dc/spotify-downloader?color=44CC11&style=flat-square)](https://github.com/Neuvillette-dc/spotify-downloader/blob/master/LICENSE)
[![Discord](https://img.shields.io/discord/771628785447337985?label=discord&logo=discord&style=flat-square)](https://discord.gg/xCa23pwJWY)

> The fastest, most robust version of spotDL with enhanced CSV and lyrics support.
</div>

______________________________________________________________________

## ✨ Key Enhancements in this Version

This fork of `spotDL` includes several critical improvements for power users:

### 📄 Direct CSV Downloading (No-Auth)
Download your library directly from CSV exports without needing a Spotify account or API credentials. 
- Automatically parses song names, artists, and albums.
- Flexible header detection (works with various CSV formats).
- Enhanced metadata enrichment even without Spotify links.

### 🎤 Reliable Synced Lyrics
Integrated with the `syncedlyrics` library and prioritized with the `synced` provider for the highest possible success rate in finding synchronized lyrics.
- Lyrics are embedded directly into the audio file (USLT/ID3v2 tags).
- Silenced noisy provider logs for a clean terminal experience.

### 🏷️ Robust Metadata Logic
Fixed several critical bugs in the metadata embedding process:
- **No more "Invalid MultiSpec" errors**: Improved safety when handling empty metadata fields.
- **Enhanced Mapping**: Better support for `albumartist`, `publisher` (mapped to `encoded_by`), and `isrc`.
- **Publisher Preservation**: Correctly identifies and saves record label information.

### 🛠️ Stability Improvements
- **Graceful Interrupts**: No more scary error blocks when you press `Ctrl+C`.
- **Silenced Library Noises**: Suppressed non-fatal `401 Unauthorized` messages from Musixmatch and other providers.

______________________________________________________________________

## 🚀 Installation

### 1. System Dependencies (Required)
FFmpeg is required for audio conversion. On Ubuntu/Debian (VPS), install it via:
```bash
sudo apt update && sudo apt install -y ffmpeg
```

### 2. Install spotDL

#### **Option A: Quick Install (Recommended for VPS)**
Install directly from this repository as a package:
```bash
pip install git+https://github.com/Neuvillette-dc/spotify-downloader.git
```

#### **Option B: From Source (For Development)**
```bash
git clone https://github.com/Neuvillette-dc/spotify-downloader
cd spotify-downloader
pip install .
```

> **Note**: If you're on Linux and the `spotdl` command is not found after installation, you may need to add `~/.local/bin` to your PATH:
> `export PATH=$PATH:~/.local/bin`


______________________________________________________________________

## 📖 Usage

### Using the CSV Power Feature (New!)
This version of spotDL allows you to download music without needing to log in to Spotify, by using a CSV file.

1. **Get your CSV**: Visit [Exportify](https://exportify.net/) to export your Spotify playlists as CSV files.
2. **Download**:
   ```sh
   spotdl download --csv your_playlist.csv
   ```
   *The downloader will automatically parse the file and find the best matches on YouTube.*

### Standard Usage
You can still use spotDL the "classic" way with URLs:

```sh
spotdl [urls]
```

General syntax:
```sh
spotdl [operation] [options] QUERY
```

<details>
<summary style="font-size:1em"><strong>Supported operations</strong></summary>

- `download`: (Default) Downloads songs and embeds metadata.
- `save`: Saves only the metadata from Spotify without downloading anything.
    - `spotdl save [query] --save-file {filename}.spotdl`
- `sync`: Updates directories. Compares the directory with your playlist and syncs changes.
    - `spotdl sync [query] --save-file {filename}.spotdl`
- `meta`: Updates metadata for existing song files.
- `url`: Get the YouTube URL for each song in the query.

</details>

______________________________________________________________________

## 🙏 Credits

This project would not be possible without the hard work of the original creators and the community.

- **Original Project**: [spotDL - spotify-downloader](https://github.com/spotDL/spotify-downloader)
- **Contributor (Neuvillette Edition)**: [Neuvillette-dc](https://github.com/Neuvillette-dc)
  <details>
  <summary>Environment Details</summary>
  <ul>
    <li>Operating System: Linux (Ubuntu/Debian)</li>
    <li>Python Version: 3.10 - 3.13</li>
  </ul>
  </details>
______________________________________________________________________

## ⚖️ License

This project is licensed under the [MIT](/LICENSE) License.
