import networkx as nx
import matplotlib.pyplot as plt
# 创建一个有向图
G = nx.DiGraph()

# 打开文件并读取内容
file_pash ='./修改renderdoc 延迟渲染着色 main.hlsl'
with open(file_pash, 'r') as file:
    content = file.read()
content = content.replace('\t', '')
content = content.replace(';', '')
hlslbase=content.split('\n')
# 删除空格
content_without_spaces = content.replace(' ', '')
content_without_spaces = content_without_spaces.replace('\t', '')
content_without_spaces = content_without_spaces.replace(';', '')
# print(content_without_spaces)



hlsl=content_without_spaces.split('\n')
_hlsl=hlsl

def print_tree_as_dict(hlsl):
    arrtemp=[]
    for sp in hlsl:
        sp = sp.replace('+', '=')
        sp = sp.replace('-', '=')
        sp = sp.replace('*', '=')
        sp = sp.replace('/', '=')
        sp = sp.replace('>', '=')
        sp = sp.replace('<', '=')
        sp = sp.replace('(', '=')
        sp = sp.replace(')', '=')
        sp = sp.replace(',', '=')
        sp = sp.replace('?', '=')
        sp = sp.replace(':', '=')

        sp = sp.split('=')

        # print(sp)
        xyztemp=[]
        for xyz in sp:
            xyz = xyz.split(".")
            # print(xyz)
            xyztemp.append(xyz)

        arrtemp.append(xyztemp)
    return  arrtemp
end=print_tree_as_dict(hlsl)
# print(end[0])


def have_common_substring(str1, str2):
    # 将两个字符串的所有可能子字符串添加到集合中
    set1 = set(str1[i:j + 1] for i in range(len(str1)) for j in range(i, len(str1)))
    set2 = set(str2[i:j + 1] for i in range(len(str2)) for j in range(i, len(str2)))

    # 查找两个集合的交集
    common_substrings = set1.intersection(set2)

    # 如果交集不为空，则存在相同的子字符串
    return len(common_substrings) > 0
def is_valid_index(array, i):
    return 0 <= i < len(array)


# 假设 end 和 hlsl 是已经定义好的列表
# end 是一个嵌套列表，其中每个元素也是一个列表，至少包含一个子列表
# hlsl 是一个与 end 长度相同的列表，用于存储一些与 end 中元素相关联的数据

hlslImgTxtPoint = ""  # 用于构建字符串的变量
hlslImgTxtEdge=''

nodes=[]
edges=[]
# 遍历 end 列表中的每个元素
for i, hlsl_value in enumerate(hlsl):
    # 为每个元素构建并追加到 hlslImgTxtPoint 字符串中
    # hlslImgTxtPoint += "id"+str(i)+'[label = "'+str(hlslbase[i])+'"];\n'

    # 获取 end 列表中当前元素的子列表
    children = end[i]

    # 从第二个子元素开始遍历（索引为1，因为通常列表从0开始）
    for j in range(1, len(children)):
        body = children[j][0]  # 获取当前子元素的“身体”

        # 逆序遍历从当前元素到列表开始的元素，寻找匹配的“头”
        for headId in range(i-1, -1, -1):
            head = end[headId][0][0]  # 获取当前头元素的“头”

            # 如果找到了匹配的“头”和“身体”，打印 headId 并跳出循环
            childId = -1
            if head == body:
                if (is_valid_index(end[headId][0], 1) & is_valid_index(end[i][j], 1)):
                    if (have_common_substring(end[headId][0][1], end[i][j][1])):
                        childId = headId
                        fatherId=i
                        # hlslImgTxtEdge += "id" + str(childId) + '->id' + str(fatherId) + ";\n"
                        nodes.append(i)
                        edges.append((childId,fatherId))
                        # print(headId)
                        break

            # 最终，hlslImgTxtPoint 将包含所有构建的节点定义字符串

# nodes
# edges


# 添加节点
G.add_nodes_from([1, 2, 3, 4])
G.add_nodes_from(nodes)
print(nodes)

 
# 添加有向边
# G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)])
G.add_edges_from(edges)
print(edges)

 
# 绘制图形
# pos = nx.spring_layout(G)  # 使用spring布局算法来计算节点位置
# nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=200, font_size=8, font_weight='bold', arrowsize=20)

# 显示图形
# plt.title('有向连通图示例')
# plt.show()

_parent_nodes = []
def getFather(parent_nodes:int):
    for i in parent_nodes:
        _parent_nodes.append(i)
        temp = list(G.predecessors(i))
        if(not temp == []):
            getFather(temp)
        
# 获取节点2的所有父节点
# parent_nodes = list(G.predecessors(235))
getFather([235])
print(_parent_nodes)



for i, hlsl_value in enumerate(hlsl):
    # 为每个元素构建并追加到 hlslImgTxtPoint 字符串中
    if i in _parent_nodes:
        hlslImgTxtPoint += "id"+str(i)+'[label = "'+str(hlslbase[i])+'"];\n'

    # 获取 end 列表中当前元素的子列表
    children = end[i]

    # 从第二个子元素开始遍历（索引为1，因为通常列表从0开始）
    for j in range(1, len(children)):
        body = children[j][0]  # 获取当前子元素的“身体”

        # 逆序遍历从当前元素到列表开始的元素，寻找匹配的“头”
        for headId in range(i-1, -1, -1):
            head = end[headId][0][0]  # 获取当前头元素的“头”

            # 如果找到了匹配的“头”和“身体”，打印 headId 并跳出循环
            childId = -1
            if head == body:
                if (is_valid_index(end[headId][0], 1) & is_valid_index(end[i][j], 1)):
                    if (have_common_substring(end[headId][0][1], end[i][j][1])):
                        childId = headId
                        fatherId=i
                        if(childId in _parent_nodes):
                            hlslImgTxtEdge += "id" + str(childId) + '->id' + str(fatherId) + ";\n"
                        nodes.append(i)
                        edges.append((childId,fatherId))
                        # print(headId)
                        break

print(hlslImgTxtPoint+hlslImgTxtEdge)
txt="digraph G {\n    node [shape=box, style=filled, fontcolor=white];\n    edge [color=gray];\n"+hlslImgTxtPoint+hlslImgTxtEdge+"}"
# print(txt)

with open('hlsl.txt', 'w') as file:
    file.write(txt)
print('outstr')
outstr =[]
for i ,value in  enumerate(_hlsl):
    if(i in _parent_nodes):
        outstr.append(value)
print(';\n'.join(outstr)+";")