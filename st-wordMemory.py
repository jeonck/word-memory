import streamlit as st
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh
import time

# Load the CSV file
df = pd.read_csv('wordbook.csv')

# List of emojis related to learning, exercise, and food
emojis = ['📚', '✏️', '📖', '📝', '🧠', '💡', '🎓', '📅', '🏫', '🖋️', '🏋️', '🚴', '🥗', '🍎', '🍕', '🍔', '🍣', '🥑', '🥦', '🏃']

# Function to get random words and emojis
def get_random_words_and_emojis(data, num=1):
    words = data.sample(n=num)
    words['emoji'] = [random.choice(emojis) for _ in range(num)]
    return words

# Set up the Streamlit app
st.title('단어 암기 앱')

# Initialize session state
if 'random_words' not in st.session_state:
    st.session_state.random_words = pd.DataFrame()
    st.session_state.start_time = time.time()
    st.session_state.words_history = pd.DataFrame()
    st.session_state.review_mode = False
    st.session_state.review_cycle = 0
    st.session_state.review_index = 0
    st.session_state.study_history = []

# Auto-refresh every 3 seconds (3000 milliseconds)
if st_autorefresh(interval=3000, limit=None, key="autorefresh"):
    # Check if 30 seconds have passed for the study phase
    if time.time() - st.session_state.start_time > 30 and not st.session_state.review_mode:
        st.session_state.start_time = time.time()
        st.session_state.study_history = st.session_state.study_history[-10:]  # Keep last 10 words
        st.session_state.words_history = pd.DataFrame(st.session_state.study_history)
        st.session_state.review_mode = True
        st.session_state.review_cycle = 1
        st.session_state.review_index = 0
        st.write("<h2 style='text-align: center; color: red;'>복습 시작</h2>", unsafe_allow_html=True)

    # Update random words if in study mode
    if not st.session_state.review_mode:
        new_word = get_random_words_and_emojis(df)
        st.session_state.random_words = new_word
        st.session_state.study_history.append(new_word.iloc[0])
    else:
        # Handle review mode
        if st.session_state.review_cycle == 1:
            if st.session_state.review_index < len(st.session_state.words_history):
                st.session_state.random_words = st.session_state.words_history.iloc[[st.session_state.review_index]]
                st.session_state.review_index += 1
            else:
                st.session_state.review_cycle = 2
                st.session_state.review_index = 0
                st.write("<h2 style='text-align: center; color: orange;'>복습 시작 (역순)</h2>", unsafe_allow_html=True)
        elif st.session_state.review_cycle == 2:
            if st.session_state.review_index < len(st.session_state.words_history):
                st.session_state.random_words = st.session_state.words_history.iloc[[-(st.session_state.review_index + 1)]]
                st.session_state.review_index += 1
            else:
                st.session_state.review_cycle = 3
                st.session_state.review_index = 0
                st.write("<h2 style='text-align: center; color: green;'>복습 시작 (단어만)</h2>", unsafe_allow_html=True)
        elif st.session_state.review_cycle == 3:
            if st.session_state.review_index < len(st.session_state.words_history):
                st.session_state.random_words = st.session_state.words_history.iloc[[st.session_state.review_index]]
                st.session_state.review_index += 1
            else:
                # After reviewing all words, display "다시 시작" and move to next set of random words
                st.write("<h2 style='text-align: center; color: blue;'>다음 단어</h2>", unsafe_allow_html=True)
                st.session_state.random_words = get_random_words_and_emojis(df)
                st.session_state.start_time = time.time()
                st.session_state.review_mode = False
                st.session_state.review_cycle = 0
                st.session_state.review_index = 0
                st.session_state.study_history = []

# Button for next set of words
if st.button('다음 단어 보기'):
    st.session_state.random_words = get_random_words_and_emojis(df)
    st.session_state.start_time = time.time()  # Reset the timer
    st.session_state.review_mode = False  # Exit review mode
    st.session_state.review_cycle = 0  # Reset review cycle
    st.session_state.review_index = 0  # Reset review index
    st.session_state.study_history = []  # Clear study history

st.write("---")
random_words = st.session_state.random_words
for index, row in random_words.iterrows():
    if st.session_state.review_cycle == 3:
        st.write(f"<h1 style='text-align: left; font-size: 48px;'>{row['emoji']} {row['단어']}</h1>", unsafe_allow_html=True)
    else:
        st.write(f"<h1 style='text-align: left; font-size: 48px;'>{row['emoji']} {row['단어']}</h1>", unsafe_allow_html=True)
        st.write(f"<p style='text-align: center; font-size: 24px;'>{row['주요뜻']}</p>", unsafe_allow_html=True)
    st.write("")

# App layout similar to the provided design
st.write("---")
