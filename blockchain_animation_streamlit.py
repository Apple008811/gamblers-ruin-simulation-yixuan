import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np

class BlockchainMiningSimulation:
    def __init__(self):
        # Animation parameters
        self.num_miners = 4
        self.miner_colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        self.focal_miner = 1
        self.total_stages = 10
        self.conservative_payoffs = [0] * self.num_miners
        self.fork_payoffs = [0] * self.num_miners
        
        # Initialize blockchain state
        self.init_blockchain()
    
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
        
        # Initialize payoff history for analysis
        self.conservative_payoff_history = [[] for _ in range(self.num_miners)]
        self.fork_payoff_history = [[] for _ in range(self.num_miners)]
    
    def draw_blockchain(self, fig, ax, chains):
        ax.clear()
        
        # Set up the plot
        ax.set_xlim(-1, 12)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        
        # Draw main chain
        main_chain = chains[0]
        for i in range(len(main_chain)):
            # Draw block
            block = main_chain[i]
            x = i
            y = 0
            
            if block['miner'] is not None:
                color = self.miner_colors[block['miner']]
            else:
                color = '#cccccc'  # Genesis block color
                
            rect = plt.Rectangle((x-0.4, y-0.3), 0.8, 0.6, 
                               facecolor=color, edgecolor='black')
            ax.add_patch(rect)
            
            # Add stage number
            ax.text(x, y, str(block['stage']), 
                   ha='center', va='center', color='white')
            
            # Draw connection line
            if i > 0:
                ax.plot([x-1, x], [y, y], 'k-', linewidth=2)
        
        # Draw fork chain if it exists
        if len(chains) > 1 and len(chains[1]) > 0:
            fork_chain = chains[1]
            fork_start = len(main_chain) - len(fork_chain)
            
            for i in range(len(fork_chain)):
                block = fork_chain[i]
                x = fork_start + i
                y = -1
                
                color = self.miner_colors[block['miner']]
                rect = plt.Rectangle((x-0.4, y-0.3), 0.8, 0.6, 
                                   facecolor=color, edgecolor='black')
                ax.add_patch(rect)
                
                # Add stage number
                ax.text(x, y, str(block['stage']), 
                       ha='center', va='center', color='white')
                
                # Draw connection lines
                if i == 0:
                    ax.plot([x, x], [0, y], 'k--', linewidth=2)
                elif i > 0:
                    ax.plot([x-1, x], [y, y], 'k--', linewidth=2)

def main():
    st.set_page_config(page_title="Blockchain Mining Simulation", layout="wide")
    
    st.title("Blockchain Conservative Mining Simulation")
    
    # Sidebar controls
    st.sidebar.header("Simulation Controls")
    
    # Description
    st.sidebar.markdown("""
    This simulation demonstrates why miners have no incentive to deviate 
    from the conservative mining strategy (always mining on the longest chain).
    """)
    
    # Miner information
    st.sidebar.subheader("Miners")
    simulation = BlockchainMiningSimulation()
    
    for i in range(simulation.num_miners):
        label_text = f"Miner {i+1}" + (" (Focus)" if i == simulation.focal_miner else "")
        st.sidebar.markdown(
            f'<div style="background-color: {simulation.miner_colors[i]}; '
            f'color: white; padding: 5px; border-radius: 5px;">{label_text}</div>',
            unsafe_allow_html=True
        )
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs([
        "Conservative Mining", 
        "Fork Mining (Deviation)", 
        "Simulation Analysis"
    ])
    
    # Conservative Mining Tab
    with tab1:
        st.subheader("Conservative Mining Strategy")
        fig_conservative, ax_conservative = plt.subplots(figsize=(10, 6))
        simulation.draw_blockchain(fig_conservative, ax_conservative, 
                                 [simulation.conservative_chain])
        st.pyplot(fig_conservative)
        
        # Add explanation
        st.markdown("""
        In conservative mining, miners always build on the longest chain.
        This strategy leads to a single, growing blockchain with no forks.
        """)
    
    # Fork Mining Tab
    with tab2:
        st.subheader("Fork Mining Strategy")
        fig_fork, ax_fork = plt.subplots(figsize=(10, 6))
        simulation.draw_blockchain(fig_fork, ax_fork, 
                                 [simulation.fork_chain, simulation.fork_alt_chain])
        st.pyplot(fig_fork)
        
        # Add explanation
        st.markdown("""
        In fork mining, a miner might try to create an alternative chain.
        This strategy is risky as it may lead to wasted mining effort.
        """)
    
    # Simulation Analysis Tab
    with tab3:
        st.subheader("Payoff Analysis")
        
        # Create payoff comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Conservative Strategy Payoffs")
            for i in range(simulation.num_miners):
                st.text(f"Miner {i+1}: {simulation.conservative_payoffs[i]}")
        
        with col2:
            st.markdown("### Fork Strategy Payoffs")
            for i in range(simulation.num_miners):
                st.text(f"Miner {i+1}: {simulation.fork_payoffs[i]}")
    
    # Interactive Q&A section
    st.markdown("---")
    st.subheader("Interactive Q&A")
    
    # Text input for questions
    user_question = st.text_input("Ask a question about blockchain mining:")
    
    if user_question:
        # Simple Q&A logic
        if "what is blockchain" in user_question.lower():
            st.markdown("""
            A blockchain is a distributed ledger that maintains a growing list of records (blocks) 
            that are linked using cryptography. Each block contains transaction data, a timestamp, 
            and a cryptographic hash of the previous block.
            """)
        elif "conservative mining" in user_question.lower():
            st.markdown("""
            Conservative mining is a strategy where miners always build on the longest chain. 
            This strategy helps maintain blockchain consensus and avoid wasting resources on forks.
            """)
        elif "fork" in user_question.lower():
            st.markdown("""
            A fork occurs when there are two competing chains in the blockchain. This can happen 
            when miners build on different blocks, creating parallel chains. Usually, the longest 
            chain becomes the accepted one.
            """)
        else:
            st.markdown("""
            That's an interesting question! The simulation shows how different mining strategies 
            affect blockchain growth and miner rewards. Conservative mining (building on the longest chain) 
            tends to be the most profitable strategy in the long run.
            """)

if __name__ == "__main__":
    main() 