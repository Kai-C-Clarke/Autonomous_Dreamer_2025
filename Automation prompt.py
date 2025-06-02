import pyautogui
import time

pyautogui.alert("Click OK to start automation test...")
time.sleep(1)

pyautogui.click(400, 400)
pyautogui.write("Testing automation from Kai", interval=0.1)
pyautogui.scroll(-300)
