import os
import uuid
import zipfile
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

TEMPLATE_DIR = "templates"
TEMP_DIR = "temp"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def get_template_list() -> list:
    """
    Dynamically get all .html.j2 templates from the templates/ folder.
    """
    return [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".html.j2")]

def render_resume_html(data: dict, template_file: str) -> str:
    """
    Render the Jinja2 template with the provided resume data.
    """
    template = env.get_template(template_file)
    return template.render(data)

def html_to_pdf(html_content: str, filename: str) -> str:
    """
    Convert HTML content to PDF and save it.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    output_path = os.path.join(TEMP_DIR, filename)
    HTML(string=html_content).write_pdf(output_path)
    return output_path

def generate_all_templates_and_zip(data: dict) -> str:
    """
    Generate a PDF for each template and return a ZIP file path.
    """
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

def generate_resume_from_template(data: dict) -> str:
    """
    Generate a single resume from the selected template.
    Expected key in `data`: template_name
    """
    template_name = data.get("template_name")

    if not template_name or not template_name.endswith(".html.j2"):
        raise ValueError("❌ 'template_name' must be provided and end with '.html.j2'")

    html = render_resume_html(data, template_name)
    pdf_name = f"{uuid.uuid4().hex}.pdf"
    pdf_path = html_to_pdf(html, pdf_name)
    return pdf_path

