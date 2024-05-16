import numpy as np


def rotate(vec, angl):
    vec = np.array(vec)
    roll, pitch, yaw = (a * np.pi / 180 for a in angl)
    
    sf, cf = np.sin(roll), np.cos(roll) # x
    st, ct = np.sin(pitch), np.cos(pitch) # y
    sp, cp = np.sin(yaw), np.cos(yaw) # z
    
    sf, cf, st, ct, sp, cp = np.round([sf, cf, st, ct, sp, cp], 10)
    
    Rx = np.array([
        [1, 0,   0],
        [0, cf, -sf],
        [0, sf,  cf],
    ])
    
    Ry = np.array([
        [ct,  0, st],
        [0,   1, 0],
        [-st, 0, ct],
    ])
    
    Rz = np.array([
        [cp, -sp,  0],
        [sp,  cp,  0],
        [0,   0,   1],
    ])
    
    R = np.matmul(Rz, Ry, Rx)
    return np.matmul(R, vec)
     

def trajectory(NED, v, u):
    # NED: angles, pos
    points = []
    
    grav = np.array([0, 0, -9.8])
    
    angl, pos = NED
    
    v = rotate(v, (-a for a in angl))
    u = rotate(u, (-a for a in angl))
    v[2] = -v[2]
    u[2] = -u[2]

    
    while pos[2] > 0:
        if len(points) > 100:
            break
        pos += (v + u + grav)
        points.append(list(pos))
    
    return points
