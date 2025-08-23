#!/bin/sh

# Path to the combinations file
COMBO_FILE="combinations.txt"

# Check if a number was passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <combination number (1 to 1536)>"
    exit 1
fi

NUM="$1"

# Validate number input: check if NUM is all digits
case "$NUM" in
  ''|*[!0-9]*)
    echo "Invalid input. Please enter a number between 1 and 1536."
    exit 1
    ;;
esac

# Check numeric range
if [ "$NUM" -lt 1 ] || [ "$NUM" -gt 1536 ]; then
    echo "Invalid input. Please enter a number between 1 and 1536."
    exit 1
fi

# Extract the requested line from the file
LINE=$(sed -n "${NUM}p" "$COMBO_FILE")

# Exit if the line is empty
if [ -z "$LINE" ]; then
    echo "No combination found at line $NUM."
    exit 1
fi

# Split the line by commas and run each app
OLD_IFS=$IFS
IFS=','

for APP in $LINE; do
    # Trim leading and trailing whitespace
    APP=$(echo "$APP" | sed 's/^ *//;s/ *$//')
    # Run the application in background
    ./"$APP" &
done

IFS=$OLD_IFS

echo "Started combination #$NUM in background."
