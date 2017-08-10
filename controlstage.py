import numpy as np
import pandas as pd
from PyAPT import APTMotor

class ControlStage(object):
    
    def __init__(self):
        self.M = APTMotor(83829712,HWTYPE=31,verbose=True)
        self.df = pd.read_csv('../../HPF_FRD/sequence.csv')
        self.x = df.x_out_fiber_dist.values
        
    def go_home(self):
        self.M.go_home()
    
    def go_to_32(self):
        # Move absolute
        self.M.mAbs(32.)
        
    def go_to(self,value):
        self.M.mAbs(value)
    
    def exit(self):
        self.M.cleanUpAPT()

    def run_sequence(self):
        print("Running sequence")
        for i, x in enumerate(self.x):
            self.go_to(x)
            print("##########################################")
            print(i,"Now at",x,"mm")
            input_val = raw_input("Press Enter to continue. Press q to stop")
            if input_val == "q":
                break