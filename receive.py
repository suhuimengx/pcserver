import serial
import struct

"""
typedef struct LT_Frame
{
  uint8_t role;    // 0
  uint8_t id_0;    // 1
  uint8_t posx0_L; // 2
  uint8_t posx0_H; // 3
  uint8_t posy0_L; // 4
  uint8_t posy0_H; // 5
  uint8_t id_1;    // 6
  uint8_t posx1_L; // 7
  uint8_t posx1_H; // 8
  uint8_t posy1_L; // 9
  uint8_t posy1_H; // 10
  uint8_t SendBuf[11];
} LT_FRAME;
"""

class SerialProcessor:
    def __init__(self, comId, baudrate):
        self.serBasicStation = serial.Serial(comId, baudrate, timeout=1)

    def get_symbol(self, value):
        if value & 0x8000:
            return value - 0x10000
        else:
            return value
    
    def parse_packet(self, packet):
        # print(packet)
        pos_x0_int16 = (packet[2] << 8) | packet[1]
        pos_y0_int16 = (packet[4] << 8) | packet[3]
        tagId0 = packet[5]
        # print("tagId0:",tagId0)
        pos_x1_int16 = (packet[7] << 8) | packet[6]
        pos_y1_int16 = (packet[9] << 8) | packet[8]
        tagId1 = packet[10]
        pos_x0 = self.get_symbol(pos_x0_int16)
        pos_y0 = self.get_symbol(pos_y0_int16)
        pos_x1 = self.get_symbol(pos_x1_int16)
        pos_y1 = self.get_symbol(pos_y1_int16)
        return int(pos_x0), int(pos_y0), tagId0, int(pos_x1), int(pos_y1), tagId1
    
    def send_instruct(self, car_id, route_id, rode_id, action, wait_time):
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
        self.serBasicStation.write(packet_data)
        # print(route_id)
        print(rode_id)
        # print(action,"action")
        # print(wait_time,"wait_time")
        print(car_id, "号车", " 目标：", rode_id)

# send_packet(0, 1, -60.4, 0, 124, 341)

# ser = SerialProcessor("COM25", 115200)
# try:
#     if ser.serBasicStation.isOpen() == True:
#         print("connected")
#     while True:
#         packet = ser.serBasicStation.read(14)
#         # print("get data")
#         if len(packet) == 14:
#             print(hex(packet[0]))
#             x0,y0,yaw0,x1,y1,yaw1 = ser.parse_packet(packet)
#             print(x0,y0,yaw0,x1,y1,yaw1)
#         # print("get data")
# except KeyboardInterrupt:
#     ser.serBasicStation.close()

    
