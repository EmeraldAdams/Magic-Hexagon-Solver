#Backtracking algorithm with no heuristic
import time
import tracemalloc

class CSP:
    def __init__(self, variables, domains, constraints, sum_value=38, log_filename="NoHeursitc.txt"):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.sum_value = sum_value
        self.assignment = {'A': 3, 'B': 17}  # Initial assignment is empty
        self.num_assignments = 0
        self.num_backtracks = 0
        self.num_consistency_checks = 0
        self.log_filename = log_filename
        self.log_file = open(log_filename, "w")
        
    def log_assignment(self):
        log_entry = f"Assignment {self.num_assignments}: {self.assignment}\n"
        print(log_entry, end="")  
        self.log_file.write(log_entry) 

    def select_unassigned_variable(self):
        for var in self.variables:
            if var not in self.assignment:
                return var
    
    def order_domain_values(self, var):
        return self.domains[var][:]

    def is_consistent(self, var, value):
        self.num_consistency_checks += 1
        self.assignment[var] = value
        
        for constraint in self.constraints:
            if var in constraint:
                total = 0
                assigned_values = 0
                for v in constraint:
                    if v in self.assignment:
                        total += self.assignment[v]
                        assigned_values += 1
                if assigned_values == len(constraint) and total != self.sum_value:
                    del self.assignment[var]
                    return False
                elif assigned_values < len(constraint) and total >= self.sum_value:
                    del self.assignment[var]
                    return False
        del self.assignment[var]
        return True

    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return True
        var = self.select_unassigned_variable()
        if var is None:
            return False
        for value in self.domains[var][:]:
            if self.is_consistent(var, value) and value not in self.assignment.values():
                self.assignment[var] = value
                self.num_assignments += 1
                if self.num_assignments <= 20:
                    self.log_assignment()
                if self.backtrack():
                    return True
                del self.assignment[var]
        self.num_backtracks += 1
        return False

    def solve(self):
        tracemalloc.start()
        start_time = time.time()
        solution_found = self.backtrack()
        end_time = time.time()
        execution_time = end_time - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.log_file.close()
        return {
            'solution': self.assignment if solution_found else None,
            'num_assignments': self.num_assignments,
            'num_backtracks': self.num_backtracks,
            'num_consistency_checks': self.num_consistency_checks,
            'execution_time': execution_time,
            'memory_usage': peak
        }

# Test case
if __name__ == "__main__":
    variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
    domains = {var: list(range(1, 20)) for var in variables}
    constraints = [
        ['A', 'B', 'C'],
        ['D', 'E', 'F', 'G'],
        ['H', 'I', 'J', 'K', 'L'],     
        ['M', 'N', 'O', 'P'],
        ['Q', 'R', 'S'],
        ['A', 'D', 'H'],
        ['B', 'E', 'I', 'M'],
        ['C', 'F', 'J', 'N', 'Q'],
        ['G', 'K', 'O', 'R'],
        ['L', 'P', 'S'],
        ['H', 'M', 'Q'],
        ['D', 'I', 'N', 'R'],  # Extra constraint
        ['A', 'E', 'J', 'O', 'S'],  # Extra constraint
        ['B', 'F', 'P', 'K'],
        ['C', 'G', 'L']
    ]
    
    sum_value = 38

    csp = CSP(variables, domains, constraints, sum_value)
    result = csp.solve()
    solution = result['solution']
    print("With No heuristic")
    print(solution)

    print(f"Number of assignments: {result['num_assignments']}")
    print(f"Number of backtracks: {result['num_backtracks']}")
    print(f"Number of consistency checks: {result['num_consistency_checks']}")
    print(f"Execution time: {result['execution_time']} seconds")
    print(f"Peak memory usage: {result['memory_usage'] / 1024} KB")
