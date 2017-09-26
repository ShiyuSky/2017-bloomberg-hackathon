
# coding: utf-8

# In[3]:

from math import pi, atan, degrees
import socket
import sys
import random
import time


# In[4]:

def run(user, password, * commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    data = user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sfile = sock.makefile()
        rline = sfile.readline()
#         result = []
        while rline:
            result = rline.split()
#             print(rline.strip())
            rline = sfile.readline()
    return result


# In[5]:

def r(command):
    return run('psyduck', 'Psyduck777', command)


# In[14]:

def put_bomb_now():
    status = r("STATUS")
    bomb_x, bomb_y = status[0][1], status[0][2]
#     print("------ACTION------\nPut bomb at {0} {1}".format(bomb_x, bomb_y))
    r("BOMB {0} {1}".format(bomb_x, bomb_y))


# In[15]:

def is_mine_around():
    status = r("STATUS")
    if status[6] != '0':
        print("Found bomb!!")
        r("BRAKE")
        return [True, [status[8], status[9]]]
    return [False, 0]


# In[16]:

def random_walk():
    i = 0
    r("ACCELERATE {0} {1}".format(random.uniform(5*pi/6, 7*pi/6), 1))
    try:
        while True:
            i = i + 1
#             print(i)
            if i == 200:
                print("Turn")
                r("ACCELERATE {0} {1}".format(random.uniform(5*pi/6, 7*pi/6), 1))
                i = 0
            put_bomb_now()
            nearby_info = is_mine_around()
            if nearby_info[0]:
                nearby_mine = nearby_info[1]
                walk_towards_mine(nearby_mine)
                time.sleep(10)
    except KeyboardInterrupt:
        print('interrupted!')
    except TimeoutError:
        return False


# In[17]:

def get_radian(dx, dy):
    #if dy == dx == 0
    if dy == 0:
            if dx > 0:
                angle = 0
            else:
                angle = pi
    elif dx == 0:
            if dy > 0:
                angle = pi / 2
            else:
                angle = 3 * pi / 2
    else:
        angle = atan(dy/dx)
        if dx > 0:
            if dy < 0:
                angle += (2 * pi)
        else:
            angle += pi
    return 2*pi - angle


# In[18]:

def walk_towards_mine(mine):
    mine_x = float(mine[0])
    mine_y = float(mine[1])
    #Wait until v=0
    print("Walking towards mine")
    while True:
        status = r("STATUS")
        print("Vx={0}   Vy={1}".format(float(status[3]), float(status[4])))
        if abs(float(status[3])) < pow(10, -2) and abs(float(status[4])) < pow(10, -2):
            break
        time.sleep(2)
    x = float(status[1])
    y = float(status[2])
    print("Plane position------({0},{1})".format(x, y))
    print("Mine position------({0},{1})".format(mine_x, mine_y))
    angle_plane_mine = get_radian(mine_x - x, y - mine_y)
    
    r("ACCELERATE {0} 1".format(angle_plane_mine))


# In[19]:

def walk():
    while True:
        random_walk()


# In[ ]:

walk()


# In[ ]:



