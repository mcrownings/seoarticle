import streamlit as st
import openai

# Constants
MAX_HEADLINES = 5
MIN_HEADLINES = 1

VERSIONS = {
    "1.24": "New UX"
}
APP_VERSION = "1.24"

def display_versions():
    st.sidebar.title("Version Changes")
    for version, description in VERSIONS.items():
        st.sidebar.text(f"Version {version}:")
        st.sidebar.text(description)

def compute_counts(text):
    return len(text.split()), len(text)

LANGUAGES = {
    "English": """You will be provided with a list of very important keywords, a topic and target audience, and your task is to generate an SEO-Optimized article. 
        Provide real brand names instead of placeholders. For example, instead of saying "Brand 1" write "DoorDash."
        Include a table of contents, FAQ with answers. 
        Use HTML-Markdown language.
        Speak with a confident, knowledgeable, neutral and clear tone of voice.""",
    "Swedish": """Du kommer att få en lista med mycket viktiga nyckelord, ett ämne och en målgrupp, och din uppgift är att skapa en SEO-optimerad artikel.
        Var noga med att ange riktiga varumärkesnamn istället för platshållare. Till exempel, istället för att säga "Varumärke 1", skriv "Apple."
        Inkludera en innehållsförteckning, FAQ med svar.
        Använd HTML-Markdown språk.
        Tala med ett självsäkert, kunnigt, neutralt och klart tonfall."""
}

def generate_content(prompt, previous_content="", language="English", keywords=""):
    
    prompt_with_keywords = f"You should speak with a confident, knowledgeable, neutral and clear tone of voice. These keywords are CRUCIAL and EXTREMELY IMPORTANT: {keywords}. It's ESSENTIAL to use them appropriately and prominently in the generated content. DO NOT overlook them. \n\n{prompt}."

    system_message = {"role": "system", "content": LANGUAGES.get(language, LANGUAGES["English"])}
    user_message = {"role": "user", "content": prompt_with_keywords}
    
    messages = [system_message]
    if previous_content:
        messages.append({"role": "user", "content": previous_content})
    messages.append(user_message)
    
    # Debug prints
    st.write(f"System Message: {system_message['content']}")
    st.write(f"User Message: {user_message['content']}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        # Handle the exception or return an error message
        return str(e)

def main():
    st.title('Content Generator')
    st.sidebar.text(f"App Version: {APP_VERSION}")

    topic = st.text_input("Enter the Topic:", key="topic_input")
    audience = st.text_input("Enter the Target Audience:", key="audience_input")
    keywords = st.text_input("Enter a list of keywords separated with comma:", key="keywords_input")
    language = st.selectbox("Choose a language:", ["English", "Swedish"], key="language_selectbox")
    
    prompt = f"""
    Keywords: {keywords}
    Topic: {topic}
    Target audience: {audience}
    Here are some examples of real brand names for dog food:
    Purina
    Royal Canin
    """

    accumulated_content = ""
    if st.button("Generate Content", key="generate_button"):    
        with st.spinner('Generating content...'):
            # Main article content
            article_content = generate_content(prompt, keywords=keywords)
            accumulated_content += f"{article_content}\n"
            st.write(accumulated_content)

            # Display counts
            word_count, char_count = compute_counts(accumulated_content)
            st.sidebar.text(f"Total Word Count: {word_count}")
            st.sidebar.text(f"Total Character Count: {char_count}")

    display_versions()

if __name__ == "__main__":
    main()