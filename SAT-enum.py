variables = [None] * 4
Clauses = (1, 2), (-1, -2), (1, -2), (-1, 2)

def satisfiable(variables, Clauses):
    for a_clause in Clauses:
        truth_value = 0
        for prop in a_clause:
            idx = int(abs(prop)) -1
            if prop < 0:
                truth_value += (1-variables[idx])
            else:
                truth_value += (variables[idx])
        if truth_value == 0:
            return False
    print(variables)
    return True

def SAT(variables, Clauses, assignment):
    if None not in variables:
        return satisfiable(variables, Clauses)
    else:
        print(variables)
        Nvariables = variables[:]
        Nvariables[Nvariables.index(None)] = assignment
        return SAT(Nvariables, Clauses, 0) or SAT(Nvariables, Clauses, 1)
    
def SAT_enumeration(variables, Clauses):
    return SAT(variables, Clauses, 1) or SAT(variables, Clauses, 0)


print(SAT_enumeration(variables, Clauses))
