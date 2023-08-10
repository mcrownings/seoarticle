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

def generate_content(prompt, previous_content="", language="English", keywords=""):

    prompt_with_keywords = f"You should speak with a confident, knowledgeable, neutral and clear tone of voice. These keywords are CRUCIAL and EXTREMELY IMPORTANT: {keywords}. It's ESSENTIAL to use them appropriately and prominently in the generated content. DO NOT overlook them. \n\n{prompt}."

    system_prompt_content = """You will be provided with a list of very important keywords, a topic and target audience, and your task is to generate an SEO-Optimized article. 
        Provide real brand names instead of placeholders. For example, instead of saying "Brand 1" write "DoorDash."
        Include a table of contents, FAQ with answers. 
        Use Markdown language.
        Speak with a confident, knowledgeable, neutral and clear tone of voice."""

    if language == "English":
        system_message = {"role": "system", "content": system_prompt_content}
    else:
        system_message = {"role": "system", "content": "Skriv allt på svenska. Du är en kunnig SEO-skribent. Skapa detaljerat, engagerande och SEO-optimerat innehåll. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv aldrig slutsatser."}
    
    user_message = {"role": "user", "content": prompt_with_keywords}
    
    messages = [system_message]
    if previous_content:
        messages.append({"role": "user", "content": previous_content})
    messages.append(user_message)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    return response.choices[0].message['content'].strip()

def generate_h2_content(topic, audience, keywords, h2_header):
    h2_prompt = f"Craft short, engaging and SEO-optimized content on the '{h2_header}', and relevant to the topic of '{topic}', while effectively capturing the attention of the '{audience}'. Keeping in mind these keywords: '{keywords}.'"
    return generate_content(h2_prompt, keywords=keywords)

def main():
    st.title('Content Generator')
    st.sidebar.text(f"App Version: {APP_VERSION}")

    topic = st.text_input("Enter the Topic:", key="topic_input")
    audience = st.text_input("Enter the Target Audience:", key="audience_input")
    keywords = st.text_input("Enter a list of keywords separated with comma:", key="keywords_input")
    language = st.selectbox("Choose a language:", ["English", "Swedish"], key="language_selectbox")

    #prompt = f"Write an article on '{topic}' while effectively capturing the attention of the '{audience}'. The article needs to be optimized for the keywords '{keywords}' and You SHOULD speak with a confident, knowledgeable, neutral and clear tone of voice. Include a table of contents, using Markdown language, The aim is to create valuable content that engages readers and satisfies SEO-needs."
    
    prompt = f"""
    Keywords: {keywords}
    Topic: {topic}
    Target audience: {audience}
    Here are some examples of real brand names for dog food:
    Purina
    Royal Canin
    """

    num_h2_sections = st.sidebar.slider("How many headlines would you like to add?", MIN_HEADLINES, MAX_HEADLINES, 1, key="h2_slider")
    h2_headers_inputs = [st.text_input(f"Enter H2 header #{i+1}:", key=f"h2_input_{i}") for i in range(num_h2_sections)]

    accumulated_content = ""
    if st.button("Generate Content", key="generate_button"):    
        with st.spinner('Generating content...'):
            # Main article content
            article_content = generate_content(prompt, keywords=keywords)
            accumulated_content += f"{article_content}\n"
            st.write(accumulated_content)
        
        # H2 sections
            for h2_header in h2_headers_inputs:
                if h2_header:
                    h2_content = generate_h2_content(topic, audience, keywords, h2_header)
                    accumulated_content += f"\n\n### {h2_header}\n\n{h2_content}"
                    st.write(f"### {h2_header}\n\n{h2_content}")

            # Display counts
            word_count, char_count = compute_counts(accumulated_content)
            st.sidebar.text(f"Total Word Count: {word_count}")
            st.sidebar.text(f"Total Character Count: {char_count}")

    display_versions()

if __name__ == "__main__":
    main()