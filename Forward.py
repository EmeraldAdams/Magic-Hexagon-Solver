#Backtracking and Forward Checking propagation
import time
import tracemalloc

class CSP:
    def __init__(self, variables, domains, constraints, sum_value=38, log_filename="Forwardchecking.txt"):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.sum_value = sum_value
        self.assignment = {'A': 3, 'B': 17, }  # Initial assignments 
        self.num_assignments = 0
        self.num_backtracks = 0
        self.num_consistency_checks = 0
        self.log_file = open(log_filename, "w")
        
    def select_unassigned_variable(self):
        for var in self.variables:
            if var not in self.assignment:
                return var

    def order_domain_values(self, var):
        return self.domains[var][:]
    
    def log_assignment(self):
        
        log_entry = f"Assignment {self.num_assignments}: {self.assignment}\n"
        print(log_entry, end="")  # Print to console
        self.log_file.write(log_entry)  # Write to file
        
    def is_consistent(self, var, value):
        self.num_consistency_checks += 1
        if value in self.assignment.values():
            return False
        self.assignment[var] = value
        for constraint in self.constraints:
            if var in constraint:
                total = 0
                assigned_values = 0
                for v in constraint:
                    if v in self.assignment:
                        total += self.assignment[v]
                        assigned_values += 1
                    elif v == var:
                        total += value
                if assigned_values == len(constraint) and total != self.sum_value:
                    del self.assignment[var]
                    return False
                elif assigned_values < len(constraint) and total >= self.sum_value:
                    del self.assignment[var]
                    return False
        del self.assignment[var]
        return True

    def forward_checking(self, var, value):
        self.assignment[var] = value
        temp_domains = {k: v[:] for k, v in self.domains.items()}  # Backup current domains
        for constraint in self.constraints:
            if var in constraint:
                for v in constraint:
                    if v != var and v not in self.assignment:
                        if value in self.domains[v]:
                            self.domains[v].remove(value)
                        # Check for empty domain
                        if not self.domains[v]:
                            self.domains = temp_domains  # Restore domains
                            del self.assignment[var]
                            return False
        return True

    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return True
        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var): # Use a copy of the domain to avoid modification during iteration
            if self.is_consistent(var, value):
                self.assignment[var] = value
                self.num_assignments += 1
                if self.num_assignments<20:
                    self.log_assignment()  # Log each assignment
                original_domains = {k: v[:] for k, v in self.domains.items()}  # Backup the domains
                if self.forward_checking(var, value):
                    if self.backtrack():
                        return True
                del self.assignment[var]
                self.domains = original_domains  # Restore the domains
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
        ['D', 'I', 'N', 'R'],  
        ['A', 'E', 'J', 'O', 'S'],  
        ['B', 'F', 'P', 'K'],
        ['C', 'G', 'L']
    ]
    sum_value = 38
    
    csp = CSP(variables, domains, constraints, sum_value)
    result = csp.solve()
    solution = result['solution']
    print("Forward Checking  ")
    print(solution)

    print(f"Number of assignments: {result['num_assignments']}")
    print(f"Number of backtracks: {result['num_backtracks']}")
    print(f"Number of consistency checks: {result['num_consistency_checks']}")
    print(f"Execution time: {result['execution_time']} seconds")
    print(f"Peak memory usage: {result['memory_usage'] / 1024} KB")
