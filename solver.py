import numpy as np

def solve_system(A, B):
    inv_A = np.linalg.inv(A);
    solution = np.dot(inv_A, B)
    return solution
