import ipywidgets.widgets as widgets
import threading
import time
import inspect
import ctypes
from Arm_Lib import Arm_Device

def wait_for_controller():
    while True:
        try:
            controller = widgets.Controller(index=0)
            display(controller)
            break
        except Exception as e:
            time.sleep(1)
            print("컨트롤러를 연결해주세요...")
            
wait_for_controller()

Arm = Arm_Device()

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def Arm_Handle():
    s_time = 500
    s_step = 1
    angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90

    while 1:
        # Because of the individual differences between the rocker on handle.
        # all the reset values on the remote stick are not necessarily zero, so 0.1 is required as a filter to avoid misoperation.
        # No.2 servo, A1 Up-negative Down-positive
        if controller.axes[1].value <= 0.1 and controller.axes[1].value >= -0.1:
            time.sleep(.000001)
        else:
            if controller.axes[1].value > 0.1:
                angle_2 += s_step
            else:
                angle_2 -= s_step
            if angle_2 > 180:
                angle_2 = 180
            elif angle_2 < 0:
                angle_2 = 0
            Arm.Arm_serial_servo_write(2, angle_2, s_time)
            time.sleep(0.01)

        # No.1 servo, A0 Left-negative Right-positive
        if controller.axes[0].value <= 0.1 and controller.axes[0].value >= -0.1:
            time.sleep(.000001)
        else:
            if controller.axes[0].value > 0.1:
                angle_1 -= s_step
            else:
                angle_1 += s_step

            if angle_1 > 180:
                angle_1 = 180
            elif angle_1 < 0:
                angle_1 = 0
            Arm.Arm_serial_servo_write(1, angle_1, s_time)
            time.sleep(0.01)

        # No.6 servo, NUM1=B0,NUM3=B2, A2 Up-negative Down-positive
        if controller.buttons[0].value:
            angle_6 += s_step
            if angle_6 > 180:
                angle_6 = 180
            elif angle_6 < 0:
                angle_6 = 0
            Arm.Arm_serial_servo_write(6, angle_6, s_time)
            time.sleep(0.01)
        elif controller.buttons[2].value:
            angle_6 -= s_step
            if angle_6 > 180:
                angle_6 = 180
            elif angle_6 < 0:
                angle_6 = 0
            Arm.Arm_serial_servo_write(6, angle_6, s_time)
            time.sleep(0.01)
        elif controller.axes[2].value > 0.5:
            angle_6 -= s_step
            if angle_6 > 180:
                angle_6 = 180
            elif angle_6 < 0:
                angle_6 = 0
            Arm.Arm_serial_servo_write(6, angle_6, s_time)
            time.sleep(0.01)
        elif controller.axes[2].value < -0.5:
            angle_6 += s_step
            if angle_6 > 180:
                angle_6 = 180
            elif angle_6 < 0:
                angle_6 = 0
            Arm.Arm_serial_servo_write(6, angle_6, s_time)
            time.sleep(0.01)

        # No.5, NUM2=B1,NUM4=B3, A5Left-negative Right-positive
        if controller.buttons[1].value:
            angle_5 += s_step
            if angle_5 > 180:
                angle_5 = 180
            elif angle_5 < 0:
                angle_5 = 0
            Arm.Arm_serial_servo_write(5, angle_5, s_time)
            time.sleep(0.01)
        elif controller.buttons[3].value:
            angle_5 -= s_step
            if angle_5 > 180:
                angle_5 = 180
            elif angle_5 < 0:
                angle_5 = 0
            Arm.Arm_serial_servo_write(5, angle_5, s_time)
            time.sleep(0.01)
        elif controller.axes[5].value > 0.5:
            angle_5 += s_step
            if angle_5 > 180:
                angle_5 = 180
            elif angle_5 < 0:
                angle_5 = 0
            Arm.Arm_serial_servo_write(5, angle_5, s_time)
            time.sleep(0.01)
        elif controller.axes[5].value < -0.5:
            angle_5 -= s_step
            if angle_5 > 180:
                angle_5 = 180
            elif angle_5 < 0:
                angle_5 = 0
            Arm.Arm_serial_servo_write(5, angle_5, s_time)
            time.sleep(0.01)

        # NO.4 servo，R1=B5,R2=B7
        if controller.buttons[5].value:
            angle_4 -= s_step
            if angle_4 > 180:
                angle_4 = 180
            elif angle_4 < 0:
                angle_4 = 0
            Arm.Arm_serial_servo_write(4, angle_4, s_time)
            time.sleep(0.01)
        elif controller.buttons[7].value:
            angle_4 += s_step
            if angle_4 > 180:
                angle_4 = 180
            elif angle_4 < 0:
                angle_4 = 0
            Arm.Arm_serial_servo_write(4, angle_4, s_time)
            time.sleep(0.01)

        # NO.3 servo，L1=B4,L2=B6
        if controller.buttons[4].value:
            angle_3 -= s_step
            if angle_3 > 180:
                angle_3 = 180
            elif angle_3 < 0:
                angle_3 = 0
            Arm.Arm_serial_servo_write(3, angle_3, s_time)
            time.sleep(0.01)
        elif controller.buttons[6].value:
            angle_3 += s_step
            if angle_3 > 180:
                angle_3 = 180
            elif angle_3 < 0:
                angle_3 = 0
            Arm.Arm_serial_servo_write(3, angle_3, s_time)
            time.sleep(0.01)

        # Press the key B8 to set all servos of DOFBOT to 90 degrees
        if controller.buttons[8].value:
            angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90
            Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
            time.sleep(1)

thread2 = threading.Thread(target=Arm_Handle)
thread2.setDaemon(True)
thread2.start()

stop_thread(thread2)