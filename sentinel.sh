#!/data/data/com.termux/files/usr/bin/bash
HB_PID=$(pgrep -f "artemis_vision.py")
SYNC_PID=$(pgrep -f "cloud_sync.sh")

echo -e "\e[1;34m--- ARTEMIS PRODUCTION SENTINEL ---\e[0m"
echo "Hub Location: Nashville, TN"
echo "Active Vision PID: ${HB_PID:-IDLE/WAITING}"
echo "Cloud Sync PID: ${SYNC_PID:-OFFLINE}"
echo "GCP Env: Production"

if [ -n "$SYNC_PID" ]; then
    echo -e "\e[1;32mStatus: FULL UPLINK ACTIVE\e[0m"
else
    echo -e "\e[1;33mStatus: LOCAL LATTICE ONLY\e[0m"
fi
echo "------------------------------------"
