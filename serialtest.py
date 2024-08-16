from receive import SerialProcessor
serProcessor = SerialProcessor("COM116", 115200)
# serProcessor.send_instruct(0, 2, 7, 0, 1)
serProcessor.send_instruct(0, 2, 6, 0, 1)


