import streamlit as st
import openai

# Constants
MAX_HEADLINES = 5
MIN_HEADLINES = 1

VERSIONS = {
    "1.26": "Added Content Types"
}
APP_VERSION = "1.26"

def display_versions():
    st.sidebar.title("Version Changes")
    for version, description in VERSIONS.items():
        st.sidebar.text(f"Version {version}:")
        st.sidebar.text(description)

def compute_counts(text):
    return len(text.split()), len(text)

LANGUAGES = {
    "English": """I want you to always internal link at least once per article that you write. You are going to write for me, and when you write I want you to specifically respond in a way that is not considered robotic. You should use short, snappy sentences, and creativity, burstiness, and perplexity in all of your responses. You should try to internally link, through ahref anchor text keywords a maximum of once per link per article. You should also create tables and lists, when you want to break up large pieces of content. You are writing for SwedenMax.com, a Swedish tourist guide by a guy named Max, from Stockholm. These are my tours. When you mention one, you should write /stockholm/ and tour name, for example /stockholm/archipelago.

- Archipelago
- Hallwyl Museum
- Royal Palace
- Nationalmuseum
- Vasa Museum
- Moderna Museet
- Skansen
- Djurgården

Please write the first 3 headings of this article

Respond in markdown. Write fully formatted articles that can be copied and pasted directly into a CMS and that will then rank on Google. Give your opinion on topics, but make sure to remain fairly neutral. Give real life examples occasionally. Every few paragraphs respond with a list or a table.
""",
    "Swedish": """Du kommer att få en lista med mycket viktiga nyckelord, ett ämne och en målgrupp, och din uppgift är att skapa en SEO-optimerad artikel.
        Var noga med att ange riktiga varumärkesnamn istället för platshållare. Till exempel, istället för att säga "Varumärke 1", skriv "Apple."
        Inkludera en innehållsförteckning, FAQ med svar.
        Använd HTML-Markdown språk.
        Tala med ett självsäkert, kunnigt, neutralt och klart tonfall."""
}

def generate_content(prompt, previous_content="", language="Swedish", keywords=""):

    system_message = {"role": "system", "content": LANGUAGES.get(language, LANGUAGES["English"])}
    user_message = {"role": "user", "content": prompt}
    
    messages = [system_message]
    if previous_content:
        messages.append({"role": "user", "content": previous_content})
    messages.append(user_message)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message['content'].strip()
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
        topic = st.text_input("Enter the Topic:", key="topic_input")
        audience = st.text_input("Enter the Target Audience:", key="audience_input")
        prompt = f"""
        Keywords: {keywords}.\n
        Topic: {topic}.\n
        Target audience: {audience}.\n
        Here are some examples of real brand names for dog food:
        Purina,
        Royal Canin
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
    if st.button("Generate Content", key="generate_button"):    
        with st.spinner('Generating content...'):
            # Main article content
            article_content = generate_content(prompt, language=language, keywords=keywords)
            accumulated_content += f"{article_content}\n"
            st.write(accumulated_content)

            # Display counts
            word_count, char_count = compute_counts(accumulated_content)
            st.sidebar.text(f"Total Word Count: {word_count}")
            st.sidebar.text(f"Total Character Count: {char_count}")

    display_versions()

if __name__ == "__main__":
    main()