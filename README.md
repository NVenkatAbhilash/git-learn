[IMAGE_COMPRESSION.md](https://github.com/user-attachments/files/27330448/IMAGE_COMPRESSION.md)
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
