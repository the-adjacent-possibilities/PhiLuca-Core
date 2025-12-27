#!/data/data/com.termux/files/usr/bin/bash
# AetherOmni Field Recorder - Group Kill Version

ROOT="$HOME/AetherOmni"
LOG="$ROOT/data/field_logs/resonance.log"
PID_FILE="$ROOT/recorder.pid"

start() {
  echo "[$(date)] 🟢 STARTING FIELD RECORDING" >> "$LOG"
  
  # Running the loop in a way that we can track it
  (
    while true; do
      echo "$(date) | FLUX: 45.0 uT | COHERENCE: 0.99" >> "$LOG"
      sleep 5
    done
  ) &
  
  # Save the PID of the background sub-shell
  echo $! > "$PID_FILE"
  echo "Recording started with PID $(cat $PID_FILE)"
}

stop() {
  if [ -f "$PID_FILE" ]; then
    TARGET_PID=$(cat "$PID_FILE")
    # Kill the process and all its children (the loop)
    pkill -P "$TARGET_PID"
    kill "$TARGET_PID"
    rm "$PID_FILE"
    echo "[$(date)] 🛑 RECORDING STOPPED" >> "$LOG"
    echo "Process terminated."
  else
    echo "No recording process found."
  fi
}

case "$1" in
  start|on) start ;;
  stop|off) stop ;;
  pause) stop ;; # For now, pause and stop do the same thing
  *) echo "Usage: $0 {start|stop|pause}" ;;
esac
