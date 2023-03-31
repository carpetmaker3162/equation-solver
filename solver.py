def dot(A, B):
    assert len(A) == len(B)
    ans = 0
    for i in range(len(A)):
        ans += A[i] * B[i]
    return ans

def multiply(A, B):
    assert len(A[0]) == len(B)
    result = [[0] * len(B[0]) for _ in range(len(A))]
    for r in range(len(A)):
        for c in range(len(B[0])):
            result[r][c] = dot(A[r], [x[c] for x in B])
    return result

def inverse(matrix):
    n = len(matrix)
    inv = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        inv[i][i] = 1
    for i in range(n):
        pivot = matrix[i][i]
        if pivot == 0:
            return None
        for j in range(i, n):
            matrix[i][j] /= pivot
        for j in range(n):
            inv[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
                    inv[j][k] -= factor * inv[i][k]
    return inv

def solve_system(A, B):
    inv_A = inverse(A)
    solution = multiply(inv_A, B)
    return solution
