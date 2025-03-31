import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np

class BlockchainMiningAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Conservative Mining Simulation")
        self.root.geometry("1000x750")  # Reduced window size
        self.root.configure(bg='#f0f0f0')
        
        # Animation parameters
        self.num_miners = 4
        self.miner_colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']  # Different colors for miners
        self.focal_miner = 1  # Miner 1 will be our focus (index 0)
        self.animation_speed = 1000  # milliseconds between stages
        self.total_stages = 10
        self.current_stage = 0
        self.conservative_payoffs = [0] * self.num_miners
        self.fork_payoffs = [0] * self.num_miners
        self.is_showing_fork = False
        
        # Create main frames
        self.create_frames()
        
        # Create control panel
        self.create_controls()
        
        # Create visualization area
        self.create_visualizations()
        
        # Start in paused state
        self.is_playing = False
        
        # Initialize blockchain state
        self.init_blockchain()
        
        # Configure style for buttons
        style = ttk.Style()
        style.configure("Accent.TButton", background="#4a86e8", foreground="white")

    def create_frames(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Split vertically: top part for visualization, bottom for dialog
        # Change the pack order to ensure dialog is visible
        
        # Dialog frame at the bottom
        dialog_frame = ttk.LabelFrame(self.main_frame, text="Interactive Q&A", padding=10)
        dialog_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Create the dialog components first to ensure they're properly initialized
        self.create_dialog_box(dialog_frame)
        
        # Top part with controls and visualization
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Left panel for controls
        self.control_frame = ttk.LabelFrame(top_frame, text="Simulation Controls", padding=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Right panel for visualization
        self.viz_frame = ttk.LabelFrame(top_frame, text="Blockchain Visualization", padding=10)
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_controls(self):
        # Title and description
        ttk.Label(self.control_frame, text="Conservative Mining Simulation", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        description = ("This animation demonstrates why miners have no\n"
                      "incentive to deviate from the conservative mining\n"
                      "strategy (always mining on the longest chain).")
        ttk.Label(self.control_frame, text=description, justify="left").pack(pady=(0, 20))
        
        # Miner information
        miner_frame = ttk.LabelFrame(self.control_frame, text="Miners")
        miner_frame.pack(fill=tk.X, pady=10)
        
        for i in range(self.num_miners):
            label_text = f"Miner {i+1}" + (" (Focus)" if i == self.focal_miner else "")
            miner_label = tk.Label(miner_frame, text=label_text, bg=self.miner_colors[i], 
                                  fg='white', padx=5, pady=2)
            miner_label.pack(fill=tk.X, pady=2)
        
        # Animation controls
        control_buttons = ttk.Frame(self.control_frame)
        control_buttons.pack(pady=20)
        
        self.play_button = ttk.Button(control_buttons, text="Play", command=self.toggle_play)
        self.play_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(control_buttons, text="Reset", command=self.reset_animation).grid(row=0, column=1, padx=5)
        
        # Speed control
        speed_frame = ttk.Frame(self.control_frame)
        speed_frame.pack(pady=10)
        
        ttk.Label(speed_frame, text="Animation Speed:").grid(row=0, column=0, padx=5)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.2, to=2.0, orient=tk.HORIZONTAL, 
                               variable=self.speed_var, length=150)
        speed_scale.grid(row=0, column=1, padx=5)
        
        # Comparison section
        comparison_frame = ttk.LabelFrame(self.control_frame, text="Strategy Comparison")
        comparison_frame.pack(fill=tk.X, pady=10)
        
        self.payoff_labels = []
        for i in range(self.num_miners):
            row_frame = ttk.Frame(comparison_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(row_frame, text=f"Miner {i+1}:", width=8).pack(side=tk.LEFT)
            
            conservative_label = ttk.Label(row_frame, text="0", width=8)
            conservative_label.pack(side=tk.LEFT)
            
            ttk.Label(row_frame, text="vs", width=4).pack(side=tk.LEFT)
            
            fork_label = ttk.Label(row_frame, text="0", width=8)
            fork_label.pack(side=tk.LEFT)
            
            self.payoff_labels.append((conservative_label, fork_label))
        
        # Explanation section
        explanation_frame = ttk.LabelFrame(self.control_frame, text="Explanation")
        explanation_frame.pack(fill=tk.X, pady=10)
        
        self.explanation_text = tk.Text(explanation_frame, height=10, width=30, wrap=tk.WORD)
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        self.explanation_text.insert(tk.END, "The animation will show why conservative mining is an equilibrium strategy.")
        self.explanation_text.config(state=tk.DISABLED)

    def create_visualizations(self):
        # Create notebook for visualization tabs
        notebook = ttk.Notebook(self.viz_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tab for conservative mining
        conservative_tab = ttk.Frame(notebook, padding=5)
        notebook.add(conservative_tab, text="Conservative Mining")
        
        # Create tab for fork mining
        fork_tab = ttk.Frame(notebook, padding=5)
        notebook.add(fork_tab, text="Fork Mining (Deviation)")
        
        # Create matplotlib figure with smaller size
        self.fig = plt.Figure(figsize=(8, 5), tight_layout=True)  # Reduced from default size
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas and add to conservative tab
        self.canvas = FigureCanvasTkAgg(self.fig, master=conservative_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create figure and canvas for fork visualization
        self.fork_fig = plt.Figure(figsize=(8, 5), tight_layout=True)  # Reduced from default size
        self.fork_ax = self.fork_fig.add_subplot(111)
        
        # Create canvas and add to fork tab
        self.fork_canvas = FigureCanvasTkAgg(self.fork_fig, master=fork_tab)
        self.fork_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create frame for simulation visualization
        sim_frame = ttk.LabelFrame(notebook, text="Simulation Results", padding=10)
        notebook.add(sim_frame, text="Simulation Analysis")
        
        # Create figure for simulation results with smaller size
        self.sim_fig = plt.Figure(figsize=(8, 5), tight_layout=True)  # Reduced from default size
        
        # Create canvas for simulation results
        self.sim_canvas = FigureCanvasTkAgg(self.sim_fig, master=sim_frame)
        self.sim_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def init_blockchain(self):
        # Initialize blockchain state
        self.conservative_chain = [{'miner': None, 'stage': 0}]  # Genesis block
        self.fork_chain = [{'miner': None, 'stage': 0}]  # Genesis block
        self.fork_alt_chain = []  # Will store the forked chain
        
        # Stage at which the fork happens
        self.fork_stage = random.randint(2, self.total_stages // 2)
        
        # Reset payoffs
        self.conservative_payoffs = [0] * self.num_miners
        self.fork_payoffs = [0] * self.num_miners
        
        # Initialize payoff history for analysis tab
        self.conservative_payoff_history = [[] for _ in range(self.num_miners)]
        self.fork_payoff_history = [[] for _ in range(self.num_miners)]
        for i in range(self.num_miners):
            self.conservative_payoff_history[i] = [0]
            self.fork_payoff_history[i] = [0]
        
        # Update explanations
        self.update_explanation(0)
        
        # Draw initial state
        self.draw_blockchain(self.ax, [self.conservative_chain], self.canvas)
        self.draw_blockchain(self.fork_ax, [self.fork_chain], self.fork_canvas)
        
        # Initialize simulation analysis
        self.update_simulation_analysis()
        
        # Update the payoff display
        self.update_payoffs()

    def toggle_play(self):
        self.is_playing = not self.is_playing
        self.play_button.config(text="Pause" if self.is_playing else "Play")
        
        if self.is_playing:
            self.advance_animation()

    def reset_animation(self):
        self.is_playing = False
        self.play_button.config(text="Play")
        self.current_stage = 0
        self.init_blockchain()

    def on_tab_change(self, event):
        self.is_showing_fork = self.notebook.index(self.notebook.select()) == 1

    def advance_animation(self):
        if not self.is_playing or self.current_stage >= self.total_stages:
            return
        
        self.current_stage += 1
        
        # Update blockchain state
        winning_miner = random.randint(0, self.num_miners - 1)
        
        # Update conservative chain
        self.conservative_chain.append({'miner': winning_miner, 'stage': self.current_stage})
        self.conservative_payoffs[winning_miner] += 1
        
        # Update fork chain
        if self.current_stage < self.fork_stage:
            # Before fork: both scenarios are identical
            self.fork_chain.append({'miner': winning_miner, 'stage': self.current_stage})
            self.fork_payoffs[winning_miner] += 1
        else:
            # After fork: focal miner works on fork, others on main chain
            if self.current_stage == self.fork_stage:
                # Create fork - focal miner mines on previous block
                self.fork_alt_chain.append({'miner': self.focal_miner, 'stage': self.current_stage})
                
                # Other miners continue on main chain
                if winning_miner != self.focal_miner:
                    self.fork_chain.append({'miner': winning_miner, 'stage': self.current_stage})
                    self.fork_payoffs[winning_miner] += 1
            else:
                # After fork creation
                if winning_miner == self.focal_miner:
                    # Focal miner adds to fork branch
                    self.fork_alt_chain.append({'miner': self.focal_miner, 'stage': self.current_stage})
                else:
                    # Other miners add to main chain
                    self.fork_chain.append({'miner': winning_miner, 'stage': self.current_stage})
                    self.fork_payoffs[winning_miner] += 1
                
                # Check if fork has become the longest chain
                fork_length = len(self.fork_alt_chain)
                main_length = len(self.fork_chain) - self.fork_stage
                
                if fork_length > main_length:
                    # Fork is longer, award tokens to focal miner
                    self.fork_payoffs[self.focal_miner] = fork_length
        
        # Update visualizations
        self.draw_blockchain(self.ax, [self.conservative_chain], self.canvas)
        
        chains = [self.fork_chain]
        if len(self.fork_alt_chain) > 0:
            chains.append(self.fork_alt_chain)
        self.draw_blockchain(self.fork_ax, chains, self.fork_canvas)
        
        # Update payoff display
        self.update_payoffs()
        
        # Update explanation
        self.update_explanation(self.current_stage)
        
        # Update simulation analysis tab
        self.update_simulation_analysis()
        
        # Schedule next update with speed adjustment
        if self.is_playing:
            delay = int(self.animation_speed / self.speed_var.get())
            self.root.after(delay, self.advance_animation)

    def draw_blockchain(self, ax, chains, canvas):
        ax.clear()
        
        # Set up the plot
        ax.set_xlim(-1, self.total_stages + 1)
        ax.set_ylim(-2, len(chains) + 1)
        ax.set_xlabel('Stage', fontsize=10)
        ax.set_title('Blockchain Growth', fontsize=12, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Remove y-axis ticks and labels
        ax.set_yticks([])
        
        # Create legend with appropriate marker size
        legend_elements = []
        for miner_idx in range(self.num_miners):
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                             markerfacecolor=self.miner_colors[miner_idx], 
                                             markersize=8, label=f'Miner {miner_idx+1}'))
        
        ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
        
        # Draw each chain with more space between chains
        for chain_idx, chain in enumerate(chains):
            y_pos = chain_idx * 0.8  # Increased vertical spacing between chains
            
            # Draw blocks
            for i, block in enumerate(chain):
                # Genesis block is gray
                if i == 0:
                    ax.add_patch(plt.Rectangle((i-0.4, y_pos-0.3), 0.8, 0.6, 
                                             facecolor='#a9a9a9', edgecolor='black', alpha=0.7))
                    ax.text(i, y_pos, "Genesis", ha='center', va='center', color='white', 
                           fontsize=8, fontweight='bold')
                else:
                    # Other blocks are colored by miner
                    miner = block['miner']
                    color = self.miner_colors[miner] if miner is not None else '#a9a9a9'
                    
                    # Keep blocks clear but not too large
                    ax.add_patch(plt.Rectangle((i-0.4, y_pos-0.3), 0.8, 0.6, 
                                             facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.7))
                    
                    # Use appropriate size text for better readability
                    ax.text(i, y_pos, f"M{miner+1}" if miner is not None else "", 
                           ha='center', va='center', color='white', 
                           fontsize=9, fontweight='bold')
                
                # Add connecting lines between blocks
                if i > 0:
                    ax.plot([i-1, i], [y_pos, y_pos], 'k-', linewidth=1.5)
            
            # Add fork indicator
            if len(chains) > 1 and chain_idx == 1:
                fork_point = len(self.fork_chain[:self.fork_stage]) - 1
                ax.plot([fork_point, fork_point + 1], 
                       [0, y_pos], 'k', linewidth=1.5, linestyle='--')
                
                # Make fork label visible but not too large
                ax.text(fork_point, y_pos + 0.3, "Fork", ha='center', va='bottom', 
                       color='red', fontsize=10, fontweight='bold')
        
        # Add stage indicator
        ax.axvline(x=self.current_stage, color='gray', linestyle='--', alpha=0.5)
        ax.text(self.current_stage, -1.5, f"Current Stage: {self.current_stage}", 
               ha='center', va='center', fontsize=9,
               bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
        
        canvas.draw()

    def update_payoffs(self):
        for i in range(self.num_miners):
            self.payoff_labels[i][0].config(text=str(self.conservative_payoffs[i]))
            self.payoff_labels[i][1].config(text=str(self.fork_payoffs[i]))

    def update_explanation(self, stage):
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        
        if stage == 0:
            explanation = (
                "Stage 0: Initial state with Genesis block.\n\n"
                "In each stage, a random miner will win the mining "
                "competition and add a block to the chain.\n\n"
                "In Conservative Mining, all miners always extend the longest chain."
            )
        elif stage < self.fork_stage:
            explanation = (
                f"Stage {stage}: All miners are mining on the main chain.\n\n"
                "In both scenarios, miners are receiving tokens for each block they mine."
            )
        elif stage == self.fork_stage:
            explanation = (
                f"Stage {stage}: The fork begins!\n\n"
                "In the fork scenario, Miner {self.focal_miner+1} deviates from "
                "conservative strategy and creates a fork.\n\n"
                "Notice that blocks on the fork don't immediately earn tokens "
                "until the fork becomes the longest chain."
            )
        elif stage > self.fork_stage:
            fork_length = len(self.fork_alt_chain)
            main_length = len(self.fork_chain) - self.fork_stage
            
            if fork_length > main_length:
                advantage = "The fork is now the longest chain! Blocks on the fork now earn tokens."
            else:
                disadvantage = f"The fork is shorter ({fork_length} vs {main_length} blocks)."
                advantage = "The conservative chain is still longer, so those blocks earn tokens."
                
            explanation = (
                f"Stage {stage}: Mining continues after the fork.\n\n"
                f"{disadvantage if fork_length <= main_length else advantage}\n\n"
                "Compare the payoffs between conservative mining and fork mining strategies."
            )
            
            if stage == self.total_stages:
                explanation += (
                    "\n\nFinal result: The conservative strategy ensures getting "
                    "tokens for each block mined. Fork mining risks not getting "
                    "tokens if your fork doesn't become the longest chain."
                )
        
        self.explanation_text.insert(tk.END, explanation)
        self.explanation_text.config(state=tk.DISABLED)

    def create_dialog_box(self, parent):
        # Make the chat history taller and more prominent
        self.chat_history = tk.Text(parent, height=8, wrap=tk.WORD, state=tk.DISABLED, 
                                   background="#f5f5f5", borderwidth=2, relief="sunken")
        self.chat_history.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Scrollbar for chat history
        chat_scrollbar = ttk.Scrollbar(parent, command=self.chat_history.yview)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history.config(yscrollcommand=chat_scrollbar.set)
        
        # Input area with clear visual separation
        input_frame = ttk.Frame(parent, padding=5, relief="groove", borderwidth=1)
        input_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Make the question label more prominent
        ttk.Label(input_frame, text="Your question:", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Text entry
        self.question_entry = ttk.Entry(input_frame, width=70)
        self.question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.question_entry.bind("<Return>", self.handle_question)
        
        # Fix the Ask button - use regular button instead of styled button
        submit_button = ttk.Button(input_frame, text="Ask", command=self.handle_question)
        submit_button.pack(side=tk.RIGHT, padx=5)
        
        # Add initial welcome message
        self.add_to_chat("System", "Welcome to the Blockchain Mining Simulation! Feel free to ask questions about conservative mining, forks, or any aspect of the simulation.")

    def handle_question(self, event=None):
        question = self.question_entry.get().strip()
        if not question:
            return
        
        # Add the question to the chat
        self.add_to_chat("You", question)
        
        # Clear the entry
        self.question_entry.delete(0, tk.END)
        
        # Generate and display the answer
        answer = self.generate_answer(question)
        self.add_to_chat("System", answer)

    def add_to_chat(self, speaker, message):
        # Enable editing
        self.chat_history.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        
        # Format based on who's speaking
        if speaker == "You":
            self.chat_history.insert(tk.END, f"[{timestamp}] You: ", "user")
            self.chat_history.insert(tk.END, f"{message}\n", "user_msg")
        else:
            self.chat_history.insert(tk.END, f"[{timestamp}] System: ", "system")
            self.chat_history.insert(tk.END, f"{message}\n", "system_msg")
        
        # Configure tags for styling
        self.chat_history.tag_configure("user", foreground="#0066cc", font=("Arial", 9, "bold"))
        self.chat_history.tag_configure("user_msg", foreground="#000000", font=("Arial", 9))
        self.chat_history.tag_configure("system", foreground="#cc0000", font=("Arial", 9, "bold"))
        self.chat_history.tag_configure("system_msg", foreground="#000000", font=("Arial", 9))
        
        # Disable editing and scroll to end
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def generate_answer(self, question):
        # Convert question to lowercase for easier matching
        question_lower = question.lower()
        
        # Dictionary of question patterns and their answers
        qa_pairs = {
            "what is conservative mining": 
                "Conservative mining is a strategy where miners always extend the longest chain. "
                "This is considered the rational strategy as it maximizes expected rewards.",
            
            "what is a fork": 
                "A fork occurs when a miner mines on a block that is not the tip of the longest chain. "
                "This creates a branch in the blockchain, with two competing versions of history.",
            
            "why is conservative mining optimal": 
                "Conservative mining is optimal because it ensures you receive tokens for each block you mine. "
                "When creating a fork, you risk not receiving tokens for your mined blocks if your fork "
                "doesn't become the longest chain.",
            
            "what happens in a fork": 
                "In a fork, the blockchain splits into two competing chains. Only blocks on the longest "
                "chain earn tokens. If your fork doesn't become the longest chain, you won't receive "
                "tokens for those blocks, resulting in wasted mining effort.",
            
            "what is the current stage": 
                f"The current stage is {self.current_stage}. The simulation has {self.total_stages} total stages.",
            
            "how many miners": 
                f"There are {self.num_miners} miners in this simulation.",
            
            "explain payoffs": 
                "Payoffs represent the tokens earned by each miner. In conservative mining, miners "
                "receive one token for each block they mine. In fork mining, miners only receive tokens "
                "for blocks that end up on the longest chain.",
            
            "payoff in each stage": 
                f"At each stage, miners earn tokens for blocks they've mined. Currently, "
                f"in the conservative scenario, the payoffs are {self.conservative_payoffs}. "
                f"In the fork scenario, the payoffs are {self.fork_payoffs}.",
            
            "what is the process": 
                "The process simulates blockchain mining with two strategies: conservative and fork mining. "
                "Conservative miners always build on the longest chain, while fork mining introduces a "
                "competing branch. The simulation demonstrates why conservative mining is a Nash equilibrium strategy.",
            
            "how does it work": 
                "In each stage, a random miner wins the mining competition and adds a block to the chain. "
                "In conservative mining, all miners work on extending the longest chain. "
                "In fork mining, we simulate what happens when a miner deviates from this strategy "
                "by creating a competing branch from an earlier point in the chain."
        }
        
        # Try to find an exact match first
        for pattern, answer in qa_pairs.items():
            if pattern == question_lower:
                return answer
        
        # If no exact match, try partial matching
        for pattern, answer in qa_pairs.items():
            if pattern in question_lower:
                return answer
        
        # Handle questions about specific miners
        for i in range(self.num_miners):
            if f"miner {i+1}" in question_lower:
                cons_payoff = self.conservative_payoffs[i]
                fork_payoff = self.fork_payoffs[i]
                return (f"Miner {i+1} has earned {cons_payoff} tokens in the conservative scenario and "
                       f"{fork_payoff} tokens in the fork scenario.")
        
        # Handle more generic payoff questions
        if "payoff" in question_lower or "reward" in question_lower or "token" in question_lower:
            payoff_summary = "Current payoffs:\n"
            for i in range(self.num_miners):
                payoff_summary += f"Miner {i+1}: {self.conservative_payoffs[i]} tokens (conservative) vs {self.fork_payoffs[i]} tokens (fork)\n"
            return payoff_summary
        
        # Default response for questions we don't understand
        return ("I'm not sure about that. You can ask about conservative mining, forks, payoffs, "
               "specific miners, or the current stage of the simulation. Try asking 'What is the process?' "
               "or 'How does it work?' for a general explanation.")

    def update_simulation_analysis(self):
        """Update the simulation analysis tab with charts and statistics"""
        # Clear previous plots
        self.sim_fig.clear()
        
        # Create a 2x1 grid of subplots
        ax1 = self.sim_fig.add_subplot(211)  # Top plot
        ax2 = self.sim_fig.add_subplot(212)  # Bottom plot
        
        # Plot 1: Miner block distribution
        miner_labels = [f"Miner {i+1}" for i in range(self.num_miners)]
        
        # Count blocks mined by each miner in conservative scenario
        conservative_blocks = [0] * self.num_miners
        for block in self.conservative_chain[1:]:  # Skip genesis block
            if block['miner'] is not None:
                conservative_blocks[block['miner']] += 1
        
        # Count blocks in fork scenario (main chain)
        fork_main_blocks = [0] * self.num_miners
        for block in self.fork_chain[1:self.fork_stage]:  # Before fork
            if block['miner'] is not None:
                fork_main_blocks[block['miner']] += 1
        
        for block in self.fork_chain[self.fork_stage:]:  # After fork, main chain
            if block['miner'] is not None and block['miner'] != self.focal_miner:
                fork_main_blocks[block['miner']] += 1
        
        # Count blocks in forked branch
        fork_branch_blocks = [0] * self.num_miners
        for block in self.fork_alt_chain:
            if block['miner'] is not None:
                fork_branch_blocks[block['miner']] += 1
        
        # Create grouped bar chart for block distribution
        bar_width = 0.25
        x = np.arange(len(miner_labels))
        
        ax1.bar(x - bar_width, conservative_blocks, bar_width, label='Conservative Mining', color='blue', alpha=0.7)
        ax1.bar(x, fork_main_blocks, bar_width, label='Fork - Main Chain', color='green', alpha=0.7)
        ax1.bar(x + bar_width, fork_branch_blocks, bar_width, label='Fork - Branch', color='red', alpha=0.7)
        
        ax1.set_xlabel('Miners', fontsize=10)
        ax1.set_ylabel('Blocks Mined', fontsize=10)
        ax1.set_title('Block Distribution by Miner', fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(miner_labels)
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Plot 2: Payoff comparison over time
        stages = list(range(self.current_stage + 1))
        
        # Create payoff history if it doesn't exist
        if not hasattr(self, 'conservative_payoff_history'):
            self.conservative_payoff_history = [[] for _ in range(self.num_miners)]
            self.fork_payoff_history = [[] for _ in range(self.num_miners)]
        
        # Ensure arrays are the right size
        for i in range(self.num_miners):
            # Extend lists if needed
            while len(self.conservative_payoff_history[i]) <= self.current_stage:
                self.conservative_payoff_history[i].append(0)
            while len(self.fork_payoff_history[i]) <= self.current_stage:
                self.fork_payoff_history[i].append(0)
        
        # Update histories with current values
        for i in range(self.num_miners):
            self.conservative_payoff_history[i][self.current_stage] = self.conservative_payoffs[i]
            self.fork_payoff_history[i][self.current_stage] = self.fork_payoffs[i]
        
        # Plot payoff lines for each miner
        for i in range(self.num_miners):
            # Only plot up to current stage
            cons_data = self.conservative_payoff_history[i][:self.current_stage+1]
            fork_data = self.fork_payoff_history[i][:self.current_stage+1]
            
            ax2.plot(stages, cons_data, '-o', label=f'Miner {i+1} (Conservative)', 
                    color=self.miner_colors[i], alpha=0.8)
            ax2.plot(stages, fork_data, '--o', label=f'Miner {i+1} (Fork)', 
                    color=self.miner_colors[i], alpha=0.5)
        
        # Mark fork stage with vertical line
        if self.current_stage >= self.fork_stage:
            ax2.axvline(x=self.fork_stage, color='red', linestyle='--', 
                       label='Fork Created', alpha=0.7)
        
        ax2.set_xlabel('Stage', fontsize=10)
        ax2.set_ylabel('Payoff (Tokens)', fontsize=10)
        ax2.set_title('Payoff Comparison Over Time', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Only show legend for focal miner and fork line to avoid clutter
        handles, labels = ax2.get_legend_handles_labels()
        selected_handles = []
        selected_labels = []
        
        # Add only the focal miner and the fork line to legend
        for i, label in enumerate(labels):
            if f'Miner {self.focal_miner+1}' in label or 'Fork Created' in label:
                selected_handles.append(handles[i])
                selected_labels.append(labels[i])
        
        ax2.legend(selected_handles, selected_labels, loc='upper left')
        
        # Add text with key statistics
        fork_success = len(self.fork_alt_chain) > (len(self.fork_chain) - self.fork_stage)
        stats_text = (
            f"Current Stage: {self.current_stage}/{self.total_stages}\n"
            f"Fork Stage: {self.fork_stage}\n"
            f"Fork Status: {'Successful' if fork_success else 'Unsuccessful'}\n"
            f"Fork Length: {len(self.fork_alt_chain)} blocks\n"
            f"Main Chain Length: {len(self.fork_chain) - self.fork_stage} blocks (after fork)"
        )
        
        # Add text box with statistics
        self.sim_fig.text(0.02, 0.5, stats_text, transform=self.sim_fig.transFigure,
                         bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
        
        self.sim_fig.tight_layout()
        self.sim_canvas.draw()

def main():
    root = tk.Tk()
    app = BlockchainMiningAnimation(root)
    root.mainloop()

if __name__ == "__main__":
    main() 