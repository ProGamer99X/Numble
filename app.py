import streamlit as st
import random

# --- Helper functions ---

def generate_secret_number():
    # Use random.sample to generate a unique 5-digit number (list of unique digits)
    digits = random.sample(range(10), 5)
    return "".join(str(d) for d in digits)

def check_guess(secret, guess):
    # Initialize feedback list
    feedback = ['gray'] * 5
    secret_used = [False] * 5
    guess_used = [False] * 5

    # First pass: mark greens (correct digit and correct position)
    for i in range(5):
        if guess[i] == secret[i]:
            feedback[i] = 'green'
            secret_used[i] = True
            guess_used[i] = True

    # Second pass: mark yellows (digit exists in secret but in different position)
    for i in range(5):
        if not guess_used[i]:
            for j in range(5):
                if not secret_used[j] and guess[i] == secret[j]:
                    feedback[i] = 'yellow'
                    secret_used[j] = True
                    break

    return feedback

def display_history(history):
    st.markdown("### Previous Guesses:")
    for past_guess, past_feedback in history:
        cols = st.columns(5)
        for i in range(5):
            # Choose colors for feedback:
            if past_feedback[i] == 'green':
                bg_color = "#6aaa64"
                text_color = "white"
            elif past_feedback[i] == 'yellow':
                bg_color = "#f3e078"  # softer yellow
                text_color = "black"
            else:
                bg_color = "#787c7e"
                text_color = "white"
            with cols[i]:
                st.markdown(
                    f"<div style='background-color: {bg_color}; color: {text_color}; "
                    "text-align: center; padding: 8px; border-radius: 5px; font-size: 24px;'>"
                    f"{past_guess[i]}</div>",
                    unsafe_allow_html=True
                )

# --- Initialize session state variables ---
# We use session state to persist values across reruns.
if 'secret' not in st.session_state:
    st.session_state.secret = generate_secret_number()
if 'attempt' not in st.session_state:
    st.session_state.attempt = 0  # attempts from 0 to 5 (6 total)
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_guess' not in st.session_state:
    # current_guess is a list of 5 strings (one per digit)
    st.session_state.current_guess = [""] * 5

# --- App Title ---
st.title("Numble")
st.write("Guess the secret 5-digit number (all digits are unique). You have 6 attempts.")

# --- Input for current guess ---
if st.session_state.attempt < 6 and ("win" not in st.session_state):
    with st.form(key="guess_form"):
        st.markdown("#### Enter your guess:")
        # Create a row of 5 text inputs (one for each digit)
        cols = st.columns(5)
        # For each box, use a unique key based on the current attempt and index.
        for i in range(5):
            # We do not set an initial value here so the box remains empty.
            st.session_state.current_guess[i] = cols[i].text_input(
                label="",
                max_chars=1,
                key=f"digit_{st.session_state.attempt}_{i}"
            )
        submit_button = st.form_submit_button("Enter Guess")
    # Process submission if button pressed:
    if submit_button:
        guess_str = "".join(st.session_state.current_guess)
        if len(guess_str) != 5 or not guess_str.isdigit():
            st.error("Please fill in all 5 boxes with digits (0-9).")
        else:
            feedback = check_guess(st.session_state.secret, guess_str)
            st.session_state.history.append((guess_str, feedback))
            st.session_state.attempt += 1
            # Clear current_guess for next attempt
            st.session_state.current_guess = [""] * 5
            st.rerun()  # Rerun to update the UI

# --- Display Guess History ---
if st.session_state.history:
    display_history(st.session_state.history)

# --- Win/Lose Conditions ---
if st.session_state.history:
    last_guess, last_feedback = st.session_state.history[-1]
    if last_feedback == ['green'] * 5:
        st.success("🎉 Congratulations! You've guessed the secret number!")
        st.session_state.win = True
    elif st.session_state.attempt >= 6:
        st.error(f"Game Over! The secret number was: {st.session_state.secret}")

# --- Restart Game Button ---
if st.button("Restart Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

