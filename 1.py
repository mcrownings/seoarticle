import streamlit as st
import openai
import base64
import markdown

openai.api_key = st.secrets["OPENAI_API_KEY"]

VERSIONS = {
    "1.0.6": "Added important keywords."
}
APP_VERSION = "1.0.6"

def display_versions():
    st.sidebar.title("Version Changes")
    for version, description in VERSIONS.items():
        st.sidebar.text(f"Version {version}:")
        st.sidebar.text(description)

def compute_counts(text):
    word_count = len(text.split())
    char_count = len(text)
    return word_count, char_count

language = st.selectbox("Choose a language:", ["English", "Swedish"])

if language == "English":
    title_prompt = "Craft a detailed SEO-optimized article on the topic '{title}', ensuring the content is presented in the first person singular (I, me, my, mine). The narrative should be concise, devoid of extraneous adjectives, and phrases such as 'overall', 'nutshell', and 'conclusion'. Maintain a confident, informed, neutral, and lucid tone throughout. Refrain from adding any concluding remarks."
    h2_prompt = "Compose an SEO-enhanced paragraph centered on the topic '{h2_header}'. The content should strictly be in the first person singular (I, me, my, mine) and be concise. Exclude superfluous adjectives and avoid phrases like 'overall', 'nutshell', and 'conclusion'. The narrative tone should exude confidence, expertise, neutrality, and clarity."
    summary_table_prompt = "Using the given data, craft a Markdown table that includes a minimum of two columns and an appropriate number of rows. Refrain from using extraneous adjectives and phrases such as 'overall', 'nutshell', and 'conclusion'. The narrative should convey confidence, expertise, neutrality, and clarity."
    introduction_prompt = "Write a short introduction paragraph for the content above, start with a question, and focus on the benefit. Avoid duplicated content. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Never write a conclusion."
    conclusion_prompt = "Summarize the provided content in 3 bullet points. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
    faq_prompt = "Generate an FAQ of 5 questions based on the above content. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
elif language == "Swedish":
    title_prompt = "Skriv en heltäckande, SEO-optimerad artikel om '{title}', som ger en detaljerad översikt. Skriv aldrig en sammanfattning eller slutsats. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv inte en slutsats. -slutsats"
    h2_prompt = "Skriv ett kort SEO-optimerat stycke om '{h2_header}'. Skriv aldrig en sammanfattning eller slutsats. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."
    summary_table_prompt = "Baserat på innehållet, skapa en Markdown-tabell med minst två kolumner och ett lämpligt antal poster. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."
    introduction_prompt = "Skriv ett kort inledande stycke för innehållet ovan, börja med en fråga och fokusera på fördelen. Undvik upprepat innehåll. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv aldrig en slutsats."
    conclusion_prompt = "Sammanfatta det innehållet i 3 punkter och en mening om hur du samlade informationen. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."
    faq_prompt = "Generera vanligt förekommande frågor relaterade till innehållet med svar. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."

def generate_content(prompt, previous_content="", language="English", keywords=""):

    initial_message = {
        "role": "user",
        "content": f"These keywords are important: {keywords}. Use where it seems appropriate."
    }

    if language == "English":
        system_message = {"role": "system", "content": "Craft detailed, engaging, and SEO-optimized content. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Never write conclusions."}
    elif language == "Swedish":
        system_message = {"role": "system", "content": "Skriv allt på svenska. Du är en kunnig skribent. Skapa detaljerat, engagerande och SEO-optimerat innehåll. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv aldrig slutsatser."}
    
    user_message = {"role": "user", "content": prompt}
    
    messages = [initial_message, system_message]
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

    title = st.text_input("Enter a title:")
    keywords = st.text_input("Enter a list of keywords separated with comma:")
    num_h2_sections = st.sidebar.slider("How many headlines would you like to add?", 1, 5, 1)
    h2_headers_inputs = [st.text_input(f"Enter H2 header #{i+1}:") for i in range(num_h2_sections)]

    if st.button("Generate Content"):
        accumulated_content = ""
        title_content = generate_content(title_prompt.format(title=title), keywords=keywords)
        accumulated_content += f"## {title}\n\n{title_content}"
        st.write(accumulated_content)

        for h2_header in h2_headers_inputs:
            if h2_header:
                h2_content = generate_content(h2_prompt.format(h2_header=h2_header), accumulated_content, keywords=keywords)
                accumulated_content += f"\n\n### {h2_header}\n\n{h2_content}"
                st.write(f"### {h2_header}\n\n{h2_content}")

        for prompt in [summary_table_prompt, introduction_prompt, conclusion_prompt, faq_prompt]:
            section_content = generate_content(prompt, accumulated_content)
            accumulated_content += "\n\n" + section_content
            st.write(section_content)

        word_count, char_count = compute_counts(accumulated_content)
        st.sidebar.text(f"Total Word Count: {word_count}")
        st.sidebar.text(f"Total Character Count: {char_count}")

        seo_prompt = "Please rewrite the following content as an SEO-specialist:\n" + accumulated_content
        seo_rewritten_content = generate_content(seo_prompt)
        st.write("### SEO-Optimized Content")
        st.write(seo_rewritten_content)

        html_content = markdown.markdown(seo_rewritten_content)
        with open("output_article_seo.html", "w", encoding="utf-8") as file:
            file.write(html_content)

        def get_html_download_link(html_string, filename):
            b64 = base64.b64encode(html_string.encode()).decode()
            return f'<strong><a href="data:text/html;base64,{b64}" download="{filename}">Download file</a></strong>'

        download_link = get_html_download_link(html_content, "output_article_seo.html")
        st.markdown(download_link, unsafe_allow_html=True)

    display_versions()

if __name__ == "__main__":
    main()