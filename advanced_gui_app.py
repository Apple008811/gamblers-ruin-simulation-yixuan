import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import numpy as np
import os
from ttkthemes import ThemedTk
import random
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import matplotlib.style as mpl_style
import requests
import json
import threading
import time
from datetime import datetime
import streamlit as st

# Use a modern style
mpl_style.use('seaborn-v0_8-darkgrid')

# Remove Chinese font config as we'll use English
# plt.rcParams['font.sans-serif'] = ['SimHei']  
# plt.rcParams['axes.unicode_minus'] = False    

class DataVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Data Visualization Tool")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Apply theme and initialize
        self.style = ttk.Style()
        self.current_theme = "arc"
        self.available_themes = self.style.theme_names()
        self.data = None
        self.current_chart_type = "Line Chart"
        self.chart_windows = []
        self.color_maps = ["viridis", "plasma", "inferno", "magma", "coolwarm", "rainbow"]
        self.current_colormap = "viridis"
        
        # Animation related variables
        self.animation = None
        self.is_animating = False
        self.animation_speed = 100  # milliseconds
        
        # API related settings
        self.api_data_sources = {
            "Stock Market": {
                "url": "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}",
                "params": {"symbol": "MSFT", "apikey": "demo"},
                "data_path": "Time Series (Daily)",
                "x_field": "date",
                "y_fields": ["1. open", "2. high", "3. low", "4. close"]
            },
            "Weather Data": {
                "url": "https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric",
                "params": {"city": "London", "apikey": "your_api_key"},
                "data_path": "list",
                "x_field": "dt_txt",
                "y_fields": ["main.temp", "main.humidity", "wind.speed"]
            },
            "COVID-19 Data": {
                "url": "https://disease.sh/v3/covid-19/historical/{country}?lastdays={days}",
                "params": {"country": "all", "days": "30"},
                "data_path": "timeline",
                "x_field": "date",
                "y_fields": ["cases", "deaths", "recovered"]
            }
        }
        
        self.current_api_source = None
        self.api_auto_refresh = False
        self.refresh_interval = 300  # 5 minutes
        self.refresh_thread = None
        self.api_data_cache = {}
        
        # 添加这一行 - 在这里初始化auto_refresh_var
        self.auto_refresh_var = tk.BooleanVar(value=False)
        
        # Create UI components
        self.create_main_frame()
        self.create_menu()
        self.create_status_bar()
        self.apply_theme(self.current_theme)
        self.initialize_sample_data()
        self.customize_style()
        
    def customize_style(self):
        # Set aesthetically pleasing styles
        self.style.configure("TFrame", background="#f0f4f8")
        self.style.configure("TNotebook", background="#f0f4f8")
        self.style.configure("TNotebook.Tab", background="#d0e1f9", foreground="#333", padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#4a86e8")], foreground=[("selected", "white")])
        
        # Button styling
        self.style.configure("TButton", padding=[8, 4], background="#e0e9f7", font=('Arial', 10))
        self.style.configure("Accent.TButton", background="#4a86e8", foreground="white")
        
        # Label styling
        self.style.configure("TLabelframe.Label", font=('Arial', 11, 'bold'), foreground="#2c5aa0")
        self.style.configure("Title.TLabel", font=('Arial', 16, 'bold'), foreground="#2c5aa0")
        
        # Table styling
        self.style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#333333")
        self.style.map("Treeview", background=[("selected", "#4a86e8")], foreground=[("selected", "white")])
        
    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Import Data...", command=self.import_data, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Export Data...", command=self.export_data, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Clear Data", command=self.clear_data)
        self.edit_menu.add_command(label="Generate Random Data", command=self.generate_random_data)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="New Chart Window", command=self.create_new_chart_window)
        self.view_menu.add_separator()
        
        # Theme submenu
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        for theme in sorted(self.available_themes):
            self.theme_menu.add_command(label=theme, command=lambda t=theme: self.apply_theme(t))
        self.view_menu.add_cascade(label="Theme", menu=self.theme_menu)
        
        # Chart type submenu
        self.chart_menu = tk.Menu(self.view_menu, tearoff=0)
        for chart in ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Area Chart", "Heatmap"]:
            self.chart_menu.add_command(label=chart, command=lambda c=chart: self.change_chart_type(c))
        self.view_menu.add_cascade(label="Chart Type", menu=self.chart_menu)
        
        # Color scheme submenu
        self.colormap_menu = tk.Menu(self.view_menu, tearoff=0)
        for cmap in self.color_maps:
            self.colormap_menu.add_command(label=cmap, command=lambda cm=cmap: self.change_colormap(cm))
        self.view_menu.add_cascade(label="Color Scheme", menu=self.colormap_menu)
        
        # Animation submenu
        self.animation_menu = tk.Menu(self.view_menu, tearoff=0)
        self.animation_menu.add_command(label="Start Animation", command=self.start_animation)
        self.animation_menu.add_command(label="Stop Animation", command=self.stop_animation)
        self.view_menu.add_cascade(label="Animation", menu=self.animation_menu)
        
        # API menu
        self.api_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        # API data source submenu
        self.api_source_menu = tk.Menu(self.api_menu, tearoff=0)
        for source in self.api_data_sources:
            self.api_source_menu.add_command(
                label=source, 
                command=lambda s=source: self.select_api_source(s)
            )
        self.api_menu.add_cascade(label="Data Sources", menu=self.api_source_menu)
        
        # API operations
        self.api_menu.add_command(label="Fetch API Data", command=self.fetch_api_data)
        self.api_menu.add_command(label="Configure API Settings", command=self.configure_api)
        self.api_menu.add_separator()
        
        # Auto refresh option
        self.api_menu.add_checkbutton(
            label="Auto Refresh", 
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        )
        
        self.menu_bar.add_cascade(label="API", menu=self.api_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        self.root.config(menu=self.menu_bar)
        self.root.bind("<Control-o>", lambda event: self.import_data())
        self.root.bind("<Control-s>", lambda event: self.export_data())
    
    def create_main_frame(self):
        # Create main frame, using Paned window to allow resizing
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        
        # Left panel - Data and controls
        self.left_frame = ttk.Frame(self.main_paned, padding=10)
        self.main_paned.add(self.left_frame, weight=30)
        
        # Right panel - Chart display
        self.right_frame = ttk.Frame(self.main_paned, padding=10)
        self.main_paned.add(self.right_frame, weight=70)
        
        # Create toolbar, data panel and chart panel
        self.create_toolbar()
        self.create_data_panel()
        self.create_chart_panel()
    
    def create_toolbar(self):
        self.toolbar_frame = ttk.Frame(self.left_frame, padding=5)
        self.toolbar_frame.pack(fill=tk.X, padx=2, pady=(0, 5))
        
        # Import button
        self.import_btn = ttk.Button(self.toolbar_frame, text="Import Data", command=self.import_data, width=12)
        self.import_btn.pack(side=tk.LEFT, padx=2)
        
        # Export button
        self.export_btn = ttk.Button(self.toolbar_frame, text="Export Data", command=self.export_data, width=12)
        self.export_btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # New chart window button
        self.new_chart_btn = ttk.Button(self.toolbar_frame, text="New Chart Window", command=self.create_new_chart_window, width=15)
        self.new_chart_btn.pack(side=tk.LEFT, padx=2)
    
    def create_data_panel(self):
        # Create notebook to organize content in tabs
        self.data_notebook = ttk.Notebook(self.left_frame)
        self.data_notebook.pack(fill=tk.BOTH, expand=True, padx=2, pady=5)
        
        # Data table tab
        self.table_frame = ttk.Frame(self.data_notebook, padding=10)
        self.data_notebook.add(self.table_frame, text=" Data Table ")
        
        # Control panel tab
        self.control_frame = ttk.Frame(self.data_notebook, padding=10)
        self.data_notebook.add(self.control_frame, text=" Chart Controls ")
        
        self.create_data_table()
        self.create_control_panel()
    
    def create_data_table(self):
        # Table label
        table_label = ttk.Label(self.table_frame, text="Data Preview", style="Title.TLabel")
        table_label.pack(pady=(0, 10))
        
        # Create table frame and scrollbars
        table_container = ttk.Frame(self.table_frame)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        h_scroll = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scroll = ttk.Scrollbar(table_container, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create Treeview as table
        self.data_table = ttk.Treeview(table_container, columns=(), show="headings",
                                      yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.data_table.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        v_scroll.config(command=self.data_table.yview)
        h_scroll.config(command=self.data_table.xview)
        
        # Button frame
        btn_frame = ttk.Frame(self.table_frame, padding=(0, 10, 0, 0))
        btn_frame.pack(fill=tk.X)
        
        # Add table control buttons
        ttk.Button(btn_frame, text="Generate Random Data", command=self.generate_random_data, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear Data", command=self.clear_data, width=15).pack(side=tk.LEFT, padx=2)
    
    def create_control_panel(self):
        # Chart type selection
        chart_type_frame = ttk.LabelFrame(self.control_frame, text="Chart Type", padding=10)
        chart_type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.chart_type_var = tk.StringVar(value=self.current_chart_type)
        chart_types = ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Area Chart", "Heatmap"]
        
        for i, chart_type in enumerate(chart_types):
            ttk.Radiobutton(chart_type_frame, text=chart_type, value=chart_type,
                           variable=self.chart_type_var,
                           command=lambda: self.change_chart_type(self.chart_type_var.get())
                          ).grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=5)
        
        # Chart style settings
        style_frame = ttk.LabelFrame(self.control_frame, text="Chart Style", padding=10)
        style_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Chart title
        ttk.Label(style_frame, text="Chart Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_var = tk.StringVar(value="Data Visualization Chart")
        title_entry = ttk.Entry(style_frame, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # X-axis label
        ttk.Label(style_frame, text="X-axis Label:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.xlabel_var = tk.StringVar(value="X-axis")
        xlabel_entry = ttk.Entry(style_frame, textvariable=self.xlabel_var)
        xlabel_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Y-axis label
        ttk.Label(style_frame, text="Y-axis Label:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.ylabel_var = tk.StringVar(value="Y-axis")
        ylabel_entry = ttk.Entry(style_frame, textvariable=self.ylabel_var)
        ylabel_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Color scheme selection
        ttk.Label(style_frame, text="Color Scheme:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.colormap_var = tk.StringVar(value=self.current_colormap)
        colormap_combo = ttk.Combobox(style_frame, textvariable=self.colormap_var,
                                     values=self.color_maps, state="readonly", width=17)
        colormap_combo.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        colormap_combo.bind("<<ComboboxSelected>>", 
                           lambda e: self.change_colormap(self.colormap_var.get()))
        
        # Update chart button
        ttk.Button(self.control_frame, text="Update Chart", command=self.update_chart, width=20).pack(pady=10)
        
        # 在控制面板中添加API设置
        self.api_frame = ttk.LabelFrame(self.control_frame, text="API Data", padding=10)
        self.api_frame.pack(fill=tk.X, pady=(0, 10))
        
        # API源选择下拉框
        ttk.Label(self.api_frame, text="API Source:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.api_source_var = tk.StringVar()
        api_source_combo = ttk.Combobox(
            self.api_frame, 
            textvariable=self.api_source_var,
            values=list(self.api_data_sources.keys()), 
            state="readonly", 
            width=15
        )
        api_source_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        api_source_combo.bind(
            "<<ComboboxSelected>>", 
            lambda e: self.select_api_source(self.api_source_var.get())
        )
        
        # API按钮
        api_btn_frame = ttk.Frame(self.api_frame)
        api_btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            api_btn_frame, 
            text="Fetch Data",
            command=self.fetch_api_data,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            api_btn_frame, 
            text="Settings",
            command=self.configure_api,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        # 自动刷新选项
        refresh_frame = ttk.Frame(self.api_frame)
        refresh_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(
            refresh_frame,
            text="Auto refresh", 
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        ).pack(side=tk.LEFT)
        
        # 设置列权重以便拉伸
        self.api_frame.columnconfigure(1, weight=1)
    
    def create_chart_panel(self):
        # Top title
        chart_title = ttk.Label(self.right_frame, text="Data Visualization", style="Title.TLabel")
        chart_title.pack(pady=5)
        
        # Chart container
        self.chart_frame = ttk.LabelFrame(self.right_frame, text="Chart", padding=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create matplotlib figure
        plt.style.use('ggplot')
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Create chart canvas
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.chart_canvas_widget = self.chart_canvas.get_tk_widget()
        self.chart_canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add matplotlib navigation toolbar
        self.nav_toolbar = NavigationToolbar2Tk(self.chart_canvas, self.chart_frame)
        self.nav_toolbar.update()
        self.nav_toolbar.pack(fill=tk.X)
    
    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Left status information
        self.status_label = ttk.Label(self.status_bar, text="Ready", relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Right version information
        version_label = ttk.Label(self.status_bar, text="v1.0.0", relief=tk.SUNKEN, anchor=tk.E, padding=(5, 2))
        version_label.pack(side=tk.RIGHT, padx=5)
    
    # === Functional Methods ===
    
    def initialize_sample_data(self):
        self.generate_random_data()
    
    def import_data(self):
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Import based on file type
                if file_path.endswith(('.csv')):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    self.data = pd.read_excel(file_path)
                
                self.update_data_table()
                self.update_chart()
                self.status_label.config(text=f"Imported: {os.path.basename(file_path)}")
                messagebox.showinfo("Import Successful", f"Successfully imported data file: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Import Error", f"Error importing data: {str(e)}")
    
    def export_data(self):
        if self.data is None or self.data.empty:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Export based on file extension
                if file_path.endswith('.csv'):
                    self.data.to_csv(file_path, index=False)
                elif file_path.endswith(('.xlsx', '.xls')):
                    self.data.to_excel(file_path, index=False)
                
                self.status_label.config(text=f"Exported: {os.path.basename(file_path)}")
                messagebox.showinfo("Export Successful", f"Data successfully exported to: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")
    
    def generate_random_data(self):
        n_points = 50
        x = np.linspace(0, 10, n_points)
        y1 = np.sin(x) + np.random.random(n_points) * 0.5
        y2 = np.cos(x) + np.random.random(n_points) * 0.5
        y3 = np.tan(x/3) + np.random.random(n_points) * 0.2
        
        self.data = pd.DataFrame({
            'X': x,
            'Sine Wave': y1,
            'Cosine Wave': y2,
            'Tangent Wave': y3
        })
        
        self.update_data_table()
        self.update_chart()
        self.status_label.config(text="Random data generated")
    
    def clear_data(self):
        self.data = None
        
        # Clear table
        for item in self.data_table.get_children():
            self.data_table.delete(item)
            
        # Clear chart
        self.ax.clear()
        self.chart_canvas.draw()
        
        self.status_label.config(text="All data cleared")
    
    def update_data_table(self):
        if self.data is None:
            return
            
        # Clear current table
        for item in self.data_table.get_children():
            self.data_table.delete(item)
            
        # Update columns
        self.data_table['columns'] = list(self.data.columns)
        
        # Set column headings
        for col in self.data.columns:
            self.data_table.heading(col, text=col, anchor=tk.CENTER)
            self.data_table.column(col, width=100, anchor=tk.CENTER)
            
        # Fill data rows
        for i, row in self.data.iterrows():
            values = [row[col] for col in self.data.columns]
            self.data_table.insert('', 'end', values=values)
    
    def update_chart(self):
        if self.data is None or self.data.empty:
            return
            
        # Clear current chart
        self.ax.clear()
        
        # Get chart settings
        title = self.title_var.get()
        xlabel = self.xlabel_var.get()
        ylabel = self.ylabel_var.get()
        
        # Set title and labels
        self.ax.set_title(title, fontsize=14, pad=10)
        self.ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
        self.ax.set_ylabel(ylabel, fontsize=12, labelpad=10)
        
        # X-axis data
        x_col = self.data.columns[0]
        x_data = self.data[x_col]
        
        # Get color mapping
        cmap = cm.get_cmap(self.current_colormap)
        colors = [cmap(i/len(self.data.columns[1:])) for i in range(len(self.data.columns[1:]))]
        
        # Draw based on chart type
        if self.current_chart_type == "Line Chart":
            for i, col in enumerate(self.data.columns[1:]):
                self.ax.plot(x_data, self.data[col], label=col, color=colors[i], linewidth=2.5)
            
        elif self.current_chart_type == "Bar Chart":
            x = np.arange(len(x_data))
            width = 0.8 / (len(self.data.columns) - 1)
            
            for i, col in enumerate(self.data.columns[1:]):
                offset = width * i - 0.4 + width/2
                self.ax.bar(x + offset, self.data[col], width, label=col, color=colors[i], alpha=0.8)
            
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(x_data, rotation=45 if len(x_data) > 10 else 0)
            
        elif self.current_chart_type == "Scatter Plot":
            for i, col in enumerate(self.data.columns[1:]):
                self.ax.scatter(x_data, self.data[col], label=col, color=colors[i], alpha=0.7, s=60, edgecolors='white')
            
        elif self.current_chart_type == "Pie Chart":
            if len(self.data) > 0:
                row = self.data.iloc[0]
                values = [row[col] for col in self.data.columns[1:]]
                labels = self.data.columns[1:]
                self.ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, 
                          wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
                self.ax.axis('equal')
            
        elif self.current_chart_type == "Area Chart":
            for i, col in reversed(list(enumerate(self.data.columns[1:]))):
                self.ax.fill_between(x_data, self.data[col], alpha=0.6, label=col, color=colors[i])
                
        elif self.current_chart_type == "Heatmap":
            data_heatmap = self.data.iloc[:, 1:].values
            im = self.ax.imshow(data_heatmap, cmap=self.current_colormap, aspect='auto')
            self.ax.set_xticks(np.arange(len(self.data.columns[1:])))
            self.ax.set_yticks(np.arange(len(self.data)))
            self.ax.set_xticklabels(self.data.columns[1:])
            self.ax.set_yticklabels(self.data[x_col])
            
            cbar = plt.colorbar(im, ax=self.ax)
            cbar.ax.set_ylabel('Value', rotation=270, labelpad=15)
            
            for i in range(len(self.data)):
                for j in range(len(self.data.columns[1:])):
                    text_color = 'white' if abs(data_heatmap[i, j]) > 0.5 else 'black'
                    self.ax.text(j, i, f'{data_heatmap[i, j]:.2f}', ha='center', va='center', color=text_color, fontsize=8)
            
        # Add legend (unless it's a heatmap)
        if self.current_chart_type != "Heatmap" and self.current_chart_type != "Pie Chart":
            leg = self.ax.legend(loc='best', frameon=True, fancybox=True, framealpha=0.7)
            if leg:
                leg.get_frame().set_edgecolor('gray')
            
        # Add grid
        if self.current_chart_type != "Pie Chart" and self.current_chart_type != "Heatmap":
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
        # Set background color
        self.ax.set_facecolor('#f8f8f8')
        
        # Update figure and draw
        self.fig.tight_layout()
        self.chart_canvas.draw()
    
    def change_chart_type(self, chart_type):
        self.current_chart_type = chart_type
        self.chart_type_var.set(chart_type)
        self.update_chart()
        self.status_label.config(text=f"Chart type: {chart_type}")
    
    def change_colormap(self, colormap_name):
        self.current_colormap = colormap_name
        self.colormap_var.set(colormap_name)
        self.update_chart()
        self.status_label.config(text=f"Color scheme: {colormap_name}")
    
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Line Color", initialcolor="#1f77b4")
        if color_code[1]:
            self.line_color = color_code[1]
            self.update_chart()
    
    def create_new_chart_window(self):
        if self.data is None or self.data.empty:
            messagebox.showwarning("Error", "No data to display")
            return
            
        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Chart Window")
        chart_window.geometry("800x600")
        chart_window.minsize(600, 400)
        
        # Add to window list to track
        self.chart_windows.append(chart_window)
        
        # Create new chart frame
        chart_frame = ttk.LabelFrame(chart_window, text="Independent Chart View", padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create new matplotlib figure and copy main chart content
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        
        # Get X-axis data
        x_col = self.data.columns[0]
        
        # Draw similar chart
        self.copy_chart_to_new_window(ax, x_col)
        
        # Create chart canvas
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        chart_canvas_widget = chart_canvas.get_tk_widget()
        chart_canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        nav_toolbar = NavigationToolbar2Tk(chart_canvas, chart_frame)
        nav_toolbar.update()
        nav_toolbar.pack(fill=tk.X)
        
        # Window close event
        chart_window.protocol("WM_DELETE_WINDOW", lambda win=chart_window: self.close_chart_window(win))
        
        self.status_label.config(text="New chart window created")
    
    def copy_chart_to_new_window(self, ax, x_col):
        # Get color mapping
        cmap = cm.get_cmap(self.current_colormap)
        colors = [cmap(i/len(self.data.columns[1:])) for i in range(len(self.data.columns[1:]))]
        
        if self.current_chart_type == "Line Chart":
            for i, col in enumerate(self.data.columns[1:]):
                ax.plot(self.data[x_col], self.data[col], label=col, color=colors[i], linewidth=2.5)
        elif self.current_chart_type == "Scatter Plot":
            for i, col in enumerate(self.data.columns[1:]):
                ax.scatter(self.data[x_col], self.data[col], label=col, color=colors[i], alpha=0.7, s=60)
        elif self.current_chart_type == "Bar Chart":
            x = np.arange(len(self.data[x_col]))
            width = 0.8 / (len(self.data.columns) - 1)
            for i, col in enumerate(self.data.columns[1:]):
                offset = width * i - 0.4 + width/2
                ax.bar(x + offset, self.data[col], width, label=col, color=colors[i])
            ax.set_xticks(x)
            ax.set_xticklabels(self.data[x_col])
        
        # Set title and labels
        ax.set_title(self.title_var.get(), fontsize=14)
        ax.set_xlabel(self.xlabel_var.get(), fontsize=12)
        ax.set_ylabel(self.ylabel_var.get(), fontsize=12)
        
        # Add legend
        ax.legend()
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Set style
        ax.set_facecolor('#f8f8f8')
        fig = ax.figure
        fig.tight_layout()
    
    def close_chart_window(self, window):
        if window in self.chart_windows:
            self.chart_windows.remove(window)
        window.destroy()
    
    def apply_theme(self, theme_name):
        try:
            self.style.theme_use(theme_name)
            self.current_theme = theme_name
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Theme applied: {theme_name}")
        except tk.TclError:
            pass
    
    def show_about(self):
        about_text = """Advanced Data Visualization Tool
Version 1.0.0

A comprehensive data visualization tool 
with multiple chart types and style options.

Developed using tkinter, matplotlib, and pandas libraries.
"""
        messagebox.showinfo("About", about_text)
    
    def show_help(self):
        help_text = """Quick Guide:

1. Import Data: Use "File→Import Data" or toolbar button
2. View Data: Review in the left table
3. Choose Chart Type: Select in the "Chart Controls"
4. Customize Chart: Change title, labels and colors
5. Create New Window: Use "View→New Chart Window"
6. Change Theme: Use "View→Theme" menu

Shortcuts:
- Ctrl+O: Import data
- Ctrl+S: Export data
- Alt+F4: Exit
"""
        messagebox.showinfo("Help", help_text)

    def start_animation(self):
        if self.is_animating or self.data is None:
            return
        
        self.is_animating = True
        self.status_label.config(text="Animation started")
        
        fig = self.fig
        ax = self.ax
        data = self.data
        
        # Clear the previous plot
        ax.clear()
        
        # Set up animation based on chart type
        if self.current_chart_type == "Line Chart":
            x_data = data.iloc[:, 0].values
            y_columns = data.columns[1:]
            lines = []
            
            # Initialize empty lines
            for i, col in enumerate(y_columns):
                line, = ax.plot([], [], label=col, linewidth=2)
                lines.append(line)
            
            ax.set_xlim(min(x_data), max(x_data))
            y_min = data.iloc[:, 1:].values.min()
            y_max = data.iloc[:, 1:].values.max()
            ax.set_ylim(y_min - abs(y_min)*0.1, y_max + abs(y_max)*0.1)
            
            def init():
                for line in lines:
                    line.set_data([], [])
                return lines
            
            def animate(frame):
                # Animate up to the frame number
                frame = min(frame + 1, len(x_data))
                for i, line in enumerate(lines):
                    line.set_data(x_data[:frame], data.iloc[:frame, i+1].values)
                return lines
            
            self.animation = FuncAnimation(
                fig, animate, init_func=init, frames=len(x_data),
                interval=self.animation_speed, blit=True)
        
        elif self.current_chart_type == "Bar Chart":
            x_data = data.iloc[:, 0].values
            y_columns = data.columns[1:]
            bar_container = []
            
            # Create bars for the first frame
            x_pos = np.arange(len(x_data))
            width = 0.8 / len(y_columns)
            
            for i, col in enumerate(y_columns):
                offset = width * i - width * len(y_columns) / 2 + width / 2
                bars = ax.bar(x_pos + offset, [0] * len(x_data), width, label=col)
                bar_container.append(bars)
            
            ax.set_xticks(x_pos)
            ax.set_xticklabels(x_data)
            
            def animate(frame):
                for i, bars in enumerate(bar_container):
                    for j, bar in enumerate(bars):
                        height = data.iloc[j, i+1] * (frame / 100)
                        bar.set_height(height)
                return [bar for bars in bar_container for bar in bars]
            
            self.animation = FuncAnimation(
                fig, animate, frames=100,
                interval=self.animation_speed, blit=True)
        
        # Set title and labels
        ax.set_title(self.title_var.get(), fontsize=14)
        ax.set_xlabel(self.xlabel_var.get(), fontsize=12)
        ax.set_ylabel(self.ylabel_var.get(), fontsize=12)
        
        # Add legend with better styling
        legend = ax.legend(fancybox=True, framealpha=0.7, shadow=True)
        
        # Add grid with better styling
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Set background color
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#ffffff')
        
        # Better layout
        fig.tight_layout()
        self.chart_canvas.draw()
    
    def stop_animation(self):
        if self.animation:
            self.animation.event_source.stop()
            self.animation = None
            self.is_animating = False
            self.status_label.config(text="Animation stopped")
            self.update_chart()  # Redraw the chart in its final state

    def select_api_source(self, source_name):
        """Select API data source"""
        self.current_api_source = source_name
        self.status_label.config(text=f"Selected API source: {source_name}")
    
    def fetch_api_data(self):
        """Fetch data from API"""
        if not self.current_api_source:
            messagebox.showinfo("API", "Please select an API data source first")
            return
        
        try:
            # Show loading indicator
            self.status_label.config(text=f"Fetching data from {self.current_api_source}...")
            self.root.update()
            
            source_config = self.api_data_sources[self.current_api_source]
            
            # Build URL and parameters
            url = source_config["url"].format(**source_config["params"])
            
            # Send request
            response = requests.get(url)
            response.raise_for_status()  # Check for errors
            
            # Parse data
            data_json = response.json()
            processed_data = self.process_api_data(data_json, source_config)
            
            if processed_data is not None:
                # Update data and chart
                self.data = processed_data
                self.populate_data_table()
                self.update_chart()
                self.status_label.config(text=f"Data loaded from {self.current_api_source}")
                
                # Cache data
                self.api_data_cache[self.current_api_source] = {
                    "timestamp": datetime.now(),
                    "data": processed_data
                }
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Error fetching data: {str(e)}")
            self.status_label.config(text="API request failed")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing data: {str(e)}")
            self.status_label.config(text="Data processing failed")

    def process_api_data(self, json_data, source_config):
        """Process JSON data from API and convert to DataFrame format"""
        try:
            # Extract data path
            data_path = source_config["data_path"]
            if data_path:
                # Support dot notation for nested fields
                current_data = json_data
                for path_part in data_path.split('.'):
                    current_data = current_data[path_part]
            else:
                current_data = json_data
            
            # Create data lists
            x_field = source_config["x_field"]
            y_fields = source_config["y_fields"]
            
            # Initialize result columns
            result_dict = {x_field: []}
            for field in y_fields:
                result_dict[field.split('.')[-1]] = []  # Use last part of field as column name
            
            # Process different data structures
            if isinstance(current_data, dict):
                # Dictionary structure, like {"2023-01-01": {"temp": 20}, "2023-01-02": {"temp": 22}}
                for date_key, values in current_data.items():
                    result_dict[x_field].append(date_key)
                    
                    for field in y_fields:
                        # Support nested fields like "main.temp"
                        field_parts = field.split('.')
                        value = values
                        for part in field_parts:
                            if isinstance(value, dict) and part in value:
                                value = value[part]
                            else:
                                value = None
                                break
                            
                        column_name = field_parts[-1]
                        result_dict[column_name].append(float(value) if value else 0)
            
            elif isinstance(current_data, list):
                # List structure, like [{"date": "2023-01-01", "temp": 20}, {"date": "2023-01-02", "temp": 22}]
                for item in current_data:
                    # Extract X-axis value (date, etc.)
                    if x_field in item:
                        x_value = item[x_field]
                    else:
                        continue  # Skip data without time field
                    
                    result_dict[x_field].append(x_value)
                    
                    # Extract Y-axis field values
                    for field in y_fields:
                        field_parts = field.split('.')
                        value = item
                        for part in field_parts:
                            if isinstance(value, dict) and part in value:
                                value = value[part]
                            else:
                                value = None
                                break
                            
                        column_name = field_parts[-1]
                        result_dict[column_name].append(float(value) if value else 0)
            
            # Convert to DataFrame
            return pd.DataFrame(result_dict)
        
        except Exception as e:
            print(f"Error processing API data: {str(e)}")
            return None

    def configure_api(self):
        """Configure API settings window"""
        if not self.current_api_source:
            messagebox.showinfo("API", "Please select an API data source first")
            return
        
        config_window = tk.Toplevel(self.root)
        config_window.title(f"Configure {self.current_api_source} API")
        config_window.geometry("500x400")
        config_window.minsize(400, 300)
        
        # Center frame
        main_frame = ttk.Frame(config_window, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            main_frame, 
            text=f"API Settings - {self.current_api_source}",
            style="Title.TLabel"
        ).pack(pady=(0, 15))
        
        # Parameter settings
        params_frame = ttk.LabelFrame(main_frame, text="API Parameters", padding=10)
        params_frame.pack(fill=tk.X, pady=5)
        
        # Dynamically create parameter input fields
        source_config = self.api_data_sources[self.current_api_source]
        param_vars = {}
        
        row = 0
        for param, value in source_config["params"].items():
            ttk.Label(params_frame, text=f"{param}:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=5
            )
            
            param_vars[param] = tk.StringVar(value=value)
            entry = ttk.Entry(params_frame, textvariable=param_vars[param], width=30)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
            
            row += 1
        
        # Refresh interval settings
        refresh_frame = ttk.LabelFrame(main_frame, text="Auto Refresh Settings", padding=10)
        refresh_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(refresh_frame, text="Refresh Interval (seconds):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        
        refresh_var = tk.IntVar(value=self.refresh_interval)
        ttk.Spinbox(
            refresh_frame, 
            from_=10, 
            to=3600, 
            increment=10, 
            textvariable=refresh_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Button area
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(
            button_frame, 
            text="Save Settings",
            command=lambda: self.save_api_config(param_vars, refresh_var, config_window),
            style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancel",
            command=config_window.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Set column weights for stretching
        params_frame.columnconfigure(1, weight=1)
        refresh_frame.columnconfigure(1, weight=1)

    def save_api_config(self, param_vars, refresh_var, window):
        """Save API configuration"""
        # Update parameters
        for param, var in param_vars.items():
            self.api_data_sources[self.current_api_source]["params"][param] = var.get()
        
        # Update refresh interval
        self.refresh_interval = refresh_var.get()
        
        # If auto refresh is enabled, restart it
        if self.api_auto_refresh:
            self.toggle_auto_refresh()  # Turn off
            self.toggle_auto_refresh()  # Turn on again
        
        window.destroy()
        messagebox.showinfo("API Configuration", "Settings saved successfully")

    def toggle_auto_refresh(self):
        """Toggle auto refresh status"""
        self.api_auto_refresh = self.auto_refresh_var.get()
        
        if self.api_auto_refresh:
            if not self.current_api_source:
                messagebox.showinfo("API", "Please select an API data source first")
                self.auto_refresh_var.set(False)
                self.api_auto_refresh = False
                return
            
            # Start refresh thread
            self.refresh_thread = threading.Thread(target=self.auto_refresh_function, daemon=True)
            self.refresh_thread.start()
            self.status_label.config(text=f"Auto refresh enabled ({self.refresh_interval}s)")
        else:
            self.status_label.config(text="Auto refresh disabled")

    def auto_refresh_function(self):
        """Thread function for auto refreshing API data"""
        while self.api_auto_refresh:
            # Get data
            self.fetch_api_data()
            
            # Wait specified time
            for _ in range(self.refresh_interval):
                if not self.api_auto_refresh:
                    break
                time.sleep(1)

def gamblers_ruin_streamlit():
    st.title("Gambler's Ruin Interactive Exploration")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Introduction", "Simulation", "Play Game", "Analysis"
    ])
    
    # Introduction tab
    with tab1:
        st.header("Introduction to Gambler's Ruin")
        st.write("""
        The Gambler's Ruin problem is a classic probability scenario where...
        """)
        # Add explanations, formulas, etc.
    
    # Simulation tab
    with tab2:
        st.header("Interactive Simulation")
        # Add sliders, charts, etc.
        
    # Game tab
    with tab3:
        st.header("Try Your Luck!")
        # Add interactive game elements
        
    # Analysis tab
    with tab4:
        st.header("Statistical Analysis")
        # Add data visualization, insights, etc.

# Create and run application
def main():
    try:
        root = ThemedTk(theme="arc")
    except:
        root = tk.Tk()
        
    app = DataVisualizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 