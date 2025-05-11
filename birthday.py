import streamlit as st
import time

# --- Configuration ---
PAGE_TITLE = "A Special Birthday Adventure!"
PAGE_ICON = "🥳"
GIRLFRIEND_PET_NAME = "Cutie"

# --- Clue Data (with custom success messages) ---
ALL_CLUES = [
    {
        "id": 1,
        "question": "The first gift I ever gave you was small, but meant a lot (I hope!). It was a sweet treat to win your heart. What was it?",
        "answer": "chocolate",
        "hint1": "It melts in your mouth, not in your hand (usually!).",
        "hint2": "Often comes in a bar or fancy box.",
        "success_message": f"Yes! That chocolate was almost as sweet as you, {GIRLFRIEND_PET_NAME}! 😉"
    },
    {
        "id": 2,
        "question": "What's that wonderfully silly nickname you call me when you lovingly hold my stomach?",
        "answer": "motu",
        "hint1": "It's a term of endearment, often used for someone a bit... 'cuddly' in a cute way!",
        "hint2": "It rhymes with 'lotu' or 'gotu'.",
        "success_message": "Haha, Motu it is! You have always known how to make me smile. You're doing great!"
    },
    {
        "id": 3,
        "question": f"If we adopted a super cute Dog tomorrow, what's the wonderfully quirky name YOU would pick out for our new furry friend, {GIRLFRIEND_PET_NAME}?",
        "answer": "*",
        "hint1": "There's no wrong answer here, just your amazing creativity!",
        "hint2": "Think of the silliest, cutest, or most epic name you can imagine!",
        "success_message": "That's a PERFECT name! Always loved your imagination."
    },
    {
        "id": 4,
        "question": "Remember our early dating days? Which majestic, historical monument did we explore first together in Delhi?",
        "answer": "humayun tomb",
        "hint1": "It's a beautiful example of Mughal architecture and a precursor to the Taj Mahal.",
        "hint2": "Its name honors a famous Mughal emperor.",
        "success_message": "Spot on! Humayun's Tomb was beautiful but not as beautiful as our day there. And not as huge as your heart is!"
    },
    {
        "id": 5,
        "question": "We cheered our hearts out! Which nation was India playing against when we experienced our first live cricket match together?",
        "answer": "afghanistan",
        "hint1": "They are known for their passionate players and rising presence in international cricket.",
        "hint2": "Their flag features black, red, and green vertical stripes with an emblem.",
        "success_message": f"Yes, Afghanistan! That match was so exciting, especially with you by my side, {GIRLFRIEND_PET_NAME}. You're on a roll!"
    },
    {
        "id": 6,
        "question": f"Even with all the action on the field, who was truly my favorite person to look at during that cricket match, {GIRLFRIEND_PET_NAME}? (Just her first name!)",
        "answer": "divya", # ASSUMPTION: Girlfriend's actual first name. CHANGE THIS IF INCORRECT.
        "hint1": "She has the most captivating smile in the entire stadium... and my world!",
        "hint2": "The answer is the amazing person solving these riddles right now!",
        "success_message": "Of course, it was you, Divya! Always has been, always will be. ❤️"
    },
    {
        "id": 7,
        "question": "Complete this sentence from the bottom of my heart: 'You're my _________.' (One powerful word!)",
        "answer": "everything",
        "hint1": "It's a word that means the whole world, all that matters.",
        "hint2": "If I had to sum up your importance to me in a single word, this would be it.",
        "success_message": "You are. You truly are my everything. You've reached the final treasure!"
    }
]

# --- TREASURE CONTENT - FINAL DRAFT ---
TREASURE_CONTENT = {
    "title": f"🎉 You Did It, My Amazing {GIRLFRIEND_PET_NAME}! Happy Birthday! 🎉",
    "message": (
        f"My Dearest {GIRLFRIEND_PET_NAME},\n\n"
        "You've navigated every riddle, unlocked every secret and now you've reached the heart of this little adventure. Absolutely just like you've reached the very heart of me. "
        "This whole thing was just a playful way to try and show you a fraction of what you mean to me but words can barely scratch the surface.\n\n"
        "Every single day, I am in awe of you. I respect you more than words can say – for your incredible resilience when things get tough, for the way you always make time to listen, no matter how busy you are. I admire your **infectious smile that can brighten any room** and the incredible heart that warms all around you.\n\n"
        "You know, before you, I only wished I could be the person I am today. You’ve inspired me, supported me and believed in me, often more than I believed in myself. You’ve helped me grow into someone happier, stronger and more complete. You’ve shown me what true partnership and love really look like and for that I am eternally grateful.\n\n"
        "Please always remember - through thick and thin, through sunshine and storms, I will always be by your side. You can count on me for anything and everything. My commitment to you is as deep and unwavering as the stars.\n\n"
        "Happy Birthday, my love. This is just the beginning of celebrating you today.\n\n"
        "With all my love and admiration, always and forever!!\n\n"
        f"P.S. To my {GIRLFRIEND_PET_NAME}, my cutest, the most beautiful Cadbury!"
    ),
    "image_url": "https://i.pinimg.com/originals/0c/da/2f/0cda2f2d00fcdfb94e6efd7aeec005e0.gif",
    "video_url": None
}


# --- Custom CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Streamlit App ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

try:
    local_css("style.css")
except FileNotFoundError:
    st.warning("style.css not found. Custom styles will not be applied. Create a style.css file for better visuals.")

# --- Initialize Session State ---
if 'current_clue_index' not in st.session_state:
    st.session_state.current_clue_index = 0
if 'hunt_complete' not in st.session_state:
    st.session_state.hunt_complete = False
if 'show_intro' not in st.session_state:
    st.session_state.show_intro = True
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'hints_revealed' not in st.session_state:
    st.session_state.hints_revealed = {}
if 'show_next_button' not in st.session_state: # New state variable
    st.session_state.show_next_button = False
if 'last_success_message' not in st.session_state: # To store the success message
    st.session_state.last_success_message = ""


# --- Helper Functions ---
def check_answer(user_ans, correct_ans):
    if correct_ans == "*":
        return True
    return user_ans.strip().lower() == correct_ans.strip().lower()

# --- Intro Screen ---
if st.session_state.show_intro:
    st.session_state.show_next_button = False # Reset on intro
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title(f"🎂 Happpy Birthdaay 🎂My Cutie, my Beautiful!!")
        st.title(f" MY BABY!!!! ")
        st.markdown("### I've prepared a little digital scavenger hunt just for you! Meri Haseena ke liye < 3")
        st.markdown("Solve the riddles about our memories and your favorite things.")
        st.markdown("Har ek sahi jawaab aapko treasure ke aur kareeb laayega!")
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHdqYmoyaHdua2RpN3VvOWFvY2hpOTNwYTl0MTV2MzRmdWI1eWpjNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XfmB8R5Qgogj9e8RNl/giphy.gif")
        
        if st.button(f"💖 Let's Start this Adventure, {GIRLFRIEND_PET_NAME}! 💖", type="primary", use_container_width=True):
            st.session_state.show_intro = False
            st.rerun()

# --- Main Hunt Logic ---
elif not st.session_state.hunt_complete:
    current_index = st.session_state.current_clue_index
    clue_data = ALL_CLUES[current_index]

    if current_index not in st.session_state.hints_revealed:
        st.session_state.hints_revealed[current_index] = {"hint1": False, "hint2": False}

    # If we are showing the "Next Question" button, it means an answer was just correct
    if st.session_state.show_next_button:
        st.success(st.session_state.last_success_message)
        st.balloons()
        if st.session_state.current_clue_index < len(ALL_CLUES) -1 : # Not the last clue yet
             next_button_text = "➡️ On to the Next Riddle!"
        else: # This was the last clue before treasure
             next_button_text = "✨ Reveal My Treasure! ✨"

        if st.button(next_button_text, type="primary", use_container_width=True):
            st.session_state.current_clue_index += 1
            st.session_state.show_next_button = False # Reset for the next actual clue
            if st.session_state.current_clue_index >= len(ALL_CLUES):
                st.session_state.hunt_complete = True
            st.rerun()
    else: # Normal clue display and answer input
        st.header(f"Riddle #{clue_data['id']} of {len(ALL_CLUES)}")
        st.markdown(f"## {clue_data['question']}")
        st.markdown("---")

        with st.expander("Need a little help? (Click to expand hints)", expanded=False):
            if st.button("Reveal Hint 1", key=f"hint1_btn_{current_index}"):
                st.session_state.hints_revealed[current_index]["hint1"] = True
            if st.session_state.hints_revealed[current_index]["hint1"]:
                st.info(f"💡 **Hint 1:** {clue_data['hint1']}")
                if "hint2" in clue_data:
                    if st.button("Still Stuck? Reveal Hint 2", key=f"hint2_btn_{current_index}"):
                        st.session_state.hints_revealed[current_index]["hint2"] = True
            if "hint2" in clue_data and st.session_state.hints_revealed[current_index]["hint2"]:
                st.warning(f"🤔 **Hint 2:** {clue_data['hint2']}")

        user_answer = st.text_input(
            "Your Answer:",
            key=f"ans_input_{current_index}",
            placeholder="Type your answer here and press Enter or click Submit",
            label_visibility="collapsed"
        )

        col_submit, col_progress = st.columns([1, 3])
        with col_submit:
            if st.button("Submit Answer", key=f"submit_btn_{current_index}", type="primary", use_container_width=True):
                if user_answer:
                    if check_answer(user_answer, clue_data["answer"]):
                        st.session_state.user_answers[current_index] = user_answer
                        st.session_state.last_success_message = clue_data.get("success_message", "🎉 Correct! You're amazing!")
                        st.session_state.show_next_button = True # Set to show next button
                        st.rerun() # Rerun to display the success message and next button
                    else:
                        st.error("Hmm, not quite! Take another guess. You can do it! 😉")
                        st.session_state.user_answers[current_index] = f"Attempt: {user_answer} (Incorrect)"
                else:
                    st.warning("Oops! Don't forget to type in your answer.")
        
        with col_progress:
            progress_emojis = ["□"] * len(ALL_CLUES)
            for i in range(current_index):
                progress_emojis[i] = "✅"
            if current_index < len(ALL_CLUES):
                progress_emojis[current_index] = "➡️"
            st.markdown(f"**Progress:** {' '.join(progress_emojis)}")

# --- Treasure Screen ---
elif st.session_state.hunt_complete:
    st.session_state.show_next_button = False # Reset just in case
    st.title(TREASURE_CONTENT["title"])
    st.balloons()
    st.balloons()

    if TREASURE_CONTENT.get("image_url"):
        st.image(TREASURE_CONTENT["image_url"], caption=f"You're a superstar, {GIRLFRIEND_PET_NAME}! ✨")

    st.markdown(TREASURE_CONTENT["message"])

    if TREASURE_CONTENT.get("video_url"):
        st.video(TREASURE_CONTENT["video_url"])
        st.caption(f"A special message just for you, {GIRLFRIEND_PET_NAME}!")
    
    st.markdown("---")
    st.subheader(f"Thank you for playing, my wonderful {GIRLFRIEND_PET_NAME}!")

    if st.button("Want to see your brilliant journey again?"):
        st.session_state.current_clue_index = 0
        st.session_state.hunt_complete = False
        st.session_state.show_intro = True
        st.session_state.user_answers = {}
        st.session_state.hints_revealed = {}
        st.session_state.show_next_button = False # Ensure reset
        st.rerun()

    with st.expander("Review Your Path to Victory!"):
        for i, clue_item in enumerate(ALL_CLUES):
            ans_record = st.session_state.user_answers.get(i, "Not attempted or last attempt incorrect")
            st.markdown(f"**Riddle {clue_item['id']}:** {clue_item['question']}")
            st.markdown(f"   *Correct Answer:* `{clue_item['answer']}`")