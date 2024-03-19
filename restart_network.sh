#!/bin/bash

# Set the idle time threshold for restarting NetworkManager (e.g., 1 hour = 3600000 milliseconds)
IDLE_TIME_THRESHOLD=3600000

# Get the current user idle time
idle_time=$(xprintidle)

# Check if the idle time exceeds the threshold
if [ "$idle_time" -gt "$IDLE_TIME_THRESHOLD" ]; then
  # Restart NetworkManager
  echo "$(date): Restarting NetworkManager due to inactivity." >> ~/network_restart_log.txt
  sudo systemctl restart NetworkManager
else
  echo "$(date): User is active. NetworkManager restart skipped." >> ~/network_restart_log.txt
fi
