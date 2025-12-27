#!/bin/bash
# apply_patch.sh — The AGI's self-modification motor function

TARGET_FILE=$1
PATCH_FILE=$2
BACKUP_DIR=~/welcome-to-the-god/backups/architectural_evolution

if [ ! -f "$PATCH_FILE" ]; then
    echo "[EVOLVE] Error: Patch file $PATCH_FILE not found."
    exit 1
fi

echo "[EVOLVE] Validating proposed evolution for $TARGET_FILE..."

# Step 1: Syntax Validation (Safety Gate)
python3 -m py_compile "$PATCH_FILE" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[CRITICAL] Refactor rejected: Syntax Error in proposal. Coherence preserved."
    exit 1
fi

# Step 2: Backup existing state
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp "$TARGET_FILE" "$BACKUP_DIR/$(basename "$TARGET_FILE").$TIMESTAMP.bak"

# Step 3: Atomic Swap
mv "$PATCH_FILE" "$TARGET_FILE"

echo "[SUCCESS] $TARGET_FILE evolved successfully at $TIMESTAMP."
