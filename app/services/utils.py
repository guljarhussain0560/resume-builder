import os
import ast
import uuid
import zipfile
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from app.config import GOOGLE_API_KEY

from app.prompts import prompts

# setup
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
TEMP_DIR = os.path.join(os.path.dirname(__file__), '..', 'temp')
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# LangChain setup
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)



# for generating enhance project description
def enhance_project_description_with_gemini(description: str) -> list[str]:
    messages = prompts.project_description_prompt.format_messages(description=description)
    response = llm(messages)

    # Remove markdown formatting (like ```json and ```)
    content = response.content.strip().strip("```json").strip("```").strip()

    try:
        return ast.literal_eval(content)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {e}\nRaw content: {response.content}")
    
# for generating enhance project description
def enhance_Work_experience_with_gemini(description: str) -> list[str]:
    messages = prompts.work_experience_prompt.format_messages(experience=description)
    response = llm(messages)

    # Remove markdown formatting (like ```json and ```)
    content = response.content.strip().strip("```json").strip("```").strip()

    try:
        return ast.literal_eval(content)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {e}\nRaw content: {response.content}")


def get_template_list() -> list:
    return [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html.j2")]

def render_resume_html(data: dict, template_file: str) -> str:
    template = env.get_template(template_file)
    return template.render(data)

def html_to_pdf(html_content: str, filename: str) -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)
    output_path = os.path.join(TEMP_DIR, filename)
    HTML(string=html_content).write_pdf(output_path)
    return output_path

def generate_all_templates_and_zip(data: dict) -> str:
    template_files = get_template_list()
    pdf_paths = []

    for template_file in template_files:
        try:
            html = render_resume_html(data, template_file)
            pdf_name = template_file.replace(".html.j2", ".pdf")
            pdf_path = html_to_pdf(html, pdf_name)
            pdf_paths.append(pdf_path)
        except Exception as e:
            print(f"⚠️ Failed for {template_file}: {e}")

    zip_path = os.path.join(TEMP_DIR, f"resumes_{uuid.uuid4().hex}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for pdf in pdf_paths:
            zipf.write(pdf, arcname=os.path.basename(pdf))

    return zip_path

# generation resume based on user selected template
def generate_resume_from_template(data: dict) -> str:
    template_name = data.get("template_name")
    if not template_name or not template_name.endswith(".html.j2"):
        raise ValueError("'template_name' must be provided and end with '.html.j2'")
    html = render_resume_html(data, template_name)
    pdf_name = f"{uuid.uuid4().hex}.pdf"
    pdf_path = html_to_pdf(html, pdf_name)
    return pdf_path
