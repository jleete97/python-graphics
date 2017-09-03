import math

# Utility functions to calculate 2-D rotations.

# Rotation matrices (2 x 2) for each degree, 0-359.
rotationMatrices = {}

# Calculate each degree's rotation matrix.
for deg in range(360):
    rad = deg * math.pi / 180.0
    rotationMatrix = [
        [math.cos(rad), -math.sin(rad)],
        [math.sin(rad), math.cos(rad)]
    ]
    rotationMatrices[deg] = rotationMatrix

# Rotate a point about the origin.
#
# param p The point to rotate.
# param deg The number of degrees to rotate the point.
#
def rotate(p, deg):
    rm = rotationMatrices[deg]
    return (p[0] * rm[0][0] + p[1] * rm[0][1],
            p[0] * rm[1][0] + p[1] * rm[1][1])

# Rotate a point about a defined center.
#
# param center The center to rotate around.
# param p The point to rotate. (This is an offset from the center.)
# param deg The number of degrees to rotate.
#
def offsetRotate(center, p, deg):
    rot = rotate(p, deg)
    return (center[0] + rot[0], center[1] + rot[1])