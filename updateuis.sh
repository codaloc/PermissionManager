#!/bin/sh

pyuic5 -x qtui.ui -o qtui.py
pyuic5 -x qtpermui.ui -o qtpermui.py

echo "done"
