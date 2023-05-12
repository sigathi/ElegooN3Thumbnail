# Copyright (c) 2023 sigathi
# Copyright (c) 2020 DhanOS
# ElegooN3Thumbnail plugin is released under the terms of the AGPLv3 or higher.

from UM.Extension import Extension
from UM.Application import Application
from UM.Platform import Platform
from UM.Logger import Logger

from cura.Snapshot import Snapshot
from cura.CuraApplication import CuraApplication

import os
from ctypes import *
from PyQt6.QtCore import Qt
import binascii
from array import array

# Main class
class ElegooN3Thumbnail(Extension):

    # Init
    def __init__(self):
        super().__init__()

        # Add a hook when a G-code is about to be written to a file
        Application.getInstance().getOutputDeviceManager().writeStarted.connect(self.add_snapshot_to_gcode)

        # Get a scene handler
        self.scene = Application.getInstance().getController().getScene()
    
    def take_screenshot(self):
        #extracted from Elegoo Cura MKS Plugin
        cut_image = Snapshot.snapshot(width = 900, height = 900)
        return cut_image

    def add_screenshot(self, img, width, height, img_type):
        Logger.log("d", "add_screenshot." +  CuraApplication.getInstance().getMachineManager().activeMachine.definition.id)
        result = ""
        b_image = img.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        img_size = b_image.size()
        result += img_type
        datasize = 0
        for i in range(img_size.height()):
            for j in range(img_size.width()):
                pixel_color = b_image.pixelColor(j, i)
                r = pixel_color.red() >> 3
                g = pixel_color.green() >> 2
                b = pixel_color.blue() >> 3
                rgb = (r << 11) | (g << 5) | b
                strHex = "%x" % rgb
                if len(strHex) == 3:
                    strHex = '0' + strHex[0:3]
                elif len(strHex) == 2:
                    strHex = '00' + strHex[0:2]
                elif len(strHex) == 1:
                    strHex = '000' + strHex[0:1]
                if strHex[2:4] != '':
                    result += strHex[2:4]
                    datasize += 2
                if strHex[0:2] != '':
                    result += strHex[0:2]
                    datasize += 2
                if datasize >= 50:
                    datasize = 0
            # if i != img_size.height() - 1:
            result += '\rM10086 ;'
            if i == img_size.height() - 1:
                result += "\r"
        return result

        
    def add_screenshot_new(self, img, width, height, img_type):
        Logger.log("d", "add_screenshot_new." +  CuraApplication.getInstance().getMachineManager().activeMachine.definition.id)
        if Platform.isOSX():
            pDll = CDLL(os.path.join(os.path.dirname(__file__), "libColPic.dylib"))
        elif Platform.isLinux():
            pDll = CDLL(os.path.join(os.path.dirname(__file__), "libColPic.so"))
        else:
            pDll = CDLL(os.path.join(os.path.dirname(__file__), "ColPic_X64.dll"))

        result = ""
        b_image = img.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        img_size = b_image.size()
        color16 = array('H')
        try:
            for i in range(img_size.height()):
                for j in range(img_size.width()):
                    pixel_color = b_image.pixelColor(j, i)
                    r = pixel_color.red() >> 3
                    g = pixel_color.green() >> 2
                    b = pixel_color.blue() >> 3
                    rgb = (r << 11) | (g << 5) | b
                    color16.append(rgb)

            # int ColPic_EncodeStr(U16* fromcolor16, int picw, int pich, U8* outputdata, int outputmaxtsize, int colorsmax);
            fromcolor16 = color16.tobytes()
            outputdata = array('B',[0]*img_size.height()*img_size.width()).tobytes()
            resultInt = pDll.ColPic_EncodeStr(fromcolor16, img_size.height(), img_size.width(), outputdata, img_size.height()*img_size.width(), 1024)

            data0 = str(outputdata).replace('\\x00', '')
            data1 = data0[2:len(data0) - 2]
            eachMax = 1024 - 8 - 1
            maxline = int(len(data1)/eachMax)
            appendlen = eachMax - 3 - int(len(data1)%eachMax)

            for i in range(len(data1)):
                if i == maxline*eachMax:
                    result += '\r;' + img_type + data1[i]
                elif i == 0:
                    result += img_type + data1[i]
                elif i%eachMax == 0:
                    result += '\r' + img_type + data1[i]
                else:
                    result += data1[i]
            result += '\r;'
            for j in range(appendlen):
                result += '0'

        except Exception as e:
            Logger.log("d", "Exception == " + str(e))
        
        return result + '\r'

    # G-code hook
    def add_snapshot_to_gcode(self, output_device):

        # If there's no G-code - return
        if not hasattr(self.scene, "gcode_dict") or not self.scene.gcode_dict:
            Logger.log("w", "Scene does not contain any gcode")
            return

        # Enumerate G-code objects
        for build_plate_number, gcode_list in self.scene.gcode_dict.items():
            for index, gcode in enumerate(gcode_list):

                # If there is ;includeThumbnail anywhere, add encoded snapshot image (simage and gimage) at the beginning
                if ';includeThumbnail' in gcode:
                    #Take a screenshot
                    screenShot = self.take_screenshot()
                    #Create the gcode for the screenshot depending on machine type
                    image_gcode = ""
                    machineType = Application.getInstance().getMachineManager().activeMachine.definition.getId()
                    if machineType == "elegoo_neptune_3_pro" or machineType == "elegoo_neptune_3_plus" or machineType == "elegoo_neptune_3_max" or machineType == "elegoo_neptune_3pro" or machineType == "elegoo_neptune_3plus" or machineType == "elegoo_neptune_3max":
                        image_gcode += self.add_screenshot_new(screenShot, 200, 200, ";gimage:")
                        image_gcode += self.add_screenshot_new(screenShot, 160, 160, ";simage:")
                        image_gcode += "\r"
                    elif machineType != "elegoo_neptune_3":
                        image_gcode += self.add_screenshot(screenShot, 200, 200, ";gimage:")
                        image_gcode += self.add_screenshot(screenShot, 160, 160, ";simage:")
                        image_gcode += "\r"
                    # Add image G-code to the beginning of the G-code
                    self.scene.gcode_dict[0][0] = image_gcode + self.scene.gcode_dict[0][0]
