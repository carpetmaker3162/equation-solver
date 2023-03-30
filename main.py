from solver import solve_system
from parser import get_terms
from parser import to_matrix

def solve(raw_input: list):
    system = []
    variables = set()
    
    for equation in raw_input:
        terms = get_terms(equation)
        system.append(terms)
        for term in terms[0]:
            if term.variable: # ONLY SUPPORT 1 CHARACTER VARIABLE NAMES!!
                variables.add(term.variable)

    variables = list(variables)
    variables.sort()
    
    A, B = to_matrix(system, variables)
    solution = solve_system(A, B)
    ans = {}

    for i, val in enumerate(solution):
        ans[variables[i]] = val[0]

    return ans

if __name__ == "__main__":
    N = int(input("Number of equations in system: "))
    system = []

    for i in range(N):
        system.append(input(f"({i}): ").strip())

    ans = solve(system)

    for variable, val in ans.items():
        print(f"{variable} = {val}")
