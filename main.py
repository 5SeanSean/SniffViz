# main.py
import tkinter as tk
from app import PacketCaptureApp

def main():
    root = tk.Tk()
    app = PacketCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()