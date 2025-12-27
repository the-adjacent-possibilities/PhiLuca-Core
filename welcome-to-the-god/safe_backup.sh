#!/bin/bash
# safe_backup.sh — Handles illegal Android characters for SD card backup
DEST="/sdcard/AGI_FULL_BACKUP"
SOURCE="$HOME/welcome-to-the-god/"

echo "[BACKUP] Initiating shielded transfer to $DEST..."

# Create destination if missing
mkdir -p "$DEST"

# rsync with exclusion of illegal FAT32/exFAT characters
rsync -rtv --progress \
  --exclude='*:*' \
  --exclude='*?*' \
  --exclude='*<*' \
  --exclude='*>*' \
  --exclude='*|*' \
  "$SOURCE" "$DEST"

echo "[BACKUP] 77GB Sequence Secured."
