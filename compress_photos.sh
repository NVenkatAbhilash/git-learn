#!/bin/bash
SRC="/Users/abhi/Documents/A & A/Raw/Photos"
DEST="/Users/abhi/Documents/A & A/Raw/Photos_4K_q85"
LOGFILE="$DEST/_progress.log"
TOTAL=$(find "$SRC" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) ! -path "*/_compression_test/*" | wc -l | tr -d ' ')
COUNT=0
SKIPPED=0
FAILED=0

echo "Starting: $TOTAL photos" | tee "$LOGFILE"
echo "$(date)" | tee -a "$LOGFILE"

process_image() {
    local src_file="$1"
    local dest_file="${src_file/Photos/Photos_4K_q85}"
    local dest_dir
    dest_dir=$(dirname "$dest_file")
    mkdir -p "$dest_dir"

    # Skip if already processed
    if [ -f "$dest_file" ]; then
        echo "SKIP: $(basename "$src_file")"
        return 2
    fi

    # Resize to 4K max, quality 85, keep all EXIF metadata
    if magick "$src_file" -resize 3840x2160\> -quality 85 "$dest_file" 2>/dev/null; then
        # Copy filesystem timestamps (date modified)
        touch -r "$src_file" "$dest_file"
        # Copy creation date on macOS
        local cdate
        cdate=$(GetFileInfo -d "$src_file" 2>/dev/null)
        if [ -n "$cdate" ]; then
            SetFile -d "$cdate" "$dest_file" 2>/dev/null
        fi
        echo "OK: $(basename "$src_file")"
        return 0
    else
        echo "FAIL: $src_file"
        return 1
    fi
}

export -f process_image

find "$SRC" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) ! -path "*/_compression_test/*" -print0 | \
    xargs -0 -P 10 -I {} bash -c 'process_image "$@"' _ {} 2>&1 | \
    while IFS= read -r line; do
        if [[ "$line" == OK:* ]]; then
            COUNT=$((COUNT + 1))
        elif [[ "$line" == SKIP:* ]]; then
            SKIPPED=$((SKIPPED + 1))
        elif [[ "$line" == FAIL:* ]]; then
            FAILED=$((FAILED + 1))
        fi
        DONE=$((COUNT + SKIPPED + FAILED))
        if (( DONE % 50 == 0 )); then
            echo "[$DONE/$TOTAL] Done:$COUNT Skipped:$SKIPPED Failed:$FAILED" | tee -a "$LOGFILE"
        fi
    done

echo "" | tee -a "$LOGFILE"
echo "$(date) - COMPLETE" | tee -a "$LOGFILE"
echo "Source size: $(du -sh "$SRC" | cut -f1)" | tee -a "$LOGFILE"
echo "Output size: $(du -sh "$DEST" | cut -f1)" | tee -a "$LOGFILE"
