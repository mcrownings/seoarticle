import streamlit as st
import openai

# Constants
MAX_HEADLINES = 5
MIN_HEADLINES = 1

VERSIONS = {
    "1.34": "Total översättning"
}
APP_VERSION = "1.34"

def display_versions():
    st.sidebar.title("Version Changes")
    for version, description in VERSIONS.items():
        st.sidebar.text(f"Version {version}:")
        st.sidebar.text(description)

def compute_counts(text):
    return len(text.split()), len(text)

LANGUAGES = {
    "English": """You are going to write for me, and when you write I want you to specifically respond in a way that is not considered robotic. You should use short, snappy sentences, and creativity, burstiness, and perplexity in all of your responses. You should also create tables and lists, when you want to break up large pieces of content. You will be provided with a topic to write about. You will be provided with a target audience, which your text should try to capture. You will be provided with a list of keyword, which should covered in your text.

Please write atleast three the first 3 headings of this article.

Respond in markdown. Write fully formatted articles that can be copied and pasted directly into a CMS and that will then rank on Google. Give your opinion on topics, but make sure to remain fairly neutral. Give real life examples occasionally. Every few paragraphs respond with a list or a table.

If you want write more, in the end of the text state ---- (Press continue) ----. When you are done writing state ---- (Done writing) ----.
""",
    "Swedish": """Du ska att skriva åt mig, och när du skriver vill jag att du svarar på ett sätt som inte uppfattas som robotiskt. Använd korta, kärnfulla meningar och visa på kreativitet, spontanitet och varierande innehåll i dina svar. Du bör också skapa tabeller och listor när du vill dela upp stora textblock. Du kommer att få ett ämne att skriva om. Du kommer också få en målgrupp som du ska försöka fånga med din text. Du kommer också få en lista med sökord som ska vara med i texten du skriver.

Skriv minst tre rubriker för denna artikel.

Svara i markdown. Skriv formaterade artiklar som kan kopieras och klistras in i ett CMS och som sedan ska ranka på Google. Ge din åsikt om ämnen, men se till att förbli relativt neutral. Ibland kan du ge verkliga exempel. Efter några textstycken, svara med en uträkning, lista eller en tabell.

Om du har mer att skriva, skriv ALLTID ---- (Tryck fortsätt!) ——. Om du har skrivit klart, skriv ALLTID ---- (Klar!) ——.
"""}

# Initialize session state (if not already done)
if "previous_response" not in st.session_state:
    st.session_state.previous_response = ""

def generate_content(prompt, language="Swedish", keywords=""):

    system_message = {"role": "system", "content": LANGUAGES.get(language, LANGUAGES["English"])}
    user_message = {"role": "user", "content": prompt}

    # Add previous response to the messages if exists
    messages = [{"role": "system", "content": st.session_state.previous_response}, system_message, user_message]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        st.session_state.previous_response = response.choices[0].message['content'].strip()  # Save the response
        return st.session_state.previous_response
    except Exception as e:
        return str(e)

def main():
    st.title('Content Generator')
    st.sidebar.text(f"App Version: {APP_VERSION}")

    # Dropdown for content type selection
    content_type = st.selectbox("Select Content Type:", ["Article", "Book Review", "Rewrite Content", "Product Review"])

    language = st.selectbox("Choose a language:", ["English", "Swedish"], key="language_selectbox")
    keywords = st.text_input("Enter a list of keywords separated with comma:", key="keywords_input")

    # Different prompts for each content type
    if content_type == "Article":
        topic = st.text_input("Enter the Topic:" if language != "Swedish" else "Ange ämnet:", key="topic_input")
        audience = st.text_input("Enter the Target Audience:" if language != "Swedish" else "Ange målgruppen:", key="audience_input")
        if language == "Swedish":
            prompt = f"""
            Skriv minst de tre första rubrikerna ämnet: {topic}.\n
            Målgrupp: {audience}.\n
            Sökord: {keywords}.\n
            Skriv ALL text på: {language}.
            """
        else:
            prompt = f"""
            Please write me the first part of an article about: {topic}.\n
            Target audience: {audience}.\n
            Keywords: {keywords}.\n
            Write everything in: {language}.
            """
    elif content_type == "Book Review":
        book_name = st.text_input("Enter Book Name:", key="book_name_input")
        author = st.text_input("Enter Author's Name:", key="author_input")
        prompt = f"Provide a review for the book '{book_name}' written by {author}. Keywords: {keywords}."
    elif content_type == "Rewrite Content":
        original_content = st.text_area("Enter the content to rewrite:", key="content_rewrite_input")
        prompt = f"Rewrite the following content while keeping the essence intact. Keywords: {keywords}.\n\n{original_content}"
    else: # Product Review
        product_name = st.text_input("Enter Product Name:", key="product_name_input")
        product_type = st.text_input("Enter Product Type:", key="product_type_input")
        prompt = f"Provide a review for the {product_type} named '{product_name}'. Keywords: {keywords}."

    accumulated_content = ""

    # Display the stored message (if any)
    if st.session_state.previous_response:
        accumulated_content = st.session_state.previous_response
        st.write(accumulated_content)
    
    if st.button("Generate Content", key="generate_button"):    
        with st.spinner('Generating content...'):
            # Main article content
            article_content = generate_content(prompt, language=language, keywords=keywords)
            accumulated_content = f"{accumulated_content}\n\n{article_content}"  # Append the new content
            st.session_state.previous_response = accumulated_content  # Update the session state
            st.write(article_content)

            # Display counts
            #word_count, char_count = compute_counts(accumulated_content)
            #st.sidebar.text(f"Total Word Count: {word_count}")
            #st.sidebar.text(f"Total Character Count: {char_count}")


    # Button to continue the conversation based on the previous response
    if st.session_state.previous_response and st.button("Continue Conversation", key="continue_button"):
        with st.spinner('Generating content...'):
            if language == "Swedish":
                continuation_prompt = "Fortsätt skriva från sista punkten."
            else:
                continuation_prompt = "Expand upon the last point."
            # Continue the conversation
            continuation_content = generate_content(continuation_prompt, language=language, keywords=keywords)
            accumulated_content = f"{accumulated_content}\n\n{continuation_content}"  # Append the continuation content
            st.session_state.previous_response = accumulated_content  # Update the session state
            st.write(continuation_content)
    
    if accumulated_content:
        word_count, char_count = compute_counts(accumulated_content)
        st.sidebar.text(f"Total Word Count: {word_count}")
        st.sidebar.text(f"Total Character Count: {char_count}")

    # Button to reset the session state
    if st.button("Reset Session", key="reset_button"):
        st.session_state.previous_response = ""
        st.experimental_rerun()

    display_versions()

if __name__ == "__main__":
    main()