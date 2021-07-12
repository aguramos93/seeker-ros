#!/usr/bin/python3
import serial
import numpy as np

def dec2hex(dec):
        
        if dec >= 0:
            hexa = hex(int(dec))
        else:
            absDec = abs(int(dec))
            bina = bin(absDec)
            bina = bina[2:].zfill(16)

            inv_bina = ''
            for i in bina:  
                if i == '0':
                    inv_bina += '1'
                else:
                    inv_bina += '0'

            int_sum = int(inv_bina, 2) + int(1)
            hexa = hex(int_sum)

        return hexa

class Seeker:

    def __init__(self):
        print("seeker constructor")
        
    def calculate_angle(self, angle):
        
        angle /= 0.02197265625 # 1 unit: 0.02197265625 degree
        hexAngle = dec2hex(angle)

        if len(hexAngle) == 6:
            low = hexAngle[4:6]
            high = hexAngle[2:4]
        elif len(hexAngle) == 5:
            low = hexAngle[3:5]
            high = "0" + hexAngle[2]
        elif len(hexAngle) == 4:
            low = hexAngle[2:4]
            high = "00"
        elif len(hexAngle) == 3:
            low = "0" + hexAngle[2]
            high = "00"
        else:
            print("ERROR: Introduce a correct angle!")
        
        low = int(low, 16)
        high = int(high, 16)

        low = np.uint8(low)
        high = np.uint8(high)

        return low, high

    def calculate_speed(self, speed):
        
        speed /= 0.1220740379 # 1 unit: 0.1220740379 degree/sec
        hexSpeed = dec2hex(speed)

        if len(hexSpeed) == 6:
            low = hexSpeed[4:6]
            high = hexSpeed[2:4]
        elif len(hexSpeed) == 5:
            low = hexSpeed[3:5]
            high = "0" + hexSpeed[2]
        elif len(hexSpeed) == 4:
            low = hexSpeed[2:4]
            high = "00"
        elif len(hexSpeed) == 3:
            low = "0" + hexSpeed[2]
            high = "00"
        else:
            print("ERROR: Introduce a correct speed!")
        
        low = int(low, 16)
        high = int(high, 16)

        low = np.uint8(low)
        high = np.uint8(high)

        return low, high

    def calculate_gimbal_cmd(self, mode, Rsl, Rsh, Ral, Rah, Psl, Psh, Pal, Pah, Ysl, Ysh, Yal, Yah):

        HEAD = [0xFF, 0x01, 0x0F, 0x10]
        CONTROL_MODE = [mode, mode, mode]
        ROLL = [Rsl, Rsh, Ral, Rah] # speed + angle
        PITCH = [Psl, Psh, Pal, Pah] # speed + angle
        YAW = [Ysl, Ysh, Yal, Yah] # speed + angle
        CHECKSUM = CONTROL_MODE[0] + CONTROL_MODE[1] + CONTROL_MODE[2] + ROLL[0] + ROLL[1] + ROLL[2] + ROLL[3] + PITCH[0] + PITCH[1] + PITCH[2] + PITCH[3] + YAW[0] + YAW[1] + YAW[2] + YAW[3]
        CHECKSUM = hex(CHECKSUM % 256)

        if len(CHECKSUM) == 3:
            checksum_m = "0" + CHECKSUM[2]
        elif len(CHECKSUM) == 4:
            checksum_m = CHECKSUM[2:4]
        else:
            print("ERROR: Checksum overflow, introduce another angle!")
        
        checksum_m = int(checksum_m, 16)
        checksum_m = np.uint8(checksum_m)
            
        CHECKSUM = [checksum_m]

        command = HEAD + CONTROL_MODE + ROLL + PITCH + YAW + CHECKSUM

        return command

    def calculate_camera_cmd(self, cmr_cmd):

        if cmr_cmd == 'zoom_out':
            ZOOM_OUT = [0x81, 0x01, 0x04, 0x07, 0x37, 0xFF]
            command = ZOOM_OUT
        elif cmr_cmd == 'zoom_in':
            ZOOM_IN = [0x81, 0x01, 0x04, 0x07, 0x27, 0xFF]
            command = ZOOM_IN
        elif cmr_cmd == 'stop_zoom':
            STOP_ZOOM = [0x81, 0x01, 0x04, 0x07, 0x00, 0xFF]
            command = STOP_ZOOM
        elif cmr_cmd == 'focus_in':
            FOCUS_IN = [0x81, 0x01, 0x04, 0x08, 0x27, 0xFF]
            command = FOCUS_IN
        elif cmr_cmd == 'focus_out':
            FOCUS_OUT = [0x81, 0x01, 0x04, 0x08, 0x37, 0xFF]
            command = FOCUS_OUT
        elif cmr_cmd == 'stop_focus':
            STOP_FOCUS = [0x81, 0x01, 0x04, 0x08, 0x00, 0xFF]
            command = STOP_FOCUS
        elif cmr_cmd == 'photo':
            PHOTO = [0x81, 0x01, 0x04, 0x68, 0x01, 0xFF]
            command = PHOTO
        elif cmr_cmd == 'start_video':
            START_VIDEO = [0x81, 0x01, 0x04, 0x68, 0x02, 0xFF]
            command = START_VIDEO
        elif cmr_cmd == 'stop_video':
            STOP_VIDEO = [0x81, 0x01, 0x04, 0x68, 0x03, 0xFF]
            command = STOP_VIDEO
        elif cmr_cmd == 'invert':
            INVERT = [0x81, 0x01, 0x04, 0x68, 0x04, 0xFF]
            command = INVERT
        elif cmr_cmd == 'switch':
            SWITCH = [0x81, 0x01, 0x04, 0x68, 0x05, 0xFF]
            command = SWITCH
        else:
            print("ERROR: Introduce a correct camera command!")

        return command

    def send_command(self, command):
        self.ser.write(command)

    def open_serial(self, device_path='/dev/ttyUSB0', baudrate=115200):
        self.ser = serial.Serial(device_path, baudrate, timeout=1)

    def close_serial(self):
        self.ser.close()