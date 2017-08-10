import numpy as np
import time
import serial
import subprocess

class ControlIris(object):
    
    def __init__(self,device='COM10'):
        # device = '/dev/tty.usbserial-AI02GT45'
        self.device = device
        
    def connect(self):
        """
        Connect to iris
        """
        self.ser    = serial.Serial(port=self.device,  
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
        if self.ser.isOpen():    
            print('Connection established')
        else: 
            print('Connection could not be established')
            
    def set_percent(self,percent):
        """
        Set percent value
        """
        self.percent = percent
        sendcommand = '%OPEN '+str(percent)+'.00\n'
        self.ser.write(sendcommand)
        
    def list_ports(self):
        print(subprocess.check_output("python -m serial.tools.list_ports"))
