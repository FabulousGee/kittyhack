#!/bin/bash

case "$1" in
i)  # inner magnetic lock
    cat /sys/class/gpio/gpio525/value
    ;;
o)  # outer magnetic lock
    cat /sys/class/gpio/gpio524/value
    ;;
*) # show some usage information
    echo "For checking the magnetic locks state, please choose an option."
    echo "Usage: \"./getLockState.sh <c>\""
    echo " <c> = i to check state of inner magnetic lock"
    echo " <c> = o to check state of outer magnetic lock"
    ;;
esac
