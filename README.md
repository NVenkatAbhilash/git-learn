[IMAGE_COMPRESSION.md](https://github.com/user-attachments/files/27330519/IMAGE_COMPRESSION.md)
# Media Compression Guide

## Contents

### Images
- [Tool: ImageMagick v7](#tool-imagemagick-v7)
- [Single Image](#single-image)
- [Quality Options](#quality-options)
- [Resize Options](#resize-options)
- [Batch Processing](#batch-processing)
- [Image Results](#results-from-first-run)

### Videos
- [Tool: FFmpeg](#tool-ffmpeg-apple-silicon-hardware-encoder)
- [Preset](#preset)
- [Single File](#single-file)
- [Batch Compress](#batch-compress-entire-folder)
- [Copy Metadata Only](#copy-metadata-only-no-compression)
- [Verify Integrity](#verify-compressed-files-integrity-check)
- [Video Notes](#notes)
- [Video Results](#results)

---

# Image Compression Guide

## Tool: ImageMagick v7

### Install

```bash
brew install imagemagick
```

### Single Image

```bash
magick "input.jpg" -resize 3840x2160\> -quality 85 "output.jpg"
```

| Flag | What it does |
|------|-------------|
| `-resize 3840x2160\>` | Shrink to fit 4K max. `\>` means never upscale smaller images |
| `-quality 85` | JPEG compression level (1-100). 85 is the sweet spot |
| `-strip` | Optional. Removes EXIF metadata (loses dates/camera info but saves a bit more) |

### Quality Options

| Quality | Savings | Use case |
|---------|---------|----------|
| 90 | ~50% smaller | Archival — visually identical to original |
| **85** | **~65% smaller** | **Recommended — excellent quality** |
| 80 | ~70% smaller | Very good — slight loss on zoom |
| 75 | ~75% smaller | Good — for general sharing |

### Resize Options

| Size | Flag | Use case |
|------|------|----------|
| 4K | `-resize 3840x2160\>` | Best balance of quality and size |
| 2K | `-resize 1920x1080\>` | Social media / sharing |
| Original | _(omit flag)_ | Keep full resolution, only recompress |

### Batch Processing

For bulk compression with subfolder support, preserved dates, and parallel processing:

```bash
bash compress_photos.sh
```

Edit `SRC` and `DEST` at the top of the script before running. The script:

- Processes images in parallel (10 workers)
- Preserves EXIF metadata (camera info, date taken, GPS)
- Copies filesystem dates (date created & date modified) from originals
- Skips already-processed files (safe to re-run if interrupted)
- Logs progress to `_progress.log` in the output folder

### Results from First Run

| | Photos | Size |
|---|--------|------|
| Original | 8,517 | 121 GB |
| 4K + q85 | 8,517 | 10 GB |
| **Savings** | — | **111 GB (92%)** |

---

# Video Compression Guide

## Tool: FFmpeg (Apple Silicon Hardware Encoder)

### Install

```bash
brew install ffmpeg
```

### Preset

| Setting | Value |
|---|---|
| Resolution | Source (capped at 3840x2160) |
| Framerate | Source (unchanged) |
| Codec | H.265/HEVC (`hevc_videotoolbox`) |
| Quality | `-q:v 65` |
| Tag | `hvc1` (Apple/QuickTime compatible) |
| Audio | AAC Stereo, 160kbps |
| Extra | `-movflags +faststart` (web optimized) |

### Single File

```bash
ffmpeg -y -i "INPUT.MP4" \
  -c:v hevc_videotoolbox \
  -q:v 65 \
  -tag:v hvc1 \
  -vf "scale=min(3840,iw):min(2160,ih)" \
  -c:a aac -ac 2 -b:a 160k \
  -movflags +faststart \
  -map_metadata 0 \
  "OUTPUT.mp4"
```

### Batch Compress (Entire Folder)

Compresses all `.MP4` files from source to destination, preserving creation and modification dates.
Skips files that already exist in destination (safe to re-run).

```bash
SOURCE="/path/to/source/folder"
DEST="/path/to/destination/folder"

mkdir -p "$DEST"

for src in "$SOURCE"/*.MP4; do
  basename=$(basename "$src")
  name="${basename%.*}"
  dest_file="$DEST/${name}.mp4"

  # Skip if already compressed
  [ -f "$dest_file" ] && echo "SKIP: $basename" && continue

  # Capture source dates
  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")

  echo "Compressing: $basename ..."

  ffmpeg -y -i "$src" \
    -c:v hevc_videotoolbox \
    -q:v 65 \
    -tag:v hvc1 \
    -vf "scale=min(3840\,iw):min(2160\,ih)" \
    -c:a aac -ac 2 -b:a 160k \
    -movflags +faststart \
    -map_metadata 0 \
    "$dest_file"

  # Restore original dates
  SetFile -d "$created" "$dest_file"
  touch -mt "$mod" "$dest_file"

  echo "Done: $basename"
done
```

### Copy Metadata Only (No Compression)

If files are already compressed (e.g. by HandBrake) and you just need to copy dates from source to destination:

```bash
SOURCE="/path/to/source/folder"
DEST="/path/to/destination/folder"

for src in "$SOURCE"/*; do
  basename=$(basename "$src")
  target=$(find "$DEST" -maxdepth 1 -iname "$basename" -print -quit)

  [ -z "$target" ] && echo "SKIP: No match for $basename" && continue

  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")

  SetFile -d "$created" "$target"
  touch -mt "$mod" "$target"

  echo "Done: $basename"
done
```

### Verify Compressed Files (Integrity Check)

```bash
DEST="/path/to/destination/folder"

for f in "$DEST"/*.mp4; do
  result=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$f" 2>&1)
  if [ $? -ne 0 ] || [ -z "$result" ]; then
    echo "BAD: $(basename "$f")"
  fi
done && echo "All files OK."
```

### Notes

- `hevc_videotoolbox` uses Apple Silicon hardware encoder — fast and power efficient
- `-q:v 65` is high quality; lower number = higher quality, higher filesize
- `hvc1` tag ensures compatibility with Apple devices and QuickTime
- `SetFile` requires Xcode Command Line Tools (`xcode-select --install`)
- The batch script is resume-safe — re-run it and it skips already compressed files
- Source framerate is preserved (no upscaling from 25fps to 60fps)

### Results

| Folder | Files | Original | Compressed | Savings |
|---|---|---|---|---|
| Kavali Pelli Kuthuru | 405 | 101 GB | 28 GB | 73 GB (72%) |
| Pelli Koduku till Marriage start | 558 | 228 GB | 165 GB | 63 GB (28%) |
