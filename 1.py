import openai
from dotenv import load_dotenv
import streamlit as st
import os
import time
from ratelimiter import RateLimiter
import time
import base64
import markdown

#load_dotenv()
#openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Added app version
APP_VERSION = "1.0.1"

language = st.selectbox("Choose a language:", ["English", "Swedish"])

# Predefined prompts for each section
# title_prompt = "Write a comprehensive, SEO-optimized article '{title}', providing a detailed overview. Never write a summary or conclusion. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Don't write a conclusion. -conclusion"
# h2_prompt = "Write a short SEO-optimized paragraph about '{h2_header}'. Never write a summary or conclusion. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
# summary_table_prompt = "Based on the provided content, create a concise summary table highlighting key points, make sure it's a table. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
# introduction_prompt = "Write a short, personal and engaging introduction to the content provided here. Avoid duplicated content. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Never write a conclusion."
# conclusion_prompt = "Conclude the article, summarizing the main insights about the topic but never include the words conclusion or summarize in the first sentence. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
# faq_prompt = "Generate frequently asked questions related to the content with answers. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."

if language == "English":
    title_prompt = "Write a comprehensive, SEO-optimized article '{title}', providing a detailed overview. Never write a summary or conclusion. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Don't write a conclusion. -conclusion"
    h2_prompt = "Write a short SEO-optimized paragraph about '{h2_header}'. Never write a summary or conclusion. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
    summary_table_prompt = "Based on the provided content, create a concise summary table highlighting key points, make sure it's a table. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
    introduction_prompt = "Write a short, personal and engaging introduction to the content provided here. Avoid duplicated content. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Never write a conclusion."
    conclusion_prompt = "Conclude the article, summarizing the main insights about the topic but never include the words conclusion or summarize in the first sentence. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
    faq_prompt = "Generate frequently asked questions related to the content with answers. Ensure all content is in first person singular (I, me, my, mine), concise, and avoid unnecessary adjectives, overall, nutshell, conclusion and wording. You should speak with a confident, knowledgeable, neutral and clear tone of voice."
elif language == "Swedish":
    title_prompt = "Skriv en heltäckande, SEO-optimerad artikel '{title}', som ger en detaljerad översikt. Skriv aldrig en sammanfattning eller slutsats. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv inte en slutsats. -slutsats"
    h2_prompt = "Skriv ett kort, SEO-optimerat stycke om '{h2_header}'. Skriv aldrig en sammanfattning eller slutsats. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."
    summary_table_prompt = "Baserat på det tillhandahållna innehållet, skapa en koncis sammanfattningstabell som belyser viktiga punkter, se till att det är en tabell. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."
    introduction_prompt = "Skriv en kort, personlig och engagerande introduktion till det innehåll som tillhandahålls här. Undvik duplicerat innehåll. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv aldrig en slutsats."
    conclusion_prompt = "Avsluta artikeln genom att sammanfatta de viktigaste insikterna om ämnet, men inkludera aldrig orden slutsats eller sammanfatta i den första meningen. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."
    faq_prompt = "Generera vanligt förekommande frågor relaterade till innehållet med svar. Se till att allt innehåll är i första person singular (jag, mig, min, mitt), koncist, och undvik onödiga adjektiv, övergripande, i ett nötskal, slutsats och formuleringar. Du bör tala med en självsäker, kunnig, neutral och klar ton."


def generate_content(prompt, previous_content="", language="English"):
    # Set the system message based on the chosen language
    if language == "English":
        system_message = {"role": "system", "content": "You are a knowledgeable writer. Craft detailed, engaging, and SEO-optimized content. You should speak with a confident, knowledgeable, neutral and clear tone of voice. Never write conclusions."}
    elif language == "Swedish":
        system_message = {"role": "system", "content": "Skriv allt på svenska. Du är en kunnig skribent. Skapa detaljerat, engagerande och SEO-optimerat innehåll. Du bör tala med en självsäker, kunnig, neutral och klar ton. Skriv aldrig slutsatser."}
    
    user_message = {"role": "user", "content": prompt}
    
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

    accumulated_content = ""

    # 1. User provides a title.
    title = st.text_input("Enter a title:")
    if title:
        # Generate content for the title using predefined prompt
        prompt = title_prompt.format(title=title)
        title_content = generate_content(prompt)
        st.write(f"## {title}\n\n{title_content}")
        accumulated_content += f"## {title}\n\n{title_content}"

        # 2. User provides an H2 header.
        h2_header = st.text_input("Enter an H2 header:")
        if h2_header:
            # Generate content for H2 header using predefined prompt
            prompt = h2_prompt.format(h2_header=h2_header)
            h2_content = generate_content(prompt, accumulated_content)
            st.write(f"### {h2_header}\n\n{h2_content}")
            accumulated_content += f"\n\n### {h2_header}\n\n{h2_content}"

            # 3. Generate a summary table for the content using predefined prompt.
            summary_table = generate_content(summary_table_prompt, accumulated_content)
            st.write(summary_table)
            accumulated_content += "\n\n" + summary_table

            # 4. Generate an introduction section using predefined prompt.
            introduction = generate_content(introduction_prompt, accumulated_content)
            st.write(f"## Introduction\n\n{introduction}")
            accumulated_content += "\n\n" + introduction

            # 5. Generate a conclusion section using predefined prompt.
            conclusion = generate_content(conclusion_prompt, accumulated_content)
            st.write(f"## Conclusion\n\n{conclusion}")
            accumulated_content += "\n\n" + conclusion

            # 6. Generate FAQ section using predefined prompt.
            faq = generate_content(faq_prompt, accumulated_content)
            st.write(f"## Frequently Asked Questions\n\n{faq}")
            accumulated_content += "\n\n" + faq

            html_content = markdown.markdown(accumulated_content)

            # Now, save the accumulated_content to an HTML file
            with open("output_article.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            # Then, generate a download link for the HTML file and display it in Streamlit

            def get_html_download_link(html_string, filename):
                """
                Generate a link to download the HTML string as an html file.
                """
                b64 = base64.b64encode(html_string.encode()).decode()
                return f'<strong><a href="data:text/html;base64,{b64}" download="{filename}">Download file</a></strong>'

            download_link = get_html_download_link(html_content, "output_article.html")
            st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()