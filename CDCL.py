import os
import sys
from pathlib import Path
import time

def read_folder(folder_name):
    path = sys.path[0] + "\\" + folder_name
    files = os.listdir(path)
    ordered_list = []
    for file in files:
        position = path+'\\'+ file
        ordered_list.append(int(Path(position).stem))
        ordered_list.sort()
    #print(ordered_list)
    for i in ordered_list:
        i = str(i) + ".txt"
        yield str(path +'\\' + i)


def SAT():
    ans = []
    count = 0
    for file in read_folder('3SAT_50_217'):
        count += 1
        rf = open(file,'r')
        lst = []
        while True:
            line = rf.readline()
            clause_str = line.strip().split()
            clause = [int(literal) for literal in clause_str]
            if not line:
                break
            lst.append(clause)

        tot = []
        for clause in lst:
            for x in clause:
                if abs(x) not in tot:
                    tot.append(abs(x))
        tot.sort()
        rf.close()
        Matrix0 = lst[1:]
        columns = len(tot) - 1
        
        step_dict = {'unate_propagation': 0, 'unit_propagation': 0, 'pure_literal_elimination': 0, 'assignment': 0}

        
        #print(Matrix0)
        
        variables = [-1] * columns  # 初始赋值全部为“-1”
        #print(variables)
        #print()

        def deduction(assignment:list, Matrix):
            #print(f"\n开始执行推导: assignment={assignment}")
            
            assignment_saved = [x for x in assignment] #复制初始assign列表
            m_copy = [[x for x in c] for c in Matrix]
            for clause in m_copy:
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
                #print(f"\tunassigned = {unassigned}")
                #print(f"clause = {clause}")

                # Unate Propagation
                # 当一个子句存在为真的文字时，可以从子句集合中删除
                if Truthvalue:
                    #print(f"执行 unate propagation: 删除{clause}")
                    c = m_copy.index(clause)
                    m_copy[c] = []
                    step_dict["unate_propagation"] += 1
                    continue
                    # 若for循环进行到这一步未continue，说明已赋值的变元全部为False
                    
                # Unit Propagation
                if len(unassigned) == 1:
                    # 只有一个文字没有赋值，其余文字全部为false，将其赋值使子句为真
                    #print("执行unit propagation")
                    x = unassigned[0]
                    idxx = abs(x) -1
                    if x > 0:
                        assignment[idxx] = 1
                    else:
                        assignment[idxx] = 0
                    step_dict["unit_propagation"] += 1
            m_copy = [m for m in m_copy if m]
            #print(Matrix)
                # 删除空子句（即被判断为真的子句）

            # 以下给出了纯文字消除的代码，但由于该方法不够经济，以字符串的形式注释掉了。
            '''# Pure literal elimination
            #print("纯文字消除")
            #print(f"\t**{assignment}")
            ''for x in range(1, columns+1):
                if assignment[x-1] != -1:
                    #print(f"{x} 已被赋值，跳过。")
                    continue
                #print(f"x={x}")
                case1 = not any(x in clause for clause in m_copy)
                case2 = not any(-x in clause for clause in m_copy)
                if case1 and case2:
                    # 任一子句中都没有变元x，跳过
                    #print("skipped")
                    continue
                elif case1 and not case2:
                    #print(f"case1: 变元{x}的肯定形式不在任何一个子句中")
                    # 如果变元x全部为否定形式：
                    for clause in m_copy:
                        if -x in clause:
                            # 如果有包含-x的子句：将x赋值false，删除此子句
                            assignment[x-1] = 0
                            c = m_copy.index(clause)
                            m_copy[c] = []
                            step_dict["pure_literal_elimination"] += 1       
                elif case2 and not case1:
                    #print(f"case2: 变元{x}的否定形式不在任何一个子句中")
                    # 如果变元x全部为肯定形式
                    for clause in m_copy:
                        if x in clause:
                            # 如果包含x的子句，将x赋值为true，删除子句
                            assignment[x-1] = 1
                            c = m_copy.index(clause)
                            m_copy[c] = []
                            step_dict["pure_literal_elimination"] += 1''

                m_copy = [m for m in m_copy if m]   # 删除空子句
                #print(Matrix)'''
                
            if assignment == assignment_saved:
                #print("assignment == assignment_saved")
                return assignment, Matrix
            else:
                #print(f"下一次推导，assignment = {assignment}")
                return deduction(assignment, m_copy)
                        
                    
        def confliction(assign:list, Matrix):    # 冲突检测
            #print("冲突检测")
            Matrix = [m for m in Matrix if m]
            #print(Matrix)
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


        def CDCL(assign:list, Matrix):
            # assign 初始全为 -1
            trail = [assign]
            decisions = []
            assignTrue = assign
            m0 = [[c for c in r] for r in Matrix]
            while True:
                # 赋值推导
                flag = True
                x, m = deduction(assignTrue, m0)
                assign = x
                if m == []:
                    return True
                elif not confliction(x, m):
                    # 冲突检测
                    #print("检测到冲突")
                    flag = False
                #print("完成冲突检测")
                #print("assign:")
                #print(assign)
                
                #print("\ndecisions:", decisions, "\n")
                if not flag:
                    #print("\n错误decisions:", decisions, "\n")
                    # 判断当前决策层，如果当前为0层，返回unsatisfiable
                    if decisions == []:
                        return False
                    else:
                        neg_curr_deci = [-x for x in decisions]
                        decisions.pop() # 此处last_decision就是变量的序数，回退上一次决定
                        m0.append(neg_curr_deci) # 增加一条学到的子句
                        trail.pop()
                        if len(trail) == 0:
                            return False
                        #print(f"##len_Trail = {len(trail)}")
                        #print(trail)
                        assignTrue = trail[-1]
                        #print("##退回上一层")
                        #print(len([x for x in assignTrue if x != -1]))
                        #print(assignTrue)
                        #print()
                        
                elif -1 in assign:
                    #print(f"\ntrail: {trail}\n")
                    # assign 不完整
                    step_dict["assignment"] += 1
                    #print("\n**赋值")

                    # 优先选择最短子句里的变量
                    # 给所有子句长度排序
                    clause_len_dict = {}
                    for clause_id in range(len(m0)):
                        if len(m0[clause_id]) in clause_len_dict.keys():
                            clause_len_dict[len(m0[clause_id])].append(clause_id)
                        else:
                            clause_len_dict[len(m0[clause_id])] = [clause_id]
                            
                    if len(clause_len_dict) >= 3:
                        clause_len_lst = list(clause_len_dict.keys())
                        clause_len_lst.sort()
                        flg = False
                        for clause_len in clause_len_lst:
                            for clause_id in clause_len_dict[clause_len]:
                                for x in m0[clause_id]:
                                    if assign[abs(x) - 1] == -1:
                                        #print(f"变元出现次数全同，给最短子句{Matrix[clause_id]}中未赋值的变元{abs(x)}赋值")
                                        not_appointed = abs(x) - 1
                                        flg = True
                                        break
                                if flg: break
                            if flg: break
                    else:
                        #给所有子句中变量出现次数排序
                        count_dic = {}
                        for clause in m0:
                            for x in clause:
                                if assign[abs(x) - 1] == -1:
                                    if abs(x) in count_dic.keys():
                                        count_dic[abs(x)] += 1
                                    else:
                                        count_dic[abs(x)] = 1
                        most = max(count_dic.values())
                        for key, values in count_dic.items():
                            if values == most:
                                #print(f"给出现次数最多的变元赋值：{key}")
                                not_appointed = key - 1
                                break
                    
                    assignTrue = assign[:]
                    assignTrue[not_appointed] = 1
                        # 赋真
                    decisions.append(not_appointed + 1) #decisions记录新赋值的变元
                    #print(f"新赋值{not_appointed+1}\n")
                    trail.append(assignTrue)
                else:
                    return True
        print(count, CDCL(variables, Matrix0))
        ans.append(str(count)+ ":" + str(CDCL(variables, Matrix0)) + "\n")
    return ans
        #print(step_dict)

start = time.time()
ans = SAT()
with open(sys.path[0] + "\\ans.txt", "w") as f:
    for lines in ans:
        f.write(lines)
end = time.time()
print(f"time = {end - start :.2f}s")
os.startfile(sys.path[0] + "\\ans.txt")
input("Press enter to exit.")