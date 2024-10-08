from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import threading, time
from receive import SerialProcessor
from rode import rode_dict
import requests, json
import xlrd as xd
import numpy as np

# serProcessor = SerialProcessor("COM12", 115200)
    
    
"""
插入算法
"""
data = xd.open_workbook('sandtable.xls')
sheet1 = data.sheet_by_name('1_distance')
DijDis = []
for r in range(sheet1.nrows): #将表中数据按行逐步添加到列表中，最后转换为list结构
    data1 = []
    for c in range(sheet1.ncols):
        data1.append(sheet1.cell_value(r,c))
    DijDis.append(list(data1))

DijRoute = [
    [[0],  [1],          [2],  [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]],
    [[1],  [],           [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 6, 5], [1, 2, 3, 4, 6], [], [], [], [], [], []],
    [[2],  [2, 3, 1],    [], [2, 3], [2, 3, 4], [2, 3, 4, 6, 5], [2, 3, 4, 6], [], [], [], [], [], []],
    [[3],  [3, 1],       [3, 1, 2], [], [3, 4], [3, 4, 6, 5], [3, 4, 6], [], [], [], [], [], []],
    [[4],  [4, 6, 5, 1], [4, 6, 5, 1, 2], [4, 6, 5, 1, 2, 3], [], [4, 6, 5], [4, 6], [], [], [], [], [], []],
    [[5],  [5, 1],       [5, 1, 2], [5, 1, 2, 3], [5, 4], [], [5, 4, 6], [], [], [], [], [], []],
    [[6],  [6, 5, 1],    [6, 5, 1, 2], [6, 5, 1, 2, 3], [6, 5, 4], [6, 5], [], [], [], [], [], []],
    [[7],  [],           [], [], [], [], [], [], [7, 8], [7, 8, 9], [7, 8, 9, 10], [7, 8, 9, 11], [7, 8, 9, 11, 12]],
    [[8],  [],           [], [], [], [], [], [8, 9, 10, 7], [], [8, 9], [8, 9, 10], [8, 9, 11], [8, 9, 11, 12]],
    [[9],  [],           [], [], [], [], [], [9, 10, 7], [9, 10, 7, 8], [], [9, 10], [9, 11], [9, 11, 12]],
    [[10], [],           [], [], [], [], [], [10, 7], [10, 7, 8], [10, 7, 8, 9], [], [10, 7, 8, 9, 11], [10, 7, 8, 9, 11, 12]],
    [[11], [],           [], [], [], [], [], [11, 12, 10, 7], [11, 12, 10, 7, 8], [11, 12, 10, 7, 8, 9], [11, 12, 10], [], [11, 12]],
    [[12], [],           [], [], [], [], [], [12, 10, 7], [12, 10, 7, 8], [12, 10, 7, 8, 9], [12, 10], [12, 10, 7, 8, 9, 11], []]
]

dataDict1={}
dataDict1['nCustomer']=0
dataDict1['NodeCoor']=[0]
dataDict1['status0']=[1,2]
route = [dataDict1['status0'][-1]]

dataDict2={}
dataDict2['nCustomer']=0
dataDict2['NodeCoor']=[0]
dataDict2['status0']=[7,8]

# 将两个Dict的引用放入同一个列表，方便线程管理
dataDict_list = [dataDict1, dataDict2]

# 车辆全路径数组
route_array = [
    [[1,0], [2,0]],
    [[7,0], [8,0]],
]

""" 云数据库url """
uni_url_count = ("https://fc-mp-9807717d-5acc-468e-a8a2-2b6850a56613.next.bspapp.com/shapan-count")
uni_url_doc = ("https://fc-mp-9807717d-5acc-468e-a8a2-2b6850a56613.next.bspapp.com/shapan-doc")
uni_url_id = ("https://fc-mp-9807717d-5acc-468e-a8a2-2b6850a56613.next.bspapp.com/shapan-id")

""" 系统开始运行时，获取云数据库初始状态 """
init_count = json.loads(requests.get(uni_url_count).text)["total"]
init_id = json.loads(requests.get(uni_url_id, {"num":init_count}).text)["data"][0]["_id"]

'''
数字孪生端websocket服务创建
'''
app = Flask(__name__)
# 解决前端跨域问题
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = '123456789'
socketio = SocketIO(app, cors_allowed_origins='*')

# 定义路由处理websocket连接
@app.route('/socket.io/')
def socket():
    return jsonify({})

@socketio.on('connect')
def socket_connect():
    """
    监听websocket连接事件
    """

    thread_task = threading.Thread(target=task)
    thread_task.start()
    print('client connected')
    # 开启串口监视线程
    # thread_ser = threading.Thread(target=Process_Serial)
    # thread_ser.start()
    # 开启车辆服务程序
    # for car_id in range(2):
    #     thread_car = threading.Thread(target=Process_Car, args=(car_id,))
    #     thread_car.start()
    #     time.sleep(0.1)
    # 开启云数据库检测线程
    # thread_uni = threading.Thread(target=QueryUniCloud, args=(uni_url_count, uni_url_doc,))
    # thread_uni.start()

def task():
    time.sleep(3)
    socketio.emit('send_message_arrive', {
        "car_id": 0,
        "arrive_id": 6,
    })

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def QueryUniCloud(url_count, url_doc):
    """ 多线程任务
    轮询是否有新数据到来，即实时订单
    @param url_count: 查询数量
    @param url_doc: 获取新数据
    @return:
    """
    global init_count, init_id
    global route_index, route_array, dataDict
    while True:
        # 查询数据库是否有新数据
        current_count = json.loads(requests.get(url_count).text)['total']
        # print("目前数量",current_count)
        if current_count > init_count:
            time.sleep(0.2)
            print("=============收到实时需求=============")
            new_doc = json.loads(requests.get(url_doc, {
                "old_id": init_id,
            }, timeout=3).text)["data"][0]
            # 更新状态量
            init_count += 1
            init_id = new_doc["_id"]
            # 读取订单信息(出发id，到达id，乘车数)
            originId = int(new_doc["originId"]) + 1
            destId = int(new_doc["destId"]) + 1
            req = [originId, destId]
            if originId <= 6: car_id = 0
            else: car_id = 1
            # 插入实时订单
            route_array_temp = route_array[car_id].copy()
            route_array_temp.pop(0) # 扔掉第一个元素再插
            if car_id == 0:
                route_array[car_id] = [[1,0]] + insert(req, route_index[car_id], route_array_temp, dataDict_list[car_id])
            else:
                route_array[car_id] = [[7,0]] + insert(req, route_index[car_id], route_array_temp, dataDict_list[car_id])
            print(route_array[car_id], dataDict_list[car_id], route_index[car_id])
            message = {
                "originId":originId,
                "destId":destId,
                "car_id":car_id,
            }
            socketio.emit('send_message_realTimeOrder',message)
        time.sleep(1.5)

def panevaluate(nodeRoute):
    """ 获取整条路线的全距离
    @param nodeRoute: 整条路线
    """
    dis = 0
    for i in range(len(nodeRoute)-1):
        dis += DijDis[nodeRoute[i][0]][nodeRoute[i+1][0]]
    return dis

def insert(req, index, nodeRoute, dataDict):
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


""" global数据变量 """
# 两个小车的坐标
x0, y0, tag_id0, x1, y1, tag_id1 = 0.0, 0.0, 0, 0.0, 0.0, 0
init_flag = False

# 标志车辆是否到达目标路点，才可进入下一段路径
arrive_flag = [False, False]
tag_id = [0 , 0]
# 标记当前目标route的index
route_index = [0,0]
Action_dict ={
    "move2tag":0,
    "stop2tag":1,
}
WaitTime_dict = {
    "wait_always":0,
    "wait_none":1,
    "wait_2s":2,
}
need2prolong = [(2,3), (6,5), (8,9)]

start = [
    route_array[0][0],
    route_array[1][0],
]
end = [
    route_array[0][1],
    route_array[1][1],
]

route_begin = [
    [2,6],
    [9,11],
]



def Process_Car(car_id):
    """ 车辆服务函数，控制车辆按路径行驶
    @param car_id: 车辆编号
    """
    global route_array, start, end, arrive_flag, route_index
    global serProcessor, dataDict_list
    # 插入获取车辆初始路线
    route_array_temp = route_array[car_id].copy()
    route_array_temp.pop(0)
    if car_id == 0:
        route_array[car_id] = [[1,0]] + insert(route_begin[car_id], route_index[car_id], route_array_temp, dataDict_list[car_id])
    else:
        route_array[car_id] = [[7,0]] + insert(route_begin[car_id], route_index[car_id], route_array_temp, dataDict_list[car_id])
    print(route_array[car_id])
    temp_nCustomer = dataDict_list[car_id]["nCustomer"]
    temp_point = start[car_id]
    while True:
        if route_index[car_id] < len(route_array[car_id]) - 1:
            # if temp_nCustomer < dataDict["nCustomer"]:
            #     temp_nCustomer = dataDict["nCustomer"]
            #     route_index[car_id] -= 1
            #     start[car_id] = temp_point
            #     print("realtime order2")
            '''更新车辆终点'''
            end[car_id] = route_array[car_id][route_index[car_id] + 1]
            '''获取识别id'''
            route_key = (start[car_id][0], end[car_id][0])
            if route_key in need2prolong:
                virtual_next_rode = 1 if route_key[0] <= 6 else 11
                if (route_index[car_id] + 1) < len(route_array[car_id]) - 1:
                    virtual_next_rode = route_array[car_id][route_index[car_id] + 2][0]
                route_key = (start[car_id][0], end[car_id][0], virtual_next_rode)
            target_TagId = rode_dict[route_key]
            target_route = end[car_id]
            '''获取行动指令'''
            action_key = "move2tag"
            wait_time_key = "wait_none"
            if target_route[1] != 0:
                # 如果属于乘客上下车点, 则需停车
                action_key = "stop2tag"
                wait_time_key = "wait_2s"
                if route_index[car_id] == len(route_array[car_id]) - 2:
                    # 如果是最后一个目标点，一直停车
                    wait_time_key = "wait_always"
            '''下发识别指令'''
            # serProcessor.send_instruct(car_id, target_route[0], target_TagId, Action_dict[action_key], WaitTime_dict[wait_time_key])
            '''等待车辆行驶至目标点'''
            while not arrive_flag[car_id]:
                # 处理动态插入bug
                if route_array[car_id][route_index[car_id] + 1][1] != end[car_id][1]:
                    """ 若小车运行过程中终点任务发生变化，重新下发任务 """
                    print("realtime order1")
                    break
                # 车辆到达目标Tag后开启下一段路程
                if tag_id[car_id] == target_TagId:
                    print("\n-stop arrive\n")
                    # 若车辆停留，则闪烁图标
                    if end[car_id][1] != 0:
                        print("\n-stop car\n")
                        socketio.emit('send_message_arrive', {
                            "car_id": car_id,
                            "arrive_id": end[car_id][0],
                        })
                    arrive_flag[car_id] = True
            if arrive_flag[car_id] == True:
                '''正常退出循环时，更新车辆状态'''
                route_index[car_id] += 1
                temp_point = start[car_id]
                start[car_id] = end[car_id]
            arrive_flag[car_id] = False
            
            
    
def Process_Serial():
    """ 接收并处理串口数据
    """
    try:
        global init_flag, x0, y0, tag_id0, x1, y1, tag_id1
        global tag_id
        if serProcessor.serBasicStation.isOpen() == True:
            print("connected")
        # 线程循环读取沙盘数据
        while True:
            packet = serProcessor.serBasicStation.read(12)
            # print("get data")
            if len(packet) == 12:
                x0,y0,tag_id0,x1,y1,tag_id1 = serProcessor.parse_packet(packet)
                # print(x0,y0,tag_id0,x1,y1,tag_id1)
                tag_id[0] = tag_id0
                tag_id[1] = tag_id1
                # 第一次获取沙盘数据后，开启Web端数据传输
                if not init_flag:
                    # Update_msg(0.3)
                    init_flag = True
    except KeyboardInterrupt:
        serProcessor.serBasicStation.close()
        
def Update_msg(interval):
    """ 多线程定时向Web端发送车辆位置信息
    @param interval: 定时间隔
    """
    data = {
        "posx0":x0,
        "posy0":y0,
        "posx1":x1,
        "posy1":y1,
    }
    socketio.emit('send_message_location', data)
    t = threading.Timer(interval, Update_msg, args=[interval])
    t.start()
    
    
if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)

    
