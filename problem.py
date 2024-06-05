import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
from node import *

class Problem:

    fig = plt.figure(figsize=(8,6))
    ax = plt.axes(projection='3d')

    def __init__(self, filename):
        self.X, self.Y, self.Z = self.load_state_space(filename)
        self.width = len(self.X)
        self.height = len(self.Y)

    def load_state_space(self, filename):
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        img = cv2.GaussianBlur(img, (5, 5), 0)

        h, w = img.shape

        X = np.arange(w)
        Y = np.arange(h)
        Z = img
        return X, Y, Z

    def get_goal(self):
        return np.amax(self.Z)

    def get_evaluation_func(self, state):
        x, y = state.get_value()
        return self.Z[x][y]

    def get_initial_state(self):
        x = random.randrange(0, self.height)
        y = random.randrange(0, self.width)
        return (x, y)

    def get_dst_pos(self, action, x, y):
        if action == 'L':
            y -=1 
        elif action == 'R':
            y += 1
        elif action == 'U':
            x -= 1
        elif action == 'D':
            x += 1
        elif action == 'UL':
            x -=1
            y -=1
        elif action == 'UR':
            x -= 1
            y += 1
        elif action == 'DL':
            x +=1 
            y -= 1
        elif action == 'DR':
            x += 1
            y += 1
        return x, y


    def get_successor_by(self, state, action):
        x, y = state.get_value()
        x_dst, y_dst = self.get_dst_pos(action, x, y)
        if (x_dst >= 0 and x_dst < self.height) and (y_dst >= 0 and y_dst < self.width):
            return Node((x_dst, y_dst), state)
        return None


    def get_successors(self, state):
        result = []
        for action in ['L', 'R', 'U', 'D', 'UL', 'UR', 'DL', 'DR']:
            succ = self.get_successor_by(state, action)
            if succ != None:
                result.append(succ)
        return result
    
    def random_near_successor(self, state):
        successors = self.get_successors(state)
        return random.choice(successors)

    def goal_test(self, state):
        if self.get_evaluation_func(state) == self.get_goal():
            return True 
        return False

    def get_path_helper(self, state):
        path = [state]
        while path[0].get_parent() is not None:
            path.insert(0, path[0].get_parent())
        return path

    def get_path(self, state):
        path_helper = self.get_path_helper(state)
        path = []
        for ele in path_helper:
            x, y = ele.get_value()
            z = self.get_evaluation_func(ele)
            path.append((x, y, z))
        return path

    def show(self):
        X_draw, Y_draw = np.meshgrid(self.X, self.Y)
        Problem.ax.plot_surface(X_draw, Y_draw, self.Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
   
    def draw_path(self, path):
        x = []
        y = []
        z = []
        for ele in path:
            x.append(ele[1])
            y.append(ele[0])
            z.append(ele[2])
        Problem.ax.plot(x, y, z, 'r-', zorder=3, linewidth=0.5)
        plt.show()


