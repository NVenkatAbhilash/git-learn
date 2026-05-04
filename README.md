[MEDIA_COMPRESSION.md](https://github.com/user-attachments/files/27355568/MEDIA_COMPRESSION.md)
# Media Compression Guide

## Contents

### Images
- [Tool: ImageMagick v7](#tool-imagemagick-v7)
- [Single Image](#single-image)
- [Quality Options](#quality-options)
- [Resize Options](#resize-options)
- [Batch Compress (Single Folder)](#batch-compress-single-folder)
- [Batch Compress (With Subfolders)](#batch-compress-with-subfolders)
- [Image Notes](#notes)
- [Image Results](#results-from-first-run)

### Videos
- [Tool: FFmpeg](#tool-ffmpeg-apple-silicon-hardware-encoder)
- [Preset](#preset)
- [Single File](#single-file)
- [Batch Compress](#batch-compress-entire-folder)
- [Copy Metadata Only](#copy-metadata-only-no-compression)
- [Remove Slow Motion](#remove-slow-motion-convert-to-normal-speed)
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

### Batch Compress (Single Folder)

Compresses all images in a folder, preserving creation and modification dates.
Skips files that already exist in destination (safe to re-run).

```bash
SOURCE="/path/to/source/folder"
DEST="/path/to/destination/folder"

mkdir -p "$DEST"

for src in "$SOURCE"/*.jpg "$SOURCE"/*.JPG "$SOURCE"/*.jpeg "$SOURCE"/*.png; do
  [ -f "$src" ] || continue
  basename=$(basename "$src")
  dest_file="$DEST/$basename"

  # Skip if already compressed
  [ -f "$dest_file" ] && echo "SKIP: $basename" && continue

  # Capture source dates
  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")

  magick "$src" -resize 3840x2160\> -quality 85 "$dest_file"

  # Restore original dates
  SetFile -d "$created" "$dest_file"
  touch -mt "$mod" "$dest_file"

  echo "Done: $basename"
done
```

### Batch Compress (With Subfolders)

Compresses all images recursively, preserving folder structure and dates.
Uses 10 parallel workers for speed. Skips already-processed files.

```bash
SRC="/path/to/source"
DEST="/path/to/output"

find "$SRC" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) -print0 | \
xargs -0 -P 10 -I {} bash -c '
  src="$1"; dest="${src/$2/$3}"; mkdir -p "$(dirname "$dest")"

  # Skip if already compressed
  [ -f "$dest" ] && echo "SKIP: $(basename "$src")" && exit 0

  # Capture source dates
  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")

  magick "$src" -resize 3840x2160\> -quality 85 "$dest"

  # Restore original dates
  SetFile -d "$created" "$dest"
  touch -mt "$mod" "$dest"

  echo "Done: $(basename "$src")"
' _ {} "$SRC" "$DEST"
```

### Notes

- `\>` after resize dimensions means never upscale if image is already smaller
- `-quality 85` is the sweet spot — 65% smaller with excellent visual quality
- `SetFile` requires Xcode Command Line Tools (`xcode-select --install`)
- `-P 10` runs 10 images in parallel — adjust based on CPU cores
- Both batch scripts are resume-safe — re-run and they skip already compressed files

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

### Remove Slow Motion (Convert to Normal Speed)

Slow-motion videos (typically 100fps or higher) can be converted to normal 25fps playback to significantly reduce file size (~70% smaller). This drops the extra frames and plays the video at normal speed.

```bash
SOURCE="/path/to/source/folder"

for src in "$SOURCE"/*.mp4; do
  [ -f "$src" ] || continue
  basename=$(basename "$src")

  # Check frame rate
  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$src" 2>/dev/null)
  num=$(echo "$fps" | cut -d/ -f1)
  den=$(echo "$fps" | cut -d/ -f2)
  rate=0
  [ -n "$den" ] && [ "$den" -gt 0 ] 2>/dev/null && rate=$(echo "scale=0; $num / $den" | bc)

  # Skip if not slow-motion
  [ "$rate" -le 60 ] 2>/dev/null && continue

  # Capture source dates
  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")

  tmp="${src}.tmp.mp4"
  echo "Converting: $basename (${rate}fps -> 25fps)"

  ffmpeg -y -i "$src" \
    -c:v hevc_videotoolbox \
    -q:v 65 \
    -tag:v hvc1 \
    -vf "scale=min(3840\,iw):min(2160\,ih)" \
    -r 25 \
    -c:a aac -ac 2 -b:a 160k \
    -movflags +faststart \
    -map_metadata 0 \
    "$tmp" && mv "$tmp" "$src"

  # Restore original dates
  SetFile -d "$created" "$src"
  touch -mt "$mod" "$src"

  echo "Done: $basename"
done
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
