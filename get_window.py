import win32gui
import  ctypes 
from ctypes.wintypes import BOOL, HWND, RECT
import time
import platform
def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
   
    if  win32gui.GetWindowText(hwnd) == 'World of Warcraft':
        
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        print("\tLocation: (%d, %d)" % (x, y))
        print("\t    Size: (%d, %d)" % (w, h))


def main():

    win32gui.EnumWindows(callback, None)

def wint ():
    if platform.system() == 'Windows':
        top, left, w, h = win32gui.GetWindowRect(
            win32gui.GetForegroundWindow())


def GetWindowRectFromName(name: str) -> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    # print(hwnd)
    # print(rect)
    return (rect.left, rect.top, rect.right, rect.bottom)
def test():
    H1, H2, H3, H4 = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
    print(H1,H2,H3,H4)

if __name__ == "__main__":
   wint()

