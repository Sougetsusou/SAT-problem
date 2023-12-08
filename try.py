variables = [None] * 4
Clauses = (1, 2, 3), (1, 2, -3), (-1, 2, 4), (-1, 2, -4)
# 还未优化完毕， 需要主动赋初始值
def satisfiable(variables, Clauses):
    for a_clause in Clauses:
        truth_value = 0
        for prop in a_clause:
            idx = int((prop ** 2) ** 0.5) -1
            if prop < 0:
                truth_value += (1-variables[idx])
            else:
                truth_value += (variables[idx])
        if truth_value == 0:
            return False
    print(variables)
    return True

def SAT(variables, Clauses, assignment):
    if None in variables:
        print(variables)
        variables[variables.index(None)] = assignment
        return SAT(variables, Clauses, 0) or SAT(variables, Clauses, 1)    
    else:
        return satisfiable(variables, Clauses)
    
def SAT_enumeration(variables, Clauses):
    return SAT(variables, Clauses, 0) or SAT(variables, Clauses, 1)
print(SAT_enumeration(variables, Clauses))
#print(SAT(variables, Clauses, 0) or SAT(variables, Clauses, 1))