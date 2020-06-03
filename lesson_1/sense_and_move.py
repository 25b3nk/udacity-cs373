'''
Script to move and sense a robot in a 1-D world with red or green cells.
'''

p=[0.2, 0.2, 0.2, 0.2, 0.2]  # Initial belief
print("Initial belief:")
print(p)

world=['green', 'red', 'red', 'green', 'green']  # 1-D World
measurements = ['red', 'red']  # Measurements or Sense
motions = [1,1]  # Motion steps
pHit = 0.6  # Probability that measurement is correct
pMiss = 0.2  # Probability that measurement is wrong (i.e, it sensed red but told green)
pExact = 0.8  # Probability that it moves the correct number of steps
pOvershoot = 0.1  # Probability that it moves one step lesser
pUndershoot = 0.1  # Probability that it moves one step greater


def sense(p, Z):
    '''
    Function to sense the current location of the robot.
    This is similar to `Baye's rule`, where we have a prior
    and calculate posterior based on the measurement
    '''
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q


def move(p, U):
    '''
    Function to move the robot with its inaccurate movement.
    This is similar to `Theorem of total probability`, where
    we calculate the probability of current cell based on
    convolution of prior and movement of robot from surrounding
    cells.
    '''
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q


for k in range(len(measurements)):
    p = sense(p, measurements[k])
    p = move(p, motions[k])

print("Posterior probabilities after two sets of sense and movement:")
print(p)
