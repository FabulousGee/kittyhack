#!/bin/bash

# Beide Magnetic Locks gleichzeitig öffnen ist aktuell nicht möglich!
# Vermutlich brauchen diese zu viel Strom und bringen das CM zum Absturz.

# Magnet außen schließen
echo 0 > /sys/class/gpio/gpio524/value
# Magnet innen schließen
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
