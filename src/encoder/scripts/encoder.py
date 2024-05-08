#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray 
import pigpio
import time

pi  = pigpio.pi()


RX_PIN = 14
TX_PIN = 15
BAUD_RATE = 115200

str1 = 0.01
str2 = 0.01
str3 = 0.01


msg = Float32MultiArray()

handle = pi.serial_open("/dev/ttyUSB0", BAUD_RATE)

def uart2rpi(data):
    if  isinstance(data,str):
        return "*"
    data = data.decode()
    start_index = data.find("@")
    data = data[start_index:] 
    end_index = data.find(";")
    data = data[:end_index+1]
    start = data.find('@')
    ended = data.find(',')
    str1 = float(data[start+1:ended-1])
    start = ended
    ended = data.find(',', start+1)
    str2  = float(data[start+1:ended-1])
    start = ended
    ended = data.find(';', start+1)
    str3  = float(data[start+1:ended-1])
    msg.data = [str1, str2, str3]
    return 0


def clear_uart_buffer():
    while pi.serial_data_available(handle):
        pi.serial_read(handle, 1)

def main():
    rospy.init_node('UART_FROM_STM32',anonymous=True)
    pub = rospy.Publisher('encoder_value',Float32MultiArray,queue_size=10)
    clear_uart_buffer()
    time.sleep(5)
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        (count, data) = pi.serial_read(handle, 100)
        uart2rpi(data)
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    main()



