#!/bin/bash
exec 2>/dev/null
timeout -k 5 60 /home/emojivm/emojivm $1
