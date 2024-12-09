#!/bin/bash

# Opening both magnetic locks is currently not possible!
# I suspect they draw to much current and lead to a system error. (CM needs hard reboot then)

# close outer magnet lock
echo 0 > /sys/class/gpio/gpio524/value
# close inner magnetic lock
echo 0 > /sys/class/gpio/gpio525/value

case "$1" in
i)  # inner magnetic lock
    echo 1 > /sys/class/gpio/gpio525/value
    ;;
o)  # outer magnetic lock
    echo 1 > /sys/class/gpio/gpio524/value
    ;;
*) # show some usage information
    echo "For handling the magnetic locks manually, please choose an option."
    echo "Usage: \"./overrideLock.sh <c>\""
    echo " <c> = i to open inner magnetic lock (let kitty come in)"
    echo " <c> = o to open outer magnetic lock (let kitty get out)"
    ;;
esac
