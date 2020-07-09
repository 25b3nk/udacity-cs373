# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(colors,measurements,motions,sensor_right,p_move):
    """
    Parameters
    ----------
    sensor_right : float
                   This is the probability that the sensor senses the color right
                   else it is the other color
    p_move : float
             This is probabilty that the movement is correct, and if it fails robot
             won't move
    """
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for rowj in range(len(colors[0]))] for col in range(len(colors))]
    # >>> Insert your code here <<<
    for varI in range(len(measurements)):
        p = move(p,motions[varI],p_move)
        p = sense(p,measurements[varI],sensor_right)
#    p = sense(p,'R',1.0)
#    p = move(p,[0,1],1.0)
#    show(p)
#    p = sense(p,'R',1.0)
#    p = move(p,[0,0],1.0)
    return p

def sense(p,Z,sensor_right):
    q = list(p)
    for i,rows in enumerate(colors):
        for j,elements in enumerate(rows):
            Hit = (Z == elements)
            q[i][j] = p[i][j]*(sensor_right*Hit + (1-sensor_right)*(1-Hit))
    s = 0
    for rows in q:
        s = s + sum(rows)
    for i,rows in enumerate(q):
        for j,elements in enumerate(rows):
            q[i][j] = elements*1./s
    return q

def move(p,U,p_move):
    q = [x[:] for x in p]
    for i,rows in enumerate(q):
        for j,elements in enumerate(rows):
            q[i][j] = p[(i-U[0])%len(q)][(j-U[1])%len(q[0])]*p_move + p[i][j]*(1-p_move)
    return q    

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
         
colors1 = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]         
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p) # displays your answer
