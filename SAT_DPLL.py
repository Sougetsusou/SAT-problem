def SAT():
    rows = int(input("请输入子句数量："))
    columns = int(input("请输入变元数量："))
    
    Matrix0 = [[0 for x in range(columns)] for y in range(rows)]
    
    step_dict = {'unate_propagation': 0, 'unit_propagation': 0, 'pure_literal_elimination': 0, 'assignment': 0}

    for i in range(rows):
        clause = input(f"请输入第{i+1}个子句，用逗号分隔变元：")
        lst = clause.split(",")
        lst2 = []
        for strings in lst:
            lst2.append(int(strings))
        Matrix0[i] = lst2
    
    print(Matrix0)
    
    variables = [-1] * columns  # 初始赋值全部为“-1”
    print(variables)
    print()

    def deduction(assignment:list, Matrix):
        print(f"assignment={assignment}")
        assignment_saved = assignment.copy()
        for clause in Matrix:
            unassigned = []
            Truthvalue = 0
            for variable in clause:
                idx = abs(variable)-1   
                # 变元的绝对值减1 即是变元对应在列表中的index
                if assignment[idx] == -1:
                    unassigned.append(variable) 
                elif variable > 0:                          # 如果变元是肯定形式
                    Truthvalue += assignment[idx]           # 真值统计加上变元的真值：真为1，假为0
                elif variable < 0:                          # 如果变元是否定形式
                    Truthvalue += (1-assignment[idx])       # 真值统计加上变元的真值：假为1，真为0
            print(f"\tunassigned = {unassigned}")
            print(f"clause = {clause}")

            # Unate Propagation
            # 当一个子句存在为真的文字时，可以从子句集合中删除
            if Truthvalue:
                print(f"执行 unate propagation: {clause}")
                c = Matrix.index(clause)
                Matrix[c] = []
                step_dict["unate_propagation"] += 1
                continue
                # 若for循环进行到这一步未continue，说明已赋值的变元全部为False
                
            # Unit Propagation
            if len(unassigned) == 1:
                # 只有一个文字没有赋值，其余文字全部为false，将其赋值使子句为真
                print("执行unit propagation")
                x = unassigned[0]
                idxx = abs(x) -1
                if x > 0:
                    assignment[idxx] = 1
                else:
                    assignment[idxx] = 0
                step_dict["unit_propagation"] += 1
        Matrix = [m for m in Matrix if m]
        print(Matrix)
            # 删除空子句（即被判断为真的子句）

                 
        # Pure literal elimination
        print("纯文字消除")
        print(f"\t**{assignment}")
        for x in range(1, columns+1):
            print(f"x={x}")
            case1 = not (x in clause for clause in Matrix)
            case2 = not (-x in clause for clause in Matrix)
            if case1 and case2:
                # 任一子句中都没有变元x，跳过
                print("skipped")
                continue
            elif case1 and not case2:
                print(f"case1: 变元{x}的肯定形式不在任何一个子句中")
                # 如果变元x全部为否定形式：
                if assignment[x-1] == 1:
                    return False, Matrix
                for clause in Matrix:
                    if -x in clause:
                        # 如果有包含-x的子句：将x赋值false，删除此子句
                        assignment[x-1] = 0
                        c = Matrix.index(clause)
                        Matrix[c] = []
                        step_dict["pure_literal_elimination"] += 1       
            elif case2 and not case1:
                print(f"case2: 变元{x}的否定形式不在任何一个子句中")
                # 如果变元x全部为肯定形式
                if assignment[x-1] == 0:
                    return False, Matrix
                for clause in Matrix:
                    if x in clause:
                        # 如果包含x的子句，将x赋值为true，删除子句
                        assignment[x-1] = 1
                        c = Matrix.index(clause)
                        Matrix[c] = []
                        step_dict["pure_literal_elimination"] += 1

            Matrix = [m for m in Matrix if m]   # 删除空子句
            print(Matrix)
        
        if assignment == assignment_saved:
            print("assignment == assignment_saved")
            return assignment, Matrix
        else:
            return deduction(assignment, Matrix)
                    
                 
            
    def confliction(assign:list, Matrix):    # 冲突检测
        print("冲突检测")
        Matrix = [m for m in Matrix if m]
        print(Matrix)
        for clause in Matrix:
            flag = 0
            Truthvalue = 0
            for variable in clause:
                idx = abs(variable)-1
                print(assign[idx])
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



    def DPLL(assign:list, Matrix): 
        x, m = deduction(assign, Matrix)
        m1 = m.copy()
        m2 = m.copy()
        if x == False:
            return False
        else:
            assign = x
            # 赋值推导

        if not confliction(assign, m):
            # 冲突检测
            print("检测到冲突")
            return False
        print("完成冲突检测")
        print(assign)
        if -1 not in assign:
            # assign 是完整的
            return True
            
        else:
            step_dict["assignment"] += 1
            print("\n**随机赋值")
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
            return DPLL(assignTrue, m1) or DPLL(assignFalse, m2)
                # 递归
                    
    print(DPLL(variables, Matrix0))
    print(step_dict)


SAT()