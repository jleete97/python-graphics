import math

rotationMatrices = {}

for deg in range(360):
    rad = deg * math.pi / 180.0
    rotationMatrix = [
        [math.cos(rad), -math.sin(rad)],
        [math.sin(rad), math.cos(rad)]
    ]
    rotationMatrices[deg] = rotationMatrix

def rotate(p, deg):
    rm = rotationMatrices[deg]
    return (p[0] * rm[0][0] + p[1] * rm[0][1],
            p[0] * rm[1][0] + p[1] * rm[1][1])

def offsetRotate(center, p, deg):
    rot = rotate(p, deg)
    return (center[0] + rot[0], center[1] + rot[1])