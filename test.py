import struct

def send_msg1(px, py, sx, sy, rotation):
    temp = struct.pack(
            "<BBHHHHhB",
            ord('#'),
            ord('1'),
            int(px),
            int(py),
            int(sx),
            int(sy),
            int(rotation),
            ord('*')
    )
    for i in range(len(temp)):
        print(temp[i])
    
# send_msg1(160, 120, 149, 131, -214)
a = (1,2)

def send_instruct(car_id, route_id, rode_id, action, wait_time):
    frame_head = 0x23
    frame_end = 0x2A
    # 将指令数据打包成字节流，共7bytes
    packet_data = struct.pack(
        "<BBBBBBB",
        frame_head,
        car_id,
        route_id,
        rode_id,
        action,
        wait_time,
        frame_end,
    )
    # self.serBasicStation.write(packet_data)
    print(packet_data, len(packet_data))
    
send_instruct(0, 2, 5, 0, 1)