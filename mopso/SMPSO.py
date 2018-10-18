import numpy as np
import time
from dominanceComparator import DominanceComparator 

class SMPSO:
    def __init__(self, 
                objectives, 
                swarm_size, 
                number_of_variables,
                ub,
                lb,
                max_evaluations, 
                mutation,
                leaders,
                evaluator):

        self.objectives = objectives
        self.swarm_size = swarm_size
        self.number_of_variables = number_of_variables
        self.max_evaluations = max_evaluations
        self.mutation = mutation
        self.leaders = leaders
        self.evaluator = evaluator
        self.speed = np.zeros((self.swarm_size, self.number_of_variables))
        self.delta_max = np.empty(self.number_of_variables)
        self.delta_min = np.emptey(self.number_of_variables)
        for i in xrange(self.number_of_variables):
            self.delta_max[i] = (ub[i] - lb[i]) / 2.0
        self.delta_min = -1.0 * self.delta_max



    def dominance_comparator(self, solution1, solution2):
        function_values1 = [objective(solution1) for objective in self.objectives]
        function_values2 = [objective(solution2) for objective in self.objectives]
        best_is_one = 0
        best_is_two = 0 
        for i in xrange(len(objectives)):
            value_1 = function_values1[i]
            value_2 = function_values2[i]
            if value_1 < value_2:
                best_is_one = 1 
            if value_1 > value_2:
                best_is_two = 1 
        
        if best_is_one > best_is_two:
            result = -1
        elif best_is_one < best_is_two:
            result = 1 
        else:
            result = 0 
        return result

    def create_initial_swarm(self):
        return np.random.random((self.swarm_size, self.number_of_variables))
    
    def evaluate_swarm(self, swarm):
        results = []
        for particle in swarm:
            results.append([objective(particle) for objective in self.objectives])
        
        return np.array(results)
    
    def initialize_velocity(swarm):
        pass
    
    def initialize_particle_best(self,swarm):
        self.particle_best = swarm.copy()
    
    def initialize_global_best(self, swarm):
        
    
    def run(self):
        self.start_computing_time = time.time()

        self.swarm = self.create_initial_swarm()
        self.eval_results = self.evaluate_swarm(self.swarm)
        self.initialize_velocity(self.swarm)
        self.initialize_particle_best(self.swarm)
        self.initialize_global_best(self.swarm)
        self.init_progress()

        while not self.is_stopping_condition_reached():
            self.update_velocity(self.swarm)
            self.update_position(self.swarm)
            self.perturbation(self.swarm)
            self.swarm = self.evaluate_swarm(self.swarm)
            self.update_global_best(self.swarm)
            self.update_particle_best(self.swarm)
            self.update_progress()

        self.total_computing_time = self.get_current_computing_time()