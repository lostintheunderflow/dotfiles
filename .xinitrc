# disable DPMS so screens never turn of and get lost in X11
xset s off -dpms

# load urxvt color schemes, terminal fonts and other settings
xrdb ~/.Xdefaults

# allow access for qdbus from other sessions
xhost +localhost

setxkbmap -option terminate:ctrl_alt_bksp
if [ -f $HOME/.Xmodmap ]; then
    /usr/bin/xmodmap $HOME/.Xmodmap
fi

# let there be music
/usr/bin/start-pulseaudio-x11

# integrate mouse selection in various graphical windows with the terminal
autocutsel -fork &
autocutsel -selection PRIMARY -fork &

exec i3 
