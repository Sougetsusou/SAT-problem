def SAT_confliction():
    rows = int(input("请输入子句数量："))
    columns = int(input("请输入变元数量："))
    
    Matrix = [[0 for x in range(columns)] for y in range(rows)]
    
    for i in range(rows):
        clause = input(f"请输入第{i+1}个子句，用逗号分隔变元：")
        lst = clause.split(",")
        lst2 = []
        for strings in lst:
            lst2.append(int(strings))
        Matrix[i] = lst2
    
    print(Matrix)
    
    variables = [-1] * columns
    print(variables)



    def confliction(assign:list):    # 冲突检测
        for clause in Matrix:
            flag = 0
            Truthvalue = 0
            for variable in clause:
                idx = abs(variable)-1
                if assign[idx] == -1:
                    #如果变量未被赋值，此子句不会产生冲突，退出循环
                    flag = 1
                    break
                elif variable > 0:
                    Truthvalue += assign[idx]
                elif variable < 0:
                    Truthvalue += (1-assign[idx])
            if Truthvalue == 0 and flag == 0:
                return False
        return True



    def SAT(assign:list):
        if not confliction(assign):
            return False
        
        if -1 not in assign:
            # assign 是完整的
            for clause in Matrix:
                TruthValue = 0
                for variable in clause:
                    idx = abs(variable) - 1
                        # 变元的绝对值-1 即是变元对应在列表中的index
                    if variable > 0:
                        TruthValue += assign[idx]
                    else:
                        TruthValue += (1-assign[idx])
                        # 如果变元是否定的，0和1互反
                if TruthValue == 0:
                    return False
            return True
            
        else:
            not_appointed = assign.index(-1)
                # 找到未被赋值变量的位置
            assignTrue = assign[:]
            assignTrue[not_appointed] = 1
                # 赋真
            print(assignTrue)
            assignFalse = assign[:]
            assignFalse[not_appointed] = 0
                # 赋假
            print(assignFalse)
            return SAT(assignTrue) or SAT(assignFalse)
                # 递归
                    
    print(SAT(variables))




SAT_confliction()