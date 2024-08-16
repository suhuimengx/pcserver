import xlrd as xd
import numpy as np

data = xd.open_workbook('sandtable.xls')
sheet1 = data.sheet_by_name('1_distance')
DijDis = []
for r in range(sheet1.nrows): #将表中数据按行逐步添加到列表中，最后转换为list结构
    data1 = []
    for c in range(sheet1.ncols):
        data1.append(sheet1.cell_value(r,c))
    DijDis.append(list(data1))   
print(DijDis)

'''
sheet2 = data.sheet_by_name('1_route')
DijRoute = []
for r in range(sheet2.nrows): #将表中数据按行逐步添加到列表中，最后转换为list结构
    data1 = []
    for c in range(sheet2.ncols):
        data1.append(sheet2.cell_value(r,c))
    DijRoute.append(list(data1))   
print(DijRoute[3][6])
'''

DijRoute = [
    [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]],
    [[1], [], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 6, 5], [1, 2, 3, 4, 6], [], [], [], [], [], []],
    [[2], [2, 3, 1], [], [2, 3], [2, 3, 4], [2, 3, 4, 6, 5], [2, 3, 4, 6], [], [], [], [], [], []],
    [[3], [3, 1], [3, 1, 2], [], [3, 4], [3, 4, 6, 5], [3, 4, 6], [], [], [], [], [], []],
    [[4], [4, 6, 5, 1], [4, 6, 5, 1, 2], [4, 6, 5, 1, 2, 3], [], [4, 6, 5], [4, 6], [], [], [], [], [], []],
    [[5], [5, 1], [5, 1, 2], [5, 1, 2, 3], [5, 4], [], [5, 4, 6], [], [], [], [], [], []],
    [[6], [6, 5, 1], [6, 5, 1, 2], [6, 5, 1, 2, 3], [6, 5, 4], [6, 5], [], [], [], [], [], []],
    [[7], [], [], [], [], [], [], [], [7, 8], [7, 8, 9], [7, 8, 9, 10], [7, 8, 9, 11], [7, 8, 9, 11, 12]],
    [[8], [], [], [], [], [], [], [8, 9, 10, 7], [], [8, 9], [8, 9, 10], [8, 9, 11], [8, 9, 11, 12]],
    [[9], [], [], [], [], [], [], [9, 10, 7], [9, 10, 7, 8], [], [9, 10], [9, 11], [9, 11, 12]],
    [[10], [], [], [], [], [], [], [10, 7], [10, 7, 8], [10, 7, 8, 9], [], [10, 7, 8, 9, 11], [10, 7, 8, 9, 11, 12]],
    [[11], [], [], [], [], [], [], [11, 12, 10, 7], [11, 12, 10, 7, 8], [11, 12, 10, 7, 8, 9], [11, 12, 10], [], [11, 12]],
    [[12], [], [], [], [], [], [], [12, 10, 7], [12, 10, 7, 8], [12, 10, 7, 8, 9], [12, 10], [12, 10, 7, 8, 9, 11], []]
]

dataDict={}
dataDict['nCustomer']=0
dataDict['NodeCoor']=[0]
dataDict['status0']=[1,2]
route = [dataDict['status0'][-1]]

dataDict2={}
dataDict2['nCustomer']=0
dataDict2['NodeCoor']=[0]
dataDict2['status0']=[7,8]
#在路径中标记出哪些是目标上下车节点

'''
def ex_route(ind):
    route = [dataDict['status0'][-1]]
    for i in range(1,len(ind)):
        route.append(dataDict['NodeCoor'][ind[i]])
    return route
print(ex_route([0,1,]))
'''
'''
def nd_route(route):
    nodeRoute = [[route[0],0]]
    for i in range(1,len(route)-1):
        nodeRoute.append([route[i],1])
        for j in range(1,len(DijRoute[route[i]][route[i+1]])):
            nodeRoute.append([DijRoute[route[i]][route[i+1]][j],0])
    if len(route)>1:
        nodeRoute.append([route[-1],1])
        for i in range(len(nodeRoute)-1):
            if nodeRoute[i][0] == nodeRoute[i+1][0]:
                nodeRoute[i][1]=1

    nodeRoute_remove = []
    for i in range(len(nodeRoute)):
        if i ==0 or nodeRoute[i] != nodeRoute[i-1]:
            nodeRoute_remove.append(nodeRoute[i])
    return nodeRoute_remove
'''
'''                   
    nodeRoute_remove = []
    for i in range(len(nodeRoute)):
        if i ==0 or nodeRoute[i] != nodeRoute[i-1]:
            nodeRoute_remove.append(nodeRoute[i])
    return nodeRoute_remove
'''  


def panevaluate(nodeRoute):
    dis = 0
    for i in range(len(nodeRoute)-1):
        dis += DijDis[nodeRoute[i][0]][nodeRoute[i+1][0]]
    return dis
print(panevaluate([[2, 1], [3, 0], [4, 0], [6, 1], [5, 0], [4, 1], [6, 0], [5, 1]]))

def insert(req, status, index, nodeRoute, dataDict):
    dataDict['nCustomer'] += 1
    dataDict['NodeCoor'].insert(dataDict['nCustomer'], req[0])
    dataDict['NodeCoor'].append(req[1])
    halfRoute = nodeRoute[0:index+1]
    for i in range(index+1, len(nodeRoute)):
        if nodeRoute[i][1] == 1:
            halfRoute.append(nodeRoute[i])
    minDis = float("inf")
    for seq1 in range(index,len(halfRoute)+1):
        for seq2 in range(seq1+1,len(halfRoute)+2):
            route_copy = halfRoute.copy()
            route_copy.insert(seq1, [dataDict['NodeCoor'][dataDict['nCustomer']],1])
            route_copy.insert(seq2, [dataDict['NodeCoor'][2*dataDict['nCustomer']],1])
            routeEva = panevaluate(route_copy)
            if routeEva < minDis:
                minDis = routeEva
                bestRoute = route_copy
    ex_nodeRoute = []
    for i in range(len(bestRoute)-1):
        ex_nodeRoute.append(bestRoute[i])
        for j in range(1,len(DijRoute[bestRoute[i][0]][bestRoute[i+1][0]])):
            ex_nodeRoute.append([DijRoute[bestRoute[i][0]][bestRoute[i+1][0]][j],0])
    ex_nodeRoute.append(bestRoute[-1])
    for i in range(len(ex_nodeRoute)-1):
        if ex_nodeRoute[i][0]==ex_nodeRoute[i+1][0] and ex_nodeRoute[i][1]+ex_nodeRoute[i+1][1]>0:
            ex_nodeRoute[i][1] = 1
            ex_nodeRoute[i+1][1] =1
    nodeRoute_remove = []
    for i in range(len(ex_nodeRoute)):
        if i ==0 or ex_nodeRoute[i] != ex_nodeRoute[i-1]:
            nodeRoute_remove.append(ex_nodeRoute[i])
    for i in range(len(nodeRoute_remove)-1):
        if nodeRoute_remove[i][0]==nodeRoute_remove[i+1][0] and nodeRoute_remove[i][1]+nodeRoute_remove[i+1][1]>0:
            nodeRoute_remove[i][1] = 1
            nodeRoute_remove[i+1][1] =1
    nodeRoute_remove2 = []
    for i in range(len(nodeRoute_remove)):
        if i ==0 or nodeRoute_remove[i] != nodeRoute_remove[i-1]:
            nodeRoute_remove2.append(nodeRoute_remove[i])
    return nodeRoute_remove2

# print(insert([4,6],[1,2],1,[[1,0], [2,0]],dataDict))
# print(insert([3,5],[1,2],2,[[1,0], [2, 0], [3, 0], [4, 1], [6, 1]],dataDict))
# print(insert([5,4],[1,2],5,[[1,0], [2, 0], [3, 1], [4, 1], [6, 1], [5, 1]],dataDict))
a = [[1,0], [2, 1], [3, 0], [4, 0], [6, 1], [5,1], [4,1]]
b = a.copy()
b.pop(0)
print(insert([5,4],[1,2],6,[[1,0], [2, 1], [3, 0], [4, 0], [6, 1], [5,1], [4,1]],dataDict))
print([[1,0]] + insert([5,4],[1,2],6,b,dataDict))

# print(insert([8,11],[1,2],1,[[8,0]],dataDict2))
# print(insert([9,12],[1,2],1,[[8, 1], [9, 0], [11, 1]],dataDict2))
# print(insert([10,7],[1,2],4,[[8, 1], [9, 1], [11, 1], [12, 1]],dataDict2))