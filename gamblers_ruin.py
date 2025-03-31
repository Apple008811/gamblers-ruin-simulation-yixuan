import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

def simulate_gamblers_ruin(p, q, j, i, n, k, m, num_simulations):
    wins = 0
    losses = 0
    results = []

    for _ in range(num_simulations):
        money = i
        losing_streak = 0
        while money > 0 and money < n:
            bet = min(j * (1 / p) ** losing_streak, m)
            if money < bet:
                if money + k < bet:
                    break
                else:
                    money += k  # Take a loan

            if random.random() < p:
                money += bet * q
                losing_streak = 0
            else:
                money -= bet
                losing_streak += 1

        if money >= n:
            wins += 1
        else:
            losses += 1

        results.append(money)

    win_probability = wins / num_simulations
    loss_probability = losses / num_simulations

    return win_probability, loss_probability, results

def update_plot(frame, results, line):
    line.set_ydata(results[:frame])
    return line,

def run_simulation():
    try:
        p = float(probability_entry.get())
        q = float(payout_entry.get())
        j = float(bet_size_entry.get())
        i = float(starting_amount_entry.get())
        n = float(goal_amount_entry.get())
        k = float(credit_line_entry.get())
        m = float(max_bet_entry.get())
        num_simulations = int(simulations_entry.get())

        win_prob, loss_prob, results = simulate_gamblers_ruin(p, q, j, i, n, k, m, num_simulations)

        result_label.config(text=f"Probability of winning: {win_prob:.4f}\nProbability of going broke: {loss_prob:.4f}")

        fig, ax = plt.subplots()
        ax.set_xlim(0, num_simulations)
        ax.set_ylim(0, max(results))
        line, = ax.plot(results, lw=2)

        ani = FuncAnimation(fig, update_plot, frames=num_simulations, fargs=(results, line), blit=True)
        plt.show()
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# GUI setup - 使用更简单的布局
root = tk.Tk()
root.title("Gambler's Ruin Simulation")
root.geometry("500x450")

# macOS特定设置
if os.name == 'posix':
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)

# 直接使用Frame而不是ttk.Frame
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

# 使用简单的pack布局而不是grid
tk.Label(frame, text="Probability of Winning (p):").pack(anchor=tk.W)
probability_entry = tk.Entry(frame)
probability_entry.pack(fill=tk.X, pady=(0, 10))
probability_entry.insert(0, "0.5")

tk.Label(frame, text="Payout (q):").pack(anchor=tk.W)
payout_entry = tk.Entry(frame)
payout_entry.pack(fill=tk.X, pady=(0, 10))
payout_entry.insert(0, "2")

tk.Label(frame, text="Bet Size (j):").pack(anchor=tk.W)
bet_size_entry = tk.Entry(frame)
bet_size_entry.pack(fill=tk.X, pady=(0, 10))
bet_size_entry.insert(0, "1")

tk.Label(frame, text="Starting Amount (i):").pack(anchor=tk.W)
starting_amount_entry = tk.Entry(frame)
starting_amount_entry.pack(fill=tk.X, pady=(0, 10))
starting_amount_entry.insert(0, "10")

tk.Label(frame, text="Goal Amount (n):").pack(anchor=tk.W)
goal_amount_entry = tk.Entry(frame)
goal_amount_entry.pack(fill=tk.X, pady=(0, 10))
goal_amount_entry.insert(0, "20")

tk.Label(frame, text="Credit Line (k):").pack(anchor=tk.W)
credit_line_entry = tk.Entry(frame)
credit_line_entry.pack(fill=tk.X, pady=(0, 10))
credit_line_entry.insert(0, "0")

tk.Label(frame, text="Max Bet (m):").pack(anchor=tk.W)
max_bet_entry = tk.Entry(frame)
max_bet_entry.pack(fill=tk.X, pady=(0, 10))
max_bet_entry.insert(0, "10")

tk.Label(frame, text="Number of Simulations:").pack(anchor=tk.W)
simulations_entry = tk.Entry(frame)
simulations_entry.pack(fill=tk.X, pady=(0, 10))
simulations_entry.insert(0, "1000")

run_button = tk.Button(frame, text="Run Simulation", command=run_simulation, 
                      bg="#4CAF50", fg="white", padx=10, pady=5)
run_button.pack(pady=10)

result_label = tk.Label(frame, text="")
result_label.pack(pady=10)

# 强制更新GUI
root.update()

root.mainloop()

plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Test Plot")
plt.show()

# 最基础的 tkinter 应用
root = tk.Tk()

# 设置背景颜色来确认窗口内容是否可见
root.configure(bg="red")

# 添加一个标签，设置大字体和鲜明的颜色
label = tk.Label(root, text="TEST", font=("Arial", 40), fg="white", bg="blue")
label.pack(padx=50, pady=50)

root.mainloop()

class GamblersRuinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gambler's Ruin Simulation")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create control panel frame (left side)
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Parameters", padding=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create visualization frame (right side)
        self.viz_frame = ttk.LabelFrame(self.main_frame, text="Results", padding=10)
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add parameter controls
        self.create_controls()
        
        # Add visualization area
        self.create_visualizations()
        
        # Initialize with default values
        self.update_results()
    
    def create_controls(self):
        # Total chips (N)
        ttk.Label(self.control_frame, text="Total Chips (N)").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.total_chips_var = tk.IntVar(value=100)
        ttk.Spinbox(self.control_frame, from_=10, to=1000, textvariable=self.total_chips_var, width=10, 
                   command=self.update_results).grid(row=0, column=1, pady=5)
        
        # Initial chips for player A (i)
        ttk.Label(self.control_frame, text="Initial Chips for Player A (i)").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.initial_chips_var = tk.IntVar(value=50)
        self.initial_chips_spinbox = ttk.Spinbox(self.control_frame, from_=1, to=self.total_chips_var.get()-1, 
                                               textvariable=self.initial_chips_var, width=10,
                                               command=self.update_results)
        self.initial_chips_spinbox.grid(row=1, column=1, pady=5)
        
        # Win probability for player A (p)
        ttk.Label(self.control_frame, text="Win Probability for Player A (p)").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.win_prob_var = tk.DoubleVar(value=0.5)
        self.win_prob_scale = ttk.Scale(self.control_frame, from_=0.01, to=0.99, variable=self.win_prob_var, 
                                      orient=tk.HORIZONTAL, length=150, command=self.on_scale_change)
        self.win_prob_scale.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        self.win_prob_label = ttk.Label(self.control_frame, text="0.5")
        self.win_prob_label.grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # Update button
        ttk.Button(self.control_frame, text="Update Results", 
                  command=self.update_results).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Run simulation button
        ttk.Button(self.control_frame, text="Run Simulation", 
                  command=self.run_simulation).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Add simulation controls
        ttk.Label(self.control_frame, text="Number of Simulations").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.num_simulations_var = tk.IntVar(value=1000)
        ttk.Spinbox(self.control_frame, from_=100, to=10000, textvariable=self.num_simulations_var, 
                   width=10).grid(row=5, column=1, pady=5)
        
        # Theory vs Simulation section
        theory_frame = ttk.LabelFrame(self.control_frame, text="Theory vs Simulation")
        theory_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky=tk.W+tk.E)
        
        self.theory_ruin_var = tk.StringVar(value="N/A")
        self.sim_ruin_var = tk.StringVar(value="N/A")
        self.theory_duration_var = tk.StringVar(value="N/A")
        self.sim_duration_var = tk.StringVar(value="N/A")
        
        ttk.Label(theory_frame, text="Ruin Probability:").grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Label(theory_frame, text="Theory:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(theory_frame, textvariable=self.theory_ruin_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(theory_frame, text="Simulation:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(theory_frame, textvariable=self.sim_ruin_var).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(theory_frame, text="Expected Duration:").grid(row=3, column=0, sticky=tk.W, pady=3)
        ttk.Label(theory_frame, text="Theory:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Label(theory_frame, textvariable=self.theory_duration_var).grid(row=4, column=1, sticky=tk.W, pady=2)
        ttk.Label(theory_frame, text="Simulation:").grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Label(theory_frame, textvariable=self.sim_duration_var).grid(row=5, column=1, sticky=tk.W, pady=2)
        
        # Total chips change event
        self.total_chips_var.trace_add("write", self.on_total_chips_change)

    def create_visualizations(self):
        # Create tabs for different visualizations
        self.notebook = ttk.Notebook(self.viz_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Probability tab
        self.prob_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.prob_tab, text="Probability Analysis")
        
        self.prob_fig = plt.Figure(figsize=(6, 5), dpi=100)
        self.prob_canvas = FigureCanvasTkAgg(self.prob_fig, self.prob_tab)
        self.prob_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Simulation tab
        self.sim_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sim_tab, text="Simulation Results")
        
        self.sim_fig = plt.Figure(figsize=(6, 5), dpi=100)
        self.sim_canvas = FigureCanvasTkAgg(self.sim_fig, self.sim_tab)
        self.sim_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def on_scale_change(self, event):
        # Update the probability label when the scale changes
        self.win_prob_label.config(text=f"{self.win_prob_var.get():.2f}")
        self.update_results()
    
    def on_total_chips_change(self, *args):
        # Update the max value of initial chips when total changes
        try:
            total = self.total_chips_var.get()
            # Ensure initial chips doesn't exceed total-1
            current = self.initial_chips_var.get()
            if current >= total:
                self.initial_chips_var.set(total - 1)
            
            self.initial_chips_spinbox.config(to=total-1)
            self.update_results()
        except:
            pass
    
    def calculate_ruin_probability(self, i, N, p):
        q = 1 - p
        if p == 0.5:
            return 1 - (i / N)
        else:
            ratio = q / p
            return (ratio**i - ratio**N) / (1 - ratio**N)
    
    def calculate_expected_duration(self, i, N, p):
        if p == 0.5:
            return i * (N - i)
        else:
            q = 1 - p
            ratio = q / p
            term1 = N * (1 - ratio**i) / (1 - ratio**N)
            term2 = i
            return term1 / (p - q) - term2 / (p - q)
    
    def update_probability_plot(self):
        N = self.total_chips_var.get()
        p = self.win_prob_var.get()
        initial_i = self.initial_chips_var.get()
        
        # Clear the figure
        self.prob_fig.clear()
        
        # Create subplots
        ax1 = self.prob_fig.add_subplot(211)
        ax2 = self.prob_fig.add_subplot(212)
        
        # Calculate ruin probabilities for different initial values
        i_values = list(range(1, N))
        ruin_probs = [self.calculate_ruin_probability(i, N, p) for i in i_values]
        
        # Calculate expected durations for different initial values
        durations = [self.calculate_expected_duration(i, N, p) for i in i_values]
        
        # Plot ruin probability
        ax1.plot(i_values, ruin_probs, 'b-')
        ax1.set_xlabel('Initial Chips for Player A (i)')
        ax1.set_ylabel('Ruin Probability for Player A')
        ax1.set_title(f'Ruin Probability vs Initial Chips (N={N}, p={p:.2f})')
        ax1.grid(True)
        ax1.axvline(x=initial_i, color='r', linestyle='--')
        ax1.axhline(y=self.calculate_ruin_probability(initial_i, N, p), color='r', linestyle='--')
        
        # Plot expected duration
        ax2.plot(i_values, durations, 'g-')
        ax2.set_xlabel('Initial Chips for Player A (i)')
        ax2.set_ylabel('Expected Duration (Rounds)')
        ax2.set_title(f'Expected Duration vs Initial Chips (N={N}, p={p:.2f})')
        ax2.grid(True)
        ax2.axvline(x=initial_i, color='r', linestyle='--')
        ax2.axhline(y=self.calculate_expected_duration(initial_i, N, p), color='r', linestyle='--')
        
        self.prob_fig.tight_layout()
        self.prob_canvas.draw()
    
    def run_single_simulation(self, i, N, p):
        # Run a single Gambler's Ruin simulation
        # Returns: (did_player_A_go_broke, number_of_rounds)
        chips = i
        rounds = 0
        while 0 < chips < N:
            rounds += 1
            if np.random.random() < p:
                chips += 1  # Player A wins
            else:
                chips -= 1  # Player A loses
        
        return (chips == 0, rounds)
    
    def run_simulation(self):
        N = self.total_chips_var.get()
        i = self.initial_chips_var.get()
        p = self.win_prob_var.get()
        num_simulations = self.num_simulations_var.get()
        
        # Run simulations
        results = [self.run_single_simulation(i, N, p) for _ in range(num_simulations)]
        broke_results = [result[0] for result in results]
        round_results = [result[1] for result in results]
        
        # Calculate statistics
        ruin_probability = sum(broke_results) / num_simulations
        avg_duration = sum(round_results) / num_simulations
        
        # Update simulation results
        self.sim_ruin_var.set(f"{ruin_probability:.4f}")
        self.sim_duration_var.set(f"{avg_duration:.2f}")
        
        # Update simulation plot
        self.update_simulation_plot(round_results)
    
    def update_simulation_plot(self, round_results):
        # Clear the figure
        self.sim_fig.clear()
        
        # Create subplots
        ax1 = self.sim_fig.add_subplot(211)
        ax2 = self.sim_fig.add_subplot(212)
        
        # Plot histogram of game durations
        ax1.hist(round_results, bins=30, alpha=0.7, color='skyblue')
        ax1.set_xlabel('Rounds')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Game Durations')
        ax1.grid(True)
        
        # Plot trace of a few sample games
        N = self.total_chips_var.get()
        i = self.initial_chips_var.get()
        p = self.win_prob_var.get()
        
        ax2.set_xlabel('Rounds')
        ax2.set_ylabel('Player A Chips')
        ax2.set_title('Sample Game Traces')
        ax2.grid(True)
        
        # Generate and plot 5 sample games
        for game in range(5):
            chips = i
            chips_history = [chips]
            while 0 < chips < N:
                if np.random.random() < p:
                    chips += 1
                else:
                    chips -= 1
                chips_history.append(chips)
                
                # Prevent infinite loops
                if len(chips_history) > 1000:
                    break
            
            rounds = list(range(len(chips_history)))
            ax2.plot(rounds, chips_history, alpha=0.7, label=f'Game {game+1}')
        
        ax2.axhline(y=0, color='r', linestyle='--')
        ax2.axhline(y=N, color='g', linestyle='--')
        ax2.legend()
        
        self.sim_fig.tight_layout()
        self.sim_canvas.draw()
    
    def update_results(self):
        # Get current parameter values
        N = self.total_chips_var.get()
        i = self.initial_chips_var.get()
        p = self.win_prob_var.get()
        
        # Calculate theoretical results
        ruin_prob = self.calculate_ruin_probability(i, N, p)
        exp_duration = self.calculate_expected_duration(i, N, p)
        
        # Update theory labels
        self.theory_ruin_var.set(f"{ruin_prob:.4f}")
        self.theory_duration_var.set(f"{exp_duration:.2f}")
        
        # Update probability plot
        self.update_probability_plot()

def main():
    root = tk.Tk()
    app = GamblersRuinApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
