import re

class Term:
    def __init__(self, c: float = 0.0, v: str = ""):
        self.coefficient = c
        self.variable = v

    def __repr__(self):
        return f"{self.coefficient}{self.variable}"

    @classmethod
    def from_string(cls, s: str):
        vars = [c for c in s if c.isalpha()]

        # find the coefficient in the term (probably useless actually since only 1 letter variable names...)
        c = re.findall(r"[-+]?(?:\d*\.*\d+)", s)
        if not c:
            coefficient = -1.0 if "-" in s else 1.0
        else:
            coefficient = float(c[0])
        
        if vars:
            return cls(coefficient, vars[0])
        else:
            return cls(coefficient)

def merge(terms):
    terms = sorted(terms, key=lambda a: a.variable)

    new = []
    vars = set()

    for t in terms:
        vars.add(t.variable)

    for v in vars:
        total = sum([x.coefficient for x in terms if x.variable == v])
        new.append(Term(total, v))

    # sort lexicographically again so that corresponding coefficients are lined up in the A matrix
    new.sort(key=lambda a: a.variable)
    return new

def get_terms(expr):
    left, right = expr.split("=")
    
    if not left.startswith("-"):
        left = ("+" + left).replace(" ", "")
    if not right.startswith("-"):
        right = ("+" + right).replace(" ", "")
    
    # extract all the terms from the left and right sides
    left_terms = [*map(Term.from_string, re.findall(r"[-+]?\d*\.?\d*[a-zA-Z]\b|[-+]?\d*\.?\d+", left))]
    right_terms = [*map(Term.from_string, re.findall(r"[-+]?\d*\.?\d*[a-zA-Z]\b|[-+]?\d*\.?\d+", right))]
    
    # move all terms from right to left
    for term in right_terms:
        left_terms.append(Term(-term.coefficient, term.variable))
    right_terms = []

    # collect like terms
    left_terms = merge(left_terms)
    
    # move constant terms to right side
    for term in left_terms:
        if term.variable == "":
            right_terms.append(Term(-term.coefficient, term.variable)) # move constants to right side
            left_terms.remove(term)
            break
    
    return left_terms, right_terms

def to_matrix(system: tuple, variables: tuple):
    assert len(variables) == len(system), "provide the right number of equations goddammit"

    A = [[0] * len(variables) for _ in range(len(system))]
    B = [[] for _ in range(len(system))]
    variable_pos = {v: i for i, v in enumerate(variables)}

    for i, equation in enumerate(system):
        left, right = equation
        B[i].append(right[0].coefficient) # add right side constant to B matrix

        for term in left:
            idx = variable_pos[term.variable]
            A[i][idx] = term.coefficient
    
    return A, B
