# python-graphics
Playing around with basic games in Python. Also teaching kids.

## mover.py
Just move a triangular "ship" around the screen. The ship can go
north, south, east, or west, and needs a little work.

* Arrow keys change direction.
* 'C' changes color.
* ESC exits.

## gravity.py
Fly a triangular "ship" around the sun. The ship rotates in increments
of 10 degrees, and can thrust. The sun pulls you in if you don't orbit,
and you explode if you get too close.

* Left and right arrow keys to rotate.
* Up arrow thrusts forward.
* 'C' changes color.
* ESC exits.
* 'R' resets after an explosion.

## gravity2.py
Adds multiple, interacting bodies (comes with 2 suns and a planet).
The ship controls are the same as `gravity.py`, but the ship will
just fly on through suns and planets.

Also, the numerical simulation is chunky enough that things tend to
get kicked past escape velocity pretty easily. The planet will fly away
after a couple of minutes.
