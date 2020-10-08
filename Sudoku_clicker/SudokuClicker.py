import pathlib
import pyautogui
from ctypes import cdll

class SudokuClicker:
    def __init__(self, container, empty_positions, use_c_interface=False):
        self.container = container
        self.empty_positions = empty_positions
        if use_c_interface == False: self.automation_object = pyautogui
        else: self.automation_object = CInterfaceWrapper()

    def fillAll(self):
        for pos in self.empty_positions:
            self.fill(pos[0], pos[1], self.container[pos[0]][pos[1]])

    def fill(self, row, col, value=0):
        self.automation_object.moveTo(384 + col * 55, 262 + row * 55)
        self.automation_object.click()
        self.automation_object.write(str(value))

class CInterfaceWrapper:
    def __init__(self):
        self.lib = cdll.LoadLibrary(str(pathlib.Path(__file__).parent.absolute()) + '\PythonClickingInterface.dll')

    def moveTo(self, x, y):
        self.lib.MouseTo(x, y)

    def click(self):
        self.lib.MouseLClick()

    def write(self, value):
        self.lib.PressKBKey(int(value))