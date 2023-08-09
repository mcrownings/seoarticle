import streamlit as st
import openai

VERSIONS = {
    "1.23": "New prompts"
}
APP_VERSION = "1.23"

def display_versions():
    st.sidebar.title("Version Changes")
    for version, description in VERSIONS.items():
        st.sidebar.text(f"Version {version}:")
        st.sidebar.text(description)

def compute_counts(text):
    return len(text.split()), len(text)

def generate_content(prompt, previous_content="", language="English", keywords=""):
    
    prompt_with_keywords = f"You should speak with a confident, knowledgeable, neutral and clear tone of voice.\n\n{prompt}."
    
    # Printing the prompt for debugging
    # st.write(f"Debug - Prompt sent to the model: {prompt_with_keywords}")

    if language == "English":
        system_message = {"role": "system", "content": "Craft detailed, engaging, and SEO-optimized content. Never write conclusions. ALWAYS PLEASE provide the most likely brand names based on your knowledge."}
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

def main():
    st.title('Content Generator')
    st.sidebar.text(f"App Version: {APP_VERSION}")

    topic = st.text_input("Enter the Topic:")
    audience = st.text_input("Enter the Target Audience:")
    keywords = st.text_input("Enter a list of keywords separated with comma:")
    language = st.selectbox("Choose a language:", ["English", "Swedish"])

    prompt = f"Write an article on '{topic}' while effectively capturing the attention of the '{audience}' audience. The article needs to be optimized for the keywords '{keywords}' and You SHOULD speak with a confident, knowledgeable, neutral and clear tone of voice. Include a table of contents, using Markdown language, and concluding with three relevant FAQs and answers. The aim is to create valuable content that engages readers and satisfies SEO needs. PLEASE, ALWAYS provide the most likely brand names based on your knowledge."

    num_h2_sections = st.sidebar.slider("How many headlines would you like to add?", 1, 5, 1)
    h2_headers_inputs = [st.text_input(f"Enter H2 header #{i+1}:") for i in range(num_h2_sections)]
    
    accumulated_content = ""
    if st.button("Generate Content"):
        
        # Main article content
        article_content = generate_content(prompt, keywords=keywords)
        #accumulated_content += f"## {topic}\n\n{article_content}\n"
        accumulated_content += f"{article_content}\n"
        st.write(accumulated_content)
        
        # H2 sections
        for h2_header in h2_headers_inputs:
            if h2_header:
                h2_prompt = f"Write a section on '{h2_header}' relevant to the topic of '{topic}' keeping in mind the keywords '{keywords}'"
                h2_content = generate_content(h2_prompt, accumulated_content, keywords=keywords)
                #accumulated_content += f"\n\n### {h2_header}\n\n{h2_content}"
                accumulated_content += f"{h2_content}\n"
                st.write(f"### {h2_header}\n\n{h2_content}")

        # Display counts
        word_count, char_count = compute_counts(accumulated_content)
        st.sidebar.text(f"Total Word Count: {word_count}")
        st.sidebar.text(f"Total Character Count: {char_count}")

    display_versions()

if __name__ == "__main__":
    main()