# main.py
import tkinter as tk
from gui import App
import os

if not os.path.exists('data'):
    os.makedirs('data')

app = App()
app.mainloop()
