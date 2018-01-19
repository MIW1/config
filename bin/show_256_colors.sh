#!/bin/bash
# Prints the 256 colors so one can see how they'll look in the terminal
for((i=0; i<256; i++)); do
    printf "\e[48;5;${i}m%03d" $i;
    printf '\e[0m';
    [ ! $((($i - 15) % 6)) -eq 0 ] && printf ' ' || printf '\n'
done
