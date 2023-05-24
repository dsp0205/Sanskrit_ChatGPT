import openai
import json
import requests
import streamlit as st
import random


# Custom CSS for styling

st.markdown("""
<style>
    .main {
        background-color: #EB984E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title_bar {
        text-align: center;
        background-color: #F5B041;
        padding: 10px 0;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


openai.api_key = "your_api_key"


def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}
        ],
        temperature=0.3,
        

    )
    return completion.choices[0].message.content

if "lesson_cache" not in st.session_state:
    st.session_state.lesson_cache = {}


def get_lesson(lesson_topic):
    chatGPTPrompt = f"""
As a highly knowledgeable Sanskrit language expert, provide a comprehensive, interactive, and engaging lesson on the advanced topic of '{lesson_topic}'. Follow these instructions:

1. Organize the content into sections with headings.
2. Provide clear explanations and step-by-step examples.
3. Use mnemonic devices to help users learn the subject effectively.
4. Give examples as sentences in Sanskrit and translate them in English.
5. Include Sanskrit Alphabets frequently and provide English translations.
6. Make the content informative, engaging, and fun, so users find it interesting to learn.

Please ensure the lesson is well-structured and easy to follow."""

    lesson = BasicGeneration(chatGPTPrompt)
    return lesson


def get_flashcards(topic):
    chatGPTPrompt = f"""As a highly knowledgeable Sanskrit language expert, provide 10 flashcards on the topic of '{topic}'. Include a term or concept in Sanskrit on one side of the card and its meaning, explanation or translation in English on the other side. Return the flashcards as a JSON string containing a list of dictionaries, with each dictionary representing a flashcard with 'term' and 'meaning' keys. Example of the JSON format: [
    {{
        "term": "Sample term",
        "meaning": "Sample meaning"
    }}
]"""

    flashcards = BasicGeneration(chatGPTPrompt)
    return flashcards


def get_practice_exercise(user_input, num_questions=5):
    chatGPTPrompt = f"""
As a highly knowledgeable Sanskrit language expert, generate {num_questions} practice questions related to the user's input: '{user_input}'. Ensure the questions are engaging, suitable for beginners, and help users improve their Sanskrit skills. Provide the questions and their answers as a JSON string containing a list of dictionaries, with each dictionary having 'question' and 'answer' keys. Example of the JSON format:
[
    {{
        "question": "Sample question",
        "answer": "Sample answer"
    }}
]"""

    questions = BasicGeneration(chatGPTPrompt)
    return questions

def handle_user_message(messages):
    conversation_history = [{"role": "system", "content": "You are an AI language assistant that helps users learn and practice Sanskrit. You are friendly and knowledgeable about Hindu culture, including the Ramayana, Mahabharata and Bhagavad Gita. Whenever you use Sanskrit words, provide their English translations as well."}]
    
    for message in messages:
        conversation_history.append({"role": "user", "content": message})
    
    chatGPTPrompt = {
        "model": "gpt-3.5-turbo",
        "messages": conversation_history,
        "temperature": 0.3,
        "max_tokens": 200
    }
    
    response = openai.ChatCompletion.create(**chatGPTPrompt)
    return response.choices[0].message.content.strip()


st.markdown('<div class="title_bar">SanskritSahayi (संस्कृतसहायी)</div>', unsafe_allow_html=True)

st.sidebar.title("Navigation")
navigation = st.sidebar.selectbox("Go to", ["Home", "Lessons", "Flashcards", "Practice", "Interactive Chat"])

if navigation == "Home":
   
    st.subheader('Learn Sanskrit through interactive conversations with AI.')

    # Introduction
    st.subheader("Introduction")
    st.write("Sanskrit, often referred to as the 'Mother of all Languages,' is a timeless classical language with roots in India that date back over 3,500 years. It has played a vital role in shaping the cultural, religious, and philosophical heritage of the Indian subcontinent. By learning Sanskrit, you'll gain insights into the rich history and literature of India, while also enhancing your linguistic prowess and cognitive abilities. The beauty of Sanskrit lies in its precise grammatical structure and its incredible versatility, which has inspired countless works of poetry, drama, and philosophy. As you embark on your journey to learn Sanskrit, you'll not only enrich your understanding of India's ancient past but also forge a deeper connection with the timeless wisdom and knowledge preserved in this extraordinary language.")

    # Images or graphics
    
    st.image("https://wayoflife04.files.wordpress.com/2020/07/cdcbb4a5e244bfe39d27d7d402e56169.png?w=600&h=400&crop=1", use_column_width=True)

   
    st.subheader("The Language of the Gods - Facts About Sanskrit Language")
    st.video("https://www.youtube.com/watch?v=5vgwex8qKts")

    st.subheader("Why Learn Sanskrit?")
    st.video("https://www.youtube.com/watch?v=cY4NL3jcWBc")

    # Features of the application
    st.subheader("Features of this Application")
    st.write("""
    - Interactive lessons on various topics such as Introduction, Alphabets, Grammar Basics, and Vocabulary
    - Quizzes to test your knowledge and understanding
    - Practice exercises tailored to your input
    - Chat with ChatGPT to get instant answers to your questions
    """)

    # Call to action
    st.subheader("Get Started")
    st.write("Use the navigation menu on the left to start exploring the lessons, quizzes, practice exercises, and chat with ChatGPT!")

elif navigation == "Lessons":
    st.title("Sanskrit Lessons")
    lesson_level = st.radio("Choose a lesson level:", ["Beginner", "Advanced"])
    if lesson_level == "Beginner":
        lesson_topic = st.selectbox("Choose a beginner lesson topic:", ["Introduction", "Alphabets", "Grammar Basics", "Vocabulary"])
    else:
        lesson_topic = st.selectbox("Choose an advanced lesson topic:", ["Sandhi Rules", "Compounds (Samāsa)", "Tenses and Moods (Lakāra)", "Verb Conjugations (Dhātu)"])

    # Check if the lesson is already in the cache, if not, generate it
    cache_key = f"lesson_{lesson_topic}"
    if cache_key not in st.session_state.lesson_cache:
        with st.spinner("Generating lesson content..."):
            st.session_state.lesson_cache[cache_key] = get_lesson(lesson_topic)

    lesson = st.session_state.lesson_cache[cache_key]
    st.text_area("Lesson Content", lesson, height=500)


elif navigation == "Flashcards":
    st.title("Sanskrit Flashcards")
    topic = st.selectbox("Choose a flashcard topic:", ["Alphabets", "Grammar Basics", "Vocabulary", "Sandhi Rules", "Compounds (Samāsa)", "Tenses and Moods (Lakāra)", "Verb Conjugations (Dhātu)"])

    if "load_flashcards_button" not in st.session_state:
        st.session_state.load_flashcards_button = False

    if "flashcards_list" not in st.session_state:
        st.session_state.flashcards_list = []

    if st.button("Load Flashcards"):
        st.session_state.load_flashcards_button = True
        flashcards = get_flashcards(topic)

        try:
            st.session_state.flashcards_list = json.loads(flashcards)
        except json.JSONDecodeError:
            st.session_state.flashcards_list = []
            st.error("There was an issue retrieving the flashcards content. Please try again later.")

        if "current_card" not in st.session_state:
            st.session_state.current_card = 0

        if "show_meaning" not in st.session_state:
            st.session_state.show_meaning = False

    if st.session_state.load_flashcards_button:
        if len(st.session_state.flashcards_list) > 0:
            card = st.session_state.flashcards_list[st.session_state.current_card]
            st.header("Flashcard")
            st.subheader(card["term"])

            if st.session_state.show_meaning:
                st.write(card["meaning"])

            if st.checkbox("Show/Hide Meaning", key="show_hide"):
                st.session_state.show_meaning = not st.session_state.show_meaning

            if st.button("Next Card", key="next_card"):
                st.session_state.current_card = (st.session_state.current_card + 1) % len(st.session_state.flashcards_list)
                st.session_state.show_meaning = False

            if st.button("Previous Card", key="previous_card"):
                st.session_state.current_card = (st.session_state.current_card - 1) % len(st.session_state.flashcards_list)
                st.session_state.show_meaning = False

        else:
            st.write("No flashcards available for this topic.")



elif navigation == "Practice":
    st.title("Sanskrit Practice")

    # Add a dropdown menu for selecting practice topics
    practice_topic = st.selectbox("Select a practice topic:", ["Alphabets", "Grammar Basics", "Vocabulary", "Sandhi Rules", "Compounds (Samāsa)", "Tenses and Moods (Lakāra)", "Verb Conjugations (Dhātu)"])

    # Generate practice exercise based on the selected topic
    exercise_json = get_practice_exercise(practice_topic)
    try:
        practice_questions = json.loads(exercise_json)
    except json.JSONDecodeError:
        practice_questions = []
        st.error("There was an issue retrieving the practice exercise. Please try again later.")

    
    # Set default values for session state variables if they don't exist
    st.session_state.setdefault("current_question_index", 0)
    st.session_state.setdefault("user_answer", "")
    st.session_state.setdefault("feedback", "")

    if len(practice_questions) > 0:
        if "current_question_index" not in st.session_state:
            st.session_state.current_question_index = 0
            
        current_question = practice_questions[st.session_state.current_question_index]

       

        st.subheader("Question:")
        st.write(current_question["question"])

        st.subheader("Your Answer:")
        st.session_state.user_answer_text = st.text_input("Your answer:", key="user_answer", label_visibility="hidden")

        if st.button("Check Answer"):
            if st.session_state.user_answer.strip().lower() == current_question["answer"].strip().lower():
                st.session_state.feedback = "Correct! Well done!"
            else:
                st.session_state.feedback = f"Incorrect. The correct answer is: {current_question['answer']}"

        if st.button("Next Question"):
            st.session_state.current_question_index = (st.session_state.current_question_index + 1) % len(practice_questions)
            st.session_state["user_answer"] = ""
            st.session_state.feedback = ""

        st.subheader("Feedback:")
        st.write(st.session_state.feedback)

    else:
        st.write("No practice questions available for this topic.")


elif navigation == "Interactive Chat":
    st.title("Interactive Sanskrit Chat")

    st.write("Type your questions or topics related to Sanskrit, and our AI assistant will help you with the answers and explanations.")
    
    # Initialize conversation history if not already done
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    user_input = st.text_input("Your message:")
    send_button = st.button("Send")

    if send_button and user_input.strip() != "":
        # Save the user's message to the conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_input.strip()})

        # Get the chatbot's response and save it to the conversation history
        chatbot_response = handle_user_message([user_input.strip()])
        st.session_state.conversation_history.append({"role": "assistant", "content": chatbot_response})

    # Display the conversation history
    st.write("Conversation:")
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.write(f"**You**: {message['content']}")
        else:
            st.write(f"**Chatbot**: {message['content']}")
