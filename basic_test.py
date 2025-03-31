# 极简Tkinter测试
import tkinter as tk
root = tk.Tk()
root.title("测试")
label = tk.Label(root, text="如果您看到这个，Tkinter工作正常")
label.pack(padx=20, pady=20)
root.mainloop() 