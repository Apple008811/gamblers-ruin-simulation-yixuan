import tkinter as tk

# 创建一个最简单的tkinter窗口
root = tk.Tk()
root.title("Tkinter Test")
root.geometry("300x200")  # 明确设置窗口大小

# 添加一些基本元素
label = tk.Label(root, text="这是一个测试标签", font=("Arial", 16))
label.pack(pady=20)

button = tk.Button(root, text="测试按钮", bg="blue", fg="white")
button.pack(pady=20)

# 确保GUI在前台显示（macOS特定）
root.lift()
root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", False)

# 强制更新
root.update()

# 开始主循环
root.mainloop() 