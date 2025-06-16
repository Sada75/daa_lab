import streamlit as st
import numpy as np
import time
import pandas as pd # Import pandas for data manipulation with charts

# Initialize session state
def init_session_state():
    if 'board' not in st.session_state:
        st.session_state.board = np.zeros((3, 3))
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'player' not in st.session_state:
        st.session_state.player = 1
    if 'player_starts' not in st.session_state:
        st.session_state.player_starts = True
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    # Initialize analysis tracking variables
    if 'player_wins' not in st.session_state:
        st.session_state.player_wins = 0
    if 'computer_wins' not in st.session_state:
        st.session_state.computer_wins = 0
    if 'draws' not in st.session_state:
        st.session_state.draws = 0
    if 'total_games' not in st.session_state:
        st.session_state.total_games = 0

# Game logic functions
def available_square(row, col):
    return st.session_state.board[row][col] == 0

def mark_square(row, col, player):
    st.session_state.board[row][col] = player

def is_board_full(check_board=None):
    if check_board is None:
        check_board = st.session_state.board
    for row in range(3):
        for col in range(3):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=None):
    if check_board is None:
        check_board = st.session_state.board
    
    # Check columns
    for col in range(3):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    
    # Check rows
    for row in range(3):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    
    # Check diagonals
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

# Minimax algorithm with Alpha-Beta pruning
def minimax(minimax_board, depth, is_maximising, alpha, beta):
    if check_win(2, minimax_board):
        return 10 - depth
    elif check_win(1, minimax_board):
        return depth - 10
    elif is_board_full(minimax_board):
        return 0

    if is_maximising:
        max_eval = -float('inf')
        for row in range(3):
            for col in range(3):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    eval = minimax(minimax_board, depth + 1, False, alpha, beta)
                    minimax_board[row][col] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    eval = minimax(minimax_board, depth + 1, True, alpha, beta)
                    minimax_board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    best_score = -1000
    move = (-1, -1)
    
    board_copy = st.session_state.board.copy()
    
    for row in range(3):
        for col in range(3):
            if board_copy[row][col] == 0:
                board_copy[row][col] = 2
                score = minimax(board_copy, 0, False, -float('inf'), float('inf'))
                board_copy[row][col] = 0
                
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    st.session_state.board = np.zeros((3, 3))
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.game_started = False
    # Don't reset win/loss/draw counts here to keep cumulative stats

def reset_analysis_data():
    st.session_state.player_wins = 0
    st.session_state.computer_wins = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0

def get_cell_symbol(value):
    if value == 1:
        return "⭕"
    elif value == 2:
        return "❌"
    else:
        return ""

def get_cell_color(row, col):
    if st.session_state.winner == "player" and st.session_state.board[row][col] == 1:
        return "background-color: #90EE90; color: #006400; font-weight: bold;"
    elif st.session_state.winner == "computer" and st.session_state.board[row][col] == 2:
        return "background-color: #FFB6C1; color: #8B0000; font-weight: bold;"
    elif st.session_state.winner == "draw":
        return "background-color: #D3D3D3; color: #696969; font-weight: bold;"
    else:
        return "background-color: #f0f0f0; color: #333; font-weight: bold;"

# Streamlit UI
def main():
    st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="🎮", layout="centered")
    
    init_session_state()
    
    # Inject custom CSS for sidebar radio button font size
    st.markdown(
        """
        <style>
        .stRadio > label {
            font-size: 1.2em !important; /* Adjust the value as needed */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🎮 Tic-Tac-Toe vs AI")
    st.markdown("---")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        app_mode = st.radio("Choose a section", ["🕹️ Game", "📊 Analysis"])

    if app_mode == "🕹️ Game":
        # Game setup
        if not st.session_state.game_started:
            st.subheader("🚀 Game Setup")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👤 Player Starts", use_container_width=True, type="primary"):
                    st.session_state.player_starts = True
                    st.session_state.player = 1
                    st.session_state.game_started = True
                    st.rerun()
            
            with col2:
                if st.button("🤖 Computer Starts", use_container_width=True):
                    st.session_state.player_starts = False
                    st.session_state.player = 2
                    st.session_state.game_started = True
                    # Computer makes first move
                    best_move()
                    st.session_state.player = 1
                    st.rerun()
            
            st.markdown("### 📋 How to Play:")
            st.markdown("- **Player**: ⭕ (Circle)")
            st.markdown("- **Computer**: ❌ (Cross)")
            st.markdown("- Click on any empty cell to make your move")
            st.markdown("- The AI uses Minimax algorithm - it's unbeatable!")
            
        else:
            # Game board
            st.subheader("🎯 Game Board")
            
            # Display current player
            if not st.session_state.game_over:
                if st.session_state.player == 1:
                    st.info("👤 Your turn! (⭕)")
                else:
                    st.warning("🤖 Computer's turn... (❌)")
            
            # Create the game board
            for row in range(3):
                cols = st.columns(3)
                for col in range(3):
                    with cols[col]:
                        cell_value = st.session_state.board[row][col]
                        symbol = get_cell_symbol(cell_value)
                        
                        # Create button with styling
                        button_style = get_cell_color(row, col)
                        
                        if st.button(
                            symbol if symbol else "⬜", 
                            key=f"cell_{row}_{col}",
                            use_container_width=True,
                            disabled=st.session_state.game_over or cell_value != 0 or st.session_state.player != 1
                        ):
                            if available_square(row, col) and st.session_state.player == 1 and not st.session_state.game_over:
                                # Player move
                                mark_square(row, col, 1)
                                
                                # Check if player wins
                                if check_win(1):
                                    st.session_state.game_over = True
                                    st.session_state.winner = "player"
                                elif is_board_full():
                                    st.session_state.game_over = True
                                    st.session_state.winner = "draw"
                                else:
                                    # Computer move
                                    st.session_state.player = 2
                                    time.sleep(0.5)  # Small delay for better UX
                                    
                                    if best_move():
                                        if check_win(2):
                                            st.session_state.game_over = True
                                            st.session_state.winner = "computer"
                                        elif is_board_full():
                                            st.session_state.game_over = True
                                            st.session_state.winner = "draw"
                                        else:
                                            st.session_state.player = 1
                                
                                st.rerun()
            
            # Game result
            if st.session_state.game_over:
                st.session_state.total_games += 1 # Increment total games played
                if st.session_state.winner == "player":
                    st.success("🎉 Congratulations! You won!")
                    st.balloons()
                    st.session_state.player_wins += 1 # Increment player wins
                elif st.session_state.winner == "computer":
                    st.error("🤖 Computer wins! Better luck next time!")
                    st.session_state.computer_wins += 1 # Increment computer wins
                else:
                    st.info("🤝 It's a draw! Good game!")
                    st.session_state.draws += 1 # Increment draws
                
                st.markdown("---")
                # Restart options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Play Again", use_container_width=True, type="primary"):
                        restart_game()
                        st.rerun()
                
                with col2:
                    if st.button("⚙️ New Game Setup", use_container_width=True):
                        restart_game()
                        st.rerun()

    elif app_mode == "📊 Analysis":
        st.subheader("📈 Game Analysis")
        st.markdown("Here you can see the overall statistics of games played.")

        if st.session_state.total_games == 0:
            st.info("No games played yet. Start a game to see the analysis!")
        else:
            total = st.session_state.total_games
            player_win_rate = (st.session_state.player_wins / total) * 100
            computer_win_rate = (st.session_state.computer_wins / total) * 100
            draw_rate = (st.session_state.draws / total) * 100

            st.metric("Total Games Played", total)
            
            st.write("### Win/Loss/Draw Breakdown:")
            st.markdown(f"- Player Wins: **{st.session_state.player_wins}** ({player_win_rate:.2f}%)")
            st.markdown(f"- Computer Wins: **{st.session_state.computer_wins}** ({computer_win_rate:.2f}%)")
            st.markdown(f"- Draws: **{st.session_state.draws}** ({draw_rate:.2f}%)")

            # Create a DataFrame for charting
            data = {
                'Outcome': ['Player Wins', 'Computer Wins', 'Draws'],
                'Count': [st.session_state.player_wins, st.session_state.computer_wins, st.session_state.draws]
            }
            df = pd.DataFrame(data)

            st.bar_chart(df.set_index('Outcome'))
            
            st.markdown("---")
            st.write("### Insights from the Data:")
            st.markdown(
                """
                The Minimax algorithm with Alpha-Beta pruning is designed to play optimally,
                meaning it will either win or force a draw. Based on the game theory of Tic-Tac-Toe,
                if both players play perfectly, the game will always end in a draw.

                From the chart above, you should generally observe:
                - **High Percentage of Draws:** This indicates that the AI is playing optimally and
                  the human player is also making strong moves, leading to a balanced outcome.
                - **Computer Wins:** If the computer registers wins, it means the human player
                  made a non-optimal move, allowing the AI to capitalize and secure a victory.
                - **Player Wins:** These should be rare, or ideally zero, if the AI is truly unbeatable.
                  A player win would indicate a flaw in the AI's logic or a scenario not perfectly handled.

                These results reaffirm the effectiveness of the Minimax algorithm in achieving
                optimal play in deterministic, perfect-information games like Tic-Tac-Toe.
                """
            )

            st.markdown("---")
            st.write("Click 'Reset Analysis Data' to clear all game statistics.")
            if st.button("Reset Analysis Data", type="secondary"):
                reset_analysis_data()
                st.rerun()


if __name__ == "__main__":
    main()
