#!/bin/bash
 
if [ -z "$1" ]; then
        echo "Usage: $0 filename"
        exit 1
fi
filename="$1"
grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\b' "$filename" | sort -u
 
