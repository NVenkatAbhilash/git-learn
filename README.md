[MEDIA_COMPRESSION.md](https://github.com/user-attachments/files/27355608/MEDIA_COMPRESSION.md)
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

### Videos
- [Tool: FFmpeg](#tool-ffmpeg-apple-silicon-hardware-encoder)
- [Preset](#preset)
- [Single File](#single-file)
- [Batch Compress](#batch-compress-entire-folder)
- [Convert Slow-Motion to Normal Speed](#convert-slow-motion-to-normal-speed)
- [Copy Metadata Only](#copy-metadata-only-no-compression)
- [Verify Integrity](#verify-compressed-files-integrity-check)
- [Video Notes](#notes-1)

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

Compresses all `.MP4` files, preserving dates. Skips existing files (safe to re-run).
Runs ffmpeg in background with per-file timeout to prevent hangs on large files.

```bash
SOURCE="/path/to/source/folder"
DEST="/path/to/destination/folder"
mkdir -p "$DEST"

for src in "$SOURCE"/*.MP4; do
  basename=$(basename "$src")
  dest_file="$DEST/${basename%.*}.mp4"
  [ -f "$dest_file" ] && echo "SKIP: $basename" && continue

  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")
  file_mb=$(( $(stat -f "%z" "$src") / 1048576 ))
  timeout_sec=$file_mb; [ $timeout_sec -lt 600 ] && timeout_sec=600; [ $timeout_sec -gt 5400 ] && timeout_sec=5400

  echo "Compressing: $basename (${file_mb}MB, timeout ${timeout_sec}s) ..."

  ffmpeg -y -i "$src" \
    -c:v hevc_videotoolbox -q:v 65 -tag:v hvc1 \
    -vf "scale=min(3840\,iw):min(2160\,ih)" \
    -c:a aac -ac 2 -b:a 160k \
    -movflags +faststart -map_metadata 0 -max_muxing_queue_size 4096 \
    "$dest_file" < /dev/null 2>/dev/null &
  pid=$!

  elapsed=0
  while kill -0 $pid 2>/dev/null; do
    sleep 5; elapsed=$((elapsed + 5))
    if [ $elapsed -ge $timeout_sec ]; then
      kill -9 $pid 2>/dev/null; wait $pid 2>/dev/null
      echo "  TIMEOUT: $basename"; rm -f "$dest_file"; continue 2
    fi
  done
  wait $pid
  [ $? -ne 0 ] || [ ! -f "$dest_file" ] && echo "  FAILED: $basename" && rm -f "$dest_file" && continue

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

### Convert Slow-Motion to Normal Speed

| Type | How to detect | Fix |
|------|--------------|-----|
| **Raw high-fps** | `ffprobe` shows fps > 60 (e.g. 100fps, 300fps) | Re-encode with `-r 25` to drop extra frames |
| **Baked by camera** | `ffprobe` shows 25fps, but camera XML has `captureFps="100.00p"` and `RecordingMode type="slowAndQuickMotion"` | Speed up with `setpts=PTS/4` |

#### Raw High-FPS (drop frames)

Converts in-place. Same timeout logic as batch compress.

```bash
FOLDER="/path/to/compressed/folder"

find "$FOLDER" -maxdepth 1 -type f -iname "*.mp4" -print0 | sort -z | while IFS= read -r -d '' src; do
  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$src" 2>/dev/null)
  num=$(echo "$fps" | cut -d/ -f1); den=$(echo "$fps" | cut -d/ -f2)
  rate=0; [ -n "$den" ] && [ "$den" -gt 0 ] 2>/dev/null && rate=$((num / den))
  [ "$rate" -le 60 ] 2>/dev/null && continue

  file_mb=$(($(stat -f "%z" "$src") / 1048576))
  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")
  tmp="${src}.tmp.mp4"
  timeout_sec=$file_mb; [ $timeout_sec -lt 600 ] && timeout_sec=600; [ $timeout_sec -gt 5400 ] && timeout_sec=5400

  echo "Converting: $(basename "$src") (${rate}fps -> 25fps, ${file_mb}MB)"

  ffmpeg -y -i "$src" \
    -c:v hevc_videotoolbox -q:v 65 -tag:v hvc1 \
    -vf "scale=min(3840\,iw):min(2160\,ih)" -r 25 \
    -c:a aac -ac 2 -b:a 160k \
    -movflags +faststart -map_metadata 0 -max_muxing_queue_size 4096 \
    "$tmp" < /dev/null 2>/dev/null &
  pid=$!; elapsed=0
  while kill -0 $pid 2>/dev/null; do
    sleep 5; elapsed=$((elapsed + 5))
    [ $elapsed -ge $timeout_sec ] && kill -9 $pid 2>/dev/null && wait $pid 2>/dev/null && echo "  TIMEOUT" && rm -f "$tmp" && continue 2
  done
  wait $pid
  [ $? -ne 0 ] || [ ! -f "$tmp" ] && echo "  FAILED" && rm -f "$tmp" && continue

  mv "$tmp" "$src"
  SetFile -d "$created" "$src"; touch -mt "$mod" "$src"
  echo "  Done: ${file_mb}MB -> $(($(stat -f "%z" "$src") / 1048576))MB"
done
```

#### Baked Slo-Mo (speed up playback)

Find baked slo-mo files using camera XML sidecars from the **original source folder**:

```bash
grep -l 'slowAndQuickMotion' "/path/to/original/source/"*.XML | while read xml; do
  base=$(basename "$xml" M01.XML)
  fps=$(grep -o 'captureFps="[^"]*"' "$xml")
  echo "$base: $fps"
done
```

Speed them up (4x for 100fps captured at 25fps):

```bash
FOLDER="/path/to/compressed/folder"
FILES=(C7297 C7306)  # add file list from above

for name in "${FILES[@]}"; do
  src="$FOLDER/${name}.mp4"
  [ ! -f "$src" ] && echo "MISSING: ${name}.mp4" && continue

  orig_mb=$(($(stat -f "%z" "$src") / 1048576))
  mod=$(stat -f "%Sm" -t "%Y%m%d%H%M.%S" "$src")
  created=$(stat -f "%SB" -t "%m/%d/%Y %H:%M:%S" "$src")
  tmp="${src}.tmp.mp4"

  echo "Speedup 4x: ${name}.mp4 (${orig_mb}MB)"

  ffmpeg -y -i "$src" \
    -c:v hevc_videotoolbox -q:v 65 -tag:v hvc1 \
    -vf "setpts=PTS/4,scale=min(3840\,iw):min(2160\,ih)" \
    -af "atempo=2.0,atempo=2.0" \
    -c:a aac -ac 2 -b:a 160k \
    -movflags +faststart -map_metadata 0 -max_muxing_queue_size 4096 \
    "$tmp" < /dev/null 2>/dev/null
  [ $? -ne 0 ] || [ ! -f "$tmp" ] && echo "  FAILED" && rm -f "$tmp" && continue

  mv "$tmp" "$src"
  SetFile -d "$created" "$src"; touch -mt "$mod" "$src"
  echo "  Done: ${orig_mb}MB -> $(($(stat -f "%z" "$src") / 1048576))MB"
done
```

| Capture FPS | Speedup | Video filter | Audio filter |
|---|---|---|---|
| 100fps | 4x | `setpts=PTS/4` | `atempo=2.0,atempo=2.0` |
| 200fps | 8x | `setpts=PTS/8` | `atempo=2.0,atempo=2.0,atempo=2.0` |
| 300fps | 12x | `setpts=PTS/12` | `atempo=2.0,atempo=2.0,atempo=2.0,atempo=1.5` |

### Notes

- `hevc_videotoolbox` uses Apple Silicon hardware encoder — fast and power efficient
- `hvc1` tag ensures compatibility with Apple devices and QuickTime
- `SetFile` requires Xcode Command Line Tools (`xcode-select --install`)
- All batch scripts are resume-safe — re-run and they skip already processed files
- `< /dev/null` and `-max_muxing_queue_size 4096` prevent ffmpeg from hanging on large files
- Per-file timeout (1s/MB, min 10min, max 90min) kills hung encodes automatically
- Baked slo-mo files have no real audio — the camera records silence during slow-motion mode
