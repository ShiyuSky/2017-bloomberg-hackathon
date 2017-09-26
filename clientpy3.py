from math import pi, asin, atan, acos, degrees, sqrt
from sklearn.preprocessing import normalize
import numpy as np
import socket
import sys
import time
import matplotlib.pyplot as plt


LOOP_SIZE = 2
USER = "a"
PASSWORD = "a"


def run(command):
    data = command + "\n"
    sock.sendall(bytes(data, "utf-8"))
    sfile = sock.makefile()
    rline = sfile.readline()
    result = rline.split()
    return result


def is_equal(x, y):
    return (x - y) < 0.1

def get_radian(dx, dy):
    angle = atan(dy/dx)
    if dx > 0:
        if dy < 0:
            angle += (2 * pi)
    else:
        angle += pi
    return 2*pi - angle


#TODO pub bomb in front of plane
def put_bomb_now():
    status = run("STATUS")
    bomb_x, bomb_y = status[0][1], status[0][2]
    run("BOMB {0} {1}".format(bomb_x, bomb_y))


def scan_neighbourhood():
    status = run("STATUS")
    if status[6] != '0':
        bomb_x = float(status[8])
        bomb_y = float(status[9])
        return (True, (bomb_x, bomb_y))
    return (False, None)


# assumption:
#   - current v != 0
def walk_to_mine(mine):
    print("Walking towards ", mine)

    status = run("STATUS")
    V = np.array([float(status[3]), float(status[4])]).reshape(1,2)
    prev_V_magnitude = np.linalg.norm(V)
    print(prev_V_magnitude)

    while True:
        status = run("STATUS")
        plane_x = float(status[1])
        plane_y = float(status[2])
        if mine[0] == plane_x and mine[1] == plane_y:
            return
        D = np.array([mine[0]-plane_x, mine[1]-plane_y]).reshape(1,2)
        D_norm = normalize(D)
        V = np.array([float(status[3]), float(status[4])]).reshape(1,2)
        V_norm = normalize(V)
        V_magnitude = np.linalg.norm(V)
        prev_acc = V_magnitude - prev_V_magnitude
        coefficient = prev_acc / prev_V_magnitude
        print(coefficient)
        prev_V_magnitude = V_magnitude
        acc = V_magnitude * coefficient

        A = (D_norm - V_norm) * acc
        A_norm = normalize(A)
        accAngle = get_radian(A_norm[0][0], -A_norm[0][1])
        run("ACCELERATE {0} 1".format(accAngle))


def walk(mines):
    walk_to_mine(mines[0])



def add_new_mine(mines, newMine):
    for mine in mines:
        if mine[0] == newMine[0] and mine[1] == newMine[1]:
            return
    print("Added new mine ({0},{1})".format(newMine[0], newMine[1]))
    mines.append(newMine)


def get_acc():
    run("ACCELERATE {0} 1".format(pi))
    status = run("STATUS")
    v_x, v_y = float(status[3]), float(status[4])
    print(v_x, v_y)
    time.sleep(1)
    status = run("STATUS")
    v_x, v_y = float(status[3]), float(status[4])
    print(v_x, v_y)
    time.sleep(1)
    status = run("STATUS")
    v_x, v_y = float(status[3]), float(status[4])
    print(v_x, v_y)
    time.sleep(1)
    status = run("STATUS")
    v_x, v_y = float(status[3]), float(status[4])
    print(v_x, v_y)
    time.sleep(1)
    status = run("STATUS")
    v_x, v_y = float(status[3]), float(status[4])
    print(v_x, v_y)


def test_engine_acc():
    run("ACCELERATE {0} 1".format(0.5))
    t = 1
    plt.axis([0, 500, 0, 20])
    plt.ion()
    plt.show()
    prev_v = 0
    while True:
        status = run("STATUS")
        v_x = float(status[3])
        v_y = float(status[4])
        v = sqrt(pow(v_x,2) + pow(v_y,2))
        plt.scatter(prev_v, v-prev_v)
        plt.pause(0.0001)
        prev_v = v
        t = t + 1



def scan_map():
    print("Start scanning map")
    mines = []
    numOfMines = 0
    configurations = run("CONFIGURATIONS")
    mapHeight = float(configurations[4])
    scanRadius = float(configurations[8])
    accAngle = acos(2*scanRadius/mapHeight)
    run("ACCELERATE {0} 1".format(accAngle))
    while True:
        put_bomb_now()
        nearbyInfo = scan_neighbourhood()
        if nearbyInfo[0]:
            add_new_mine(mines, nearbyInfo[1])
            if len(mines) == LOOP_SIZE:
                print("Finished scanning!")
                print("Mine list:\n", mines)
                return mines
     

HOST, PORT = "localhost", 17429
data = USER + " " + PASSWORD + "\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(bytes(data, "utf-8"))
print("Connected")

test_engine_acc()

# get_acc()

# scan map to collect some mine positions
# scan_map()

# walk([[6163.717629646693, 7435.567005361096]])