import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MiningFlowchartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Mining Strategy Flowcharts")
        self.root.geometry("1200x800")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create two tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Conservative Mining Flowchart
        conservative_tab = ttk.Frame(notebook, padding=10)
        notebook.add(conservative_tab, text="Conservative Mining")
        
        # Tab 2: Fork Mining Flowchart
        fork_tab = ttk.Frame(notebook, padding=10)
        notebook.add(fork_tab, text="Fork Mining (Deviation)")
        
        # Tab 3: Comparison
        comparison_tab = ttk.Frame(notebook, padding=10)
        notebook.add(comparison_tab, text="Strategy Comparison")
        
        # Create flowcharts
        self.create_conservative_flowchart(conservative_tab)
        self.create_fork_flowchart(fork_tab)
        self.create_comparison_flowchart(comparison_tab)

    def create_conservative_flowchart(self, parent):
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.tight_layout(pad=3)
        
        # Turn off axis
        ax.axis('off')
        
        # Adjust node positions - increase vertical spacing
        nodes = {
            'start': (0.5, 0.95),
            'find_longest': (0.5, 0.8),
            'mine_block': (0.5, 0.65),
            'win_mining': (0.5, 0.5),
            'yes_path': (0.25, 0.35),
            'no_path': (0.75, 0.35),
            'add_block': (0.25, 0.2),
            'receive_token': (0.25, 0.05),
            'try_again': (0.75, 0.2)
        }
        
        # Create nodes (with colors)
        self.draw_node(ax, nodes['start'], 'Start Mining', 'lightblue')
        self.draw_node(ax, nodes['find_longest'], 'Find Longest Chain', 'lightgreen')
        self.draw_node(ax, nodes['mine_block'], 'Mine Block on\nLongest Chain', 'lightgreen')
        self.draw_node(ax, nodes['win_mining'], 'Win Mining\nCompetition?', 'gold', is_decision=True)
        self.draw_node(ax, nodes['add_block'], 'Add Block to\nBlockchain', 'lightgreen')
        self.draw_node(ax, nodes['receive_token'], 'Receive Token\nReward', 'lightcoral')
        self.draw_node(ax, nodes['try_again'], 'Try Again\nNext Round', 'lightcyan')
        
        # Create edges with arrows
        self.draw_arrow(ax, nodes['start'], nodes['find_longest'])
        self.draw_arrow(ax, nodes['find_longest'], nodes['mine_block'])
        self.draw_arrow(ax, nodes['mine_block'], nodes['win_mining'])
        self.draw_arrow(ax, nodes['win_mining'], nodes['yes_path'], 'Yes')
        self.draw_arrow(ax, nodes['win_mining'], nodes['no_path'], 'No')
        self.draw_arrow(ax, nodes['yes_path'], nodes['add_block'])
        self.draw_arrow(ax, nodes['add_block'], nodes['receive_token'])
        self.draw_arrow(ax, nodes['no_path'], nodes['try_again'])
        
        # Add loop back arrow
        self.draw_curved_arrow(ax, nodes['try_again'], nodes['find_longest'], 'Next round')
        self.draw_curved_arrow(ax, nodes['receive_token'], nodes['find_longest'], 'Next round')
        
        # Title
        ax.set_title('Conservative Mining Process', fontsize=14, fontweight='bold')
        
        # Add explanation text - position it carefully to not overlap
        explanation = (
            "Conservative Mining Strategy:\n\n"
            "• Always mine on the longest chain\n"
            "• Guaranteed to receive tokens for every block mined\n"
            "• Forms a Nash equilibrium - no incentive to deviate\n"
            "• Maximizes expected rewards over time\n"
            "• All miners coordinate on a single chain"
        )
        
        # Move explanation box to bottom right
        ax.text(0.98, 0.02, explanation, transform=ax.transAxes, fontsize=9,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_fork_flowchart(self, parent):
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.tight_layout(pad=3)
        
        # Turn off axis
        ax.axis('off')
        
        # Node positions
        nodes = {
            'start': (0.5, 0.95),
            'choose_chain': (0.5, 0.85),
            'fork_decision': (0.5, 0.75),
            'longest_chain': (0.25, 0.65),
            'earlier_block': (0.75, 0.65),
            'mine_longest': (0.25, 0.55),
            'mine_fork': (0.75, 0.55),
            'win_longest': (0.25, 0.45),
            'win_fork': (0.75, 0.45),
            'add_regular': (0.25, 0.35),
            'add_fork': (0.75, 0.35),
            'fork_longest': (0.75, 0.25),
            'tokens_regular': (0.25, 0.15),
            'tokens_yes': (0.65, 0.15),
            'tokens_no': (0.85, 0.15),
            'try_again': (0.5, 0.05)
        }
        
        # Create nodes
        self.draw_node(ax, nodes['start'], 'Start Mining', 'lightblue')
        self.draw_node(ax, nodes['choose_chain'], 'Choose Block to\nMine Upon', 'lightgreen')
        self.draw_node(ax, nodes['fork_decision'], 'Mine on Longest\nChain?', 'gold', is_decision=True)
        self.draw_node(ax, nodes['longest_chain'], 'Select\nLongest Chain', 'lightgreen')
        self.draw_node(ax, nodes['earlier_block'], 'Select Earlier\nBlock (Create Fork)', 'lightcoral')
        self.draw_node(ax, nodes['mine_longest'], 'Mine on\nLongest Chain', 'lightgreen')
        self.draw_node(ax, nodes['mine_fork'], 'Mine on\nFork Chain', 'lightcoral')
        self.draw_node(ax, nodes['win_longest'], 'Win Mining?', 'gold', is_decision=True, smaller=True)
        self.draw_node(ax, nodes['win_fork'], 'Win Mining?', 'gold', is_decision=True, smaller=True)
        self.draw_node(ax, nodes['add_regular'], 'Add to\nMain Chain', 'lightgreen', smaller=True)
        self.draw_node(ax, nodes['add_fork'], 'Add to\nFork Chain', 'lightcoral', smaller=True)
        self.draw_node(ax, nodes['fork_longest'], 'Fork Becomes\nLongest?', 'gold', is_decision=True, smaller=True)
        self.draw_node(ax, nodes['tokens_regular'], 'Receive Token', 'lightgreen', smaller=True)
        self.draw_node(ax, nodes['tokens_yes'], 'Receive Tokens', 'lightgreen', smaller=True)
        self.draw_node(ax, nodes['tokens_no'], 'No Tokens', 'lightcoral', smaller=True)
        self.draw_node(ax, nodes['try_again'], 'Next Round', 'lightcyan')
        
        # Create edges with arrows
        self.draw_arrow(ax, nodes['start'], nodes['choose_chain'])
        self.draw_arrow(ax, nodes['choose_chain'], nodes['fork_decision'])
        self.draw_arrow(ax, nodes['fork_decision'], nodes['longest_chain'], 'Yes (Conservative)')
        self.draw_arrow(ax, nodes['fork_decision'], nodes['earlier_block'], 'No (Deviation)')
        self.draw_arrow(ax, nodes['longest_chain'], nodes['mine_longest'])
        self.draw_arrow(ax, nodes['earlier_block'], nodes['mine_fork'])
        self.draw_arrow(ax, nodes['mine_longest'], nodes['win_longest'])
        self.draw_arrow(ax, nodes['mine_fork'], nodes['win_fork'])
        self.draw_arrow(ax, nodes['win_longest'], nodes['add_regular'], 'Yes')
        self.draw_arrow(ax, nodes['win_fork'], nodes['add_fork'], 'Yes')
        self.draw_arrow(ax, nodes['add_regular'], nodes['tokens_regular'])
        self.draw_arrow(ax, nodes['add_fork'], nodes['fork_longest'])
        self.draw_arrow(ax, nodes['fork_longest'], nodes['tokens_yes'], 'Yes')
        self.draw_arrow(ax, nodes['fork_longest'], nodes['tokens_no'], 'No')
        
        # Add convergence arrows to try_again
        self.draw_arrow(ax, nodes['tokens_regular'], nodes['try_again'])
        self.draw_arrow(ax, nodes['tokens_yes'], nodes['try_again'])
        self.draw_arrow(ax, nodes['tokens_no'], nodes['try_again'])
        self.draw_arrow(ax, (0.25, 0.4), nodes['try_again'], 'No', start_offset=(0, -0.05), end_offset=(0, 0.05))
        self.draw_arrow(ax, (0.75, 0.4), nodes['try_again'], 'No', start_offset=(0, -0.05), end_offset=(0, 0.05))
        
        # Loop back to start
        self.draw_curved_arrow(ax, nodes['try_again'], nodes['start'], direction='left')
        
        # Title
        ax.set_title('Fork Mining Process (Deviation Strategy)', fontsize=16, fontweight='bold')
        
        # Add explanation text
        explanation = (
            "Fork Mining Strategy (Deviation):\n\n"
            "• Create a fork by mining on a non-tip block\n"
            "• Only receive tokens if fork becomes longest chain\n"
            "• Risk of wasted mining effort\n"
            "• Expected payoff never higher than conservative\n"
            "• Can lead to lower rewards (but never higher)"
        )
        
        # Add text box at bottom right
        ax.text(0.95, 0.05, explanation, transform=ax.transAxes, fontsize=10,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_comparison_flowchart(self, parent):
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.tight_layout(pad=3)
        
        # Turn off axis
        ax.axis('off')
        
        # Draw comparison table
        table_data = [
            ['Strategy', 'Mining Approach', 'Payoff Guarantee', 'Risk Level', 'Nash Equilibrium?'],
            ['Conservative Mining', 'Always extend longest chain', 'Token for each block mined', 'Low', 'Yes'],
            ['Fork Mining', 'Create competing chain', 'Only if fork becomes longest', 'High', 'No']
        ]
        
        table = ax.table(cellText=table_data, loc='center', cellLoc='center',
                       colWidths=[0.2, 0.25, 0.25, 0.15, 0.15])
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)  # Make rows taller
        
        # Color the header row
        for i in range(len(table_data[0])):
            table[(0, i)].set_facecolor('#4472C4')
            table[(0, i)].set_text_props(color='white', fontweight='bold')
        
        # Color the strategy row cells
        for i in range(len(table_data[0])):
            table[(1, i)].set_facecolor('#D9E1F2')  # Light blue for conservative
            table[(2, i)].set_facecolor('#FCE4D6')  # Light orange for fork
        
        # Create payoff matrix
        # Add title for payoff matrix
        ax.text(0.5, 0.3, "Expected Payoff Comparison", fontsize=14, fontweight='bold',
               ha='center', va='center')
        
        payoff_data = [
            ['', 'Conservative Mining', 'Fork Mining'],
            ['Expected Tokens', '1 per block mined', '≤ 1 per block mined'],
            ['Wasted Blocks', 'None', 'Potential if fork fails'],
            ['Best Strategy', 'Yes', 'No']
        ]
        
        payoff_table = ax.table(cellText=payoff_data, loc='center', cellLoc='center',
                              cellColours=[['#F2F2F2', '#D9E1F2', '#FCE4D6'],
                                          ['#F2F2F2', '#D9E1F2', '#FCE4D6'],
                                          ['#F2F2F2', '#D9E1F2', '#FCE4D6'],
                                          ['#F2F2F2', '#D9E1F2', '#FCE4D6']],
                              bbox=[0.25, 0.05, 0.5, 0.2])
        
        # Style the payoff table
        payoff_table.auto_set_font_size(False)
        payoff_table.set_fontsize(12)
        payoff_table.scale(1, 1.5)  # Make rows taller
        
        # Title
        ax.set_title('Comparison of Mining Strategies', fontsize=16, fontweight='bold')
        
        # Conclusion text
        conclusion = (
            "Conclusion:\n\n"
            "Conservative mining forms a Nash equilibrium: no miner has incentive to deviate from this strategy.\n"
            "Fork mining can only result in equal or lower expected payoffs compared to conservative mining.\n"
            "This explains why rational miners in blockchain systems all adopt the conservative strategy."
        )
        
        ax.text(0.5, 0.42, conclusion, fontsize=12, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#E2EFDA', alpha=0.8))
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_node(self, ax, pos, text, color, is_decision=False, smaller=False):
        x, y = pos
        if is_decision:
            # Diamond shape for decisions - smaller size
            width = 0.12 if not smaller else 0.08
            height = 0.06 if not smaller else 0.04
            diamond = plt.Polygon([[x, y+height], [x+width, y], [x, y-height], [x-width, y]],
                                 facecolor=color, edgecolor='black', alpha=0.7)
            ax.add_patch(diamond)
        else:
            # Rectangle for normal nodes - smaller size
            width = 0.12 if not smaller else 0.08
            height = 0.05 if not smaller else 0.035
            rect = plt.Rectangle((x-width, y-height), 2*width, 2*height,
                                facecolor=color, edgecolor='black', alpha=0.7)
            ax.add_patch(rect)
        
        # Add text - smaller font
        fontsize = 8 if not smaller else 6
        ax.text(x, y, text, horizontalalignment='center', verticalalignment='center',
               fontsize=fontsize, fontweight='bold', 
               bbox=dict(facecolor='white', alpha=0.0, boxstyle='round,pad=0.2', edgecolor='none'))

    def draw_arrow(self, ax, start_pos, end_pos, label=None, start_offset=(0, 0), end_offset=(0, 0)):
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Apply offsets
        x1 += start_offset[0]
        y1 += start_offset[1]
        x2 += end_offset[0]
        y2 += end_offset[1]
        
        # Draw arrow - thinner line
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
        
        # Add label if provided
        if label:
            # Calculate midpoint with slight offset
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Add slight offset based on direction
            offset_x = (y2 - y1) * 0.04
            offset_y = -(x2 - x1) * 0.04
            
            # Smaller label with better visibility
            ax.text(mid_x + offset_x, mid_y + offset_y, label, 
                   horizontalalignment='center', verticalalignment='center',
                   fontsize=7, bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.1', edgecolor='none'))

    def draw_curved_arrow(self, ax, start_pos, end_pos, label=None, direction='right'):
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Create a connection path with a curve
        if direction == 'right':
            connectionstyle = "arc3,rad=0.3"
        else:
            connectionstyle = "arc3,rad=-0.3"
            
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5, 
                                 connectionstyle=connectionstyle))
        
        # Add label if provided
        if label:
            # Calculate a point along the curve for the label
            if direction == 'right':
                mid_x = (x1 + x2) / 2 + 0.1
                mid_y = (y1 + y2) / 2
            else:
                mid_x = (x1 + x2) / 2 - 0.1
                mid_y = (y1 + y2) / 2
                
            ax.text(mid_x, mid_y, label, 
                   horizontalalignment='center', verticalalignment='center',
                   fontsize=8, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

def main():
    root = tk.Tk()
    app = MiningFlowchartApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 