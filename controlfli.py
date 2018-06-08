from __future__ import print_function
import FLI
import astropy.io.fits
import astropy
import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

class ControlFLI(object):
    
    def __init__(self,savefolder="."):
        self.C = FLI.USBCamera("flipro0","proline")
        self.header = astropy.io.fits.Header()
        self.header['SERIAL'] = self.C.get_info()['serial_number']
        self.savefolder=savefolder
        
    def expose(self,exptime,frametype="normal",plot=True,ax=None):
        """
        exptime in s
        """
        print("Exposing",exptime,"s...",end="")
        self.header.set("EXPTIME",value=exptime,comment="s")
        self.header['IMAGETYP']= frametype
        self.header.set("DATE-OBS",value=str(datetime.datetime.utcnow()),comment="start of exposure")
        self.C.set_exposure(int(exptime*1000),frametype=frametype)
        self.data = self.C.take_photo()
        self.header.set("CCD-TEMP",value=self.C.get_temperature(),comment="CCD temp in C")
        self.header["DATE-END"] = str(datetime.datetime.utcnow())
        self.header['CAM-MODE'] = self.C.get_camera_mode_string()
        self.header['BASETEMP'] = self.C.read_base_temperature()
        self.header['XBINNING'] = self.C.hbin
        self.header['YBINNING'] = self.C.vbin
        if plot==True:
            if ax == None:
                self.fig, self.ax = plt.subplots()
            else:
                self.ax = ax
            self.ax.imshow(self.data)
            print("MAX COUNTS:",np.max(self.data))
            plt.pause(0.1)
        print('Done')
        
    def save(self,filename,overwrite=False):
        """
        Save as a fitsfile
        """
        astropy.io.fits.writeto(self.savefolder+os.sep+filename,data=self.data,header=self.header,overwrite=overwrite,output_verify="fix")
        print('Saved to',self.savefolder+os.sep+filename)