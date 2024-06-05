from node import * 
from problem import *
import numpy as np 
import math
import sys
import random

class LocalSearchStrategy:  
    
    def hill_climbing(self, problem):
        current = Node (problem.get_initial_state())
        while True:
            neighbors = problem.get_successors(current)
            if not neighbors: # If that state has no neighbor
                break
            best_neighbor = max(neighbors, key=lambda state: problem.get_evaluation_func(state))
            if problem.get_evaluation_func(current) >= problem.get_evaluation_func(best_neighbor):
                break
            current = best_neighbor
        return current


    def random_restart_hill_climbing(self, problem, num_trial):
        current = self.hill_climbing(problem)
        count = 1 
        while count < num_trial and problem.goal_test(current) == False:
            state =  self.hill_climbing(problem)
            if problem.get_evaluation_func(state) > problem.get_evaluation_func(current):
                current = state
            count += 1
        path = problem.get_path(current)
        return path

    # Geman & Geman cooling schedule with c = 1 
    def schedule(self, c = 1): 
        return lambda t: c / (math.log(t + 1))

    def simulated_annealing_search(self, problem, schedule):
        current = Node(problem.get_initial_state())  
        max_iterations = 100000
        for t in range(1, max_iterations + 1):
            
            T = np.float16(schedule(t)) # np.float16 for larger value which T can store
            if T == 0 or problem.goal_test(current):
                path = problem.get_path(current)
                return path
       
            next = problem.random_near_successor(current)
        
            if not next:
                path = problem.get_path(current)
                return path

            current_z = problem.get_evaluation_func(current).astype(np.int16)
            next_z = problem.get_evaluation_func(next).astype(np.int16)

            delta_e = next_z - current_z
            if delta_e > 0:
                current = next
            else: 
                prob = math.exp(delta_e / T)
                if random.uniform(0.0, 1.0) < prob: #random.uniform() return floating number between two numbers (both include)
                    current = next

            if t == max_iterations:
                path = problem.get_path(current)
                return path
        return None


    def local_beam_search(self, problem, k):
        frontier = []
        expanded = []

        # Generate randomly k states
        for i in range(k):
            current = Node(problem.get_initial_state())   
            frontier.append(current)
       
        frontier.sort(key=lambda state: problem.get_evaluation_func(state), reverse=True)
       
        state_highest_evalution = (problem.get_evaluation_func(frontier[0]), frontier[0])
        
        while frontier: 
            p_queue = [] # Priority queue sorts by z value
        
            for state in frontier:
                neighbors = problem.get_successors(state)
                expanded.append(state.get_value())
                
                for neighbor in neighbors:
                    if neighbor.get_value() not in expanded:
                        z_value = problem.get_evaluation_func(neighbor)
                        p_queue.append((z_value, neighbor))
            
            if len(p_queue) == 0:
                best_neighbor = state_highest_evalution[1]
                path = problem.get_path(best_neighbor)
                return path
            
            p_queue.sort(key=lambda z: z[0], reverse=True)
            k_best_neighbor = p_queue[0:k]

            for neighbor in k_best_neighbor: # neighbor in form (z, node)
                if problem.goal_test(neighbor[1]) == True:
                    path = problem.get_path(neighbor[1])
                    return path
                if state_highest_evalution[0] < neighbor[0]:
                    state_highest_evalution = neighbor
                    
            next_frontier = [ele[1] for ele in k_best_neighbor] # ele in form (z, node)
            frontier = next_frontier
        return None

