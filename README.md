# 3-SAT Problem Solver Program
具体实现方法详见代码注释。
# 使用方法：
将待求解的问题集的文件夹与程序放在同一目录下
运行程序，会在控制台print每个文件的可满足性，最后会新建一个ans.txt文件并自动打开。  

**注意**：
- 由于本人编程水平有限，目前只会使用非常简易的列表嵌套储存数据，且并未使用类，所有功能都使用函数实现。
- 代码中很多被#和"""注释掉的部分大多是用于调试
- DPLL算法运算50组数据的时间大约为2秒，CDCL的时间大约为16秒

# DPLL介绍
主体部分为`DPLL(assign, Matrix)`函数
运用 Unate Propagation 和 Unit Propagation 对语句进行判断，并推断出变量的布尔值。原本也编写了 Pure Literal Elimintaion的推导方法，但由于反复遍历所有列表耗时过久，随将其变为字符串注释。
之后用`confliction(assign, m)`函数检测冲突
若变量尚未全部赋值，则挑选变量进行真假赋值
其中，挑选变量的方法为：优先考虑出现次数最多的变量，其次考虑最长子句中的变量。
对`DPLL()`函数进行递归，最终判断是否可满足

# CDCL介绍
主体部分为`CDCL(assign, Matrix)`函数
使用无限循环，在出现矛盾时设旗帜为`False`，未出现矛盾则输出`True`.
当出现矛盾时，判断当前决定的等级。
- 如果等级为0级，说明溯源到根节点依然无法满足，则此命题无法满足。
- 如果等级不为0，等级降低一级，并把assign倒退回相应位置。同时学习到新的语句，即当前`decisions`的否定形式。从上一级重新开始推导和赋值。
过程中使用列表`trail`记录`assign`的trail
赋值部分与`DPLL`方法相同  
&nbsp;
# 尚未解决的问题
1. 理论上CDCL方法的速度应当快于DPLL，但在我的程序中DPLL远快于CDCL
2. 我尝试过使用pyinstaller将代码打包成exe文件，但最后生成的exe文件在双击后会一闪而过且并未执行（并非因为程序执行完自动退出，我在最后一行使用了`input("Press enter to exit.")`阻止程序自动退出），尚不清楚问题的原因。
