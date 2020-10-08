import time
import pyautogui

#from Digit_recognize.digit_recognize_testing import DigitRecognizerTesting
from Digit_recognize.DigitRecognizerBoard import DigitRecognizerBoard
from Sudoku_solver.SudokuSolver import SudokuSolver
from Sudoku_clicker.SudokuClicker import SudokuClicker

class SudokuKit:
    """Main entry point of the sudoku kit"""
    def take_screenshot(self):
        time.sleep(1.8)
        im = pyautogui.screenshot(region=(362, 240, 500, 498))
        im.save(r'C:\Users\Svilen\Desktop\Untitled Project\Sudoku kit\scr.png')
    
    def solve_from_picture(self, pic_name, fill_solved = False):
        container, empty_positions = DigitRecognizerBoard().get_numbers(pic_name)
        container = SudokuSolver(container).solve()
        if fill_solved: SudokuClicker(container, empty_positions, use_c_interface=True).fillAll()
        return container, empty_positions

if __name__ == '__main__':
    kit = SudokuKit()
    kit.take_screenshot()
    kit.solve_from_picture('scr.png', fill_solved=True)