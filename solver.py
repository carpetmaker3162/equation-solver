import numpy as np

def solve_system(coefficients, eq):
    inv_coefficients = np.linalg.inv(coefficients);
    solution = np.dot(inv_coefficients, eq)
    return solution
