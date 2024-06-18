from docx import Document
from langchain_community.llms import Ollama
import json

def read_config():
    with open("config.json") as file:
        config = json.load(file)
        return config

def read_docfile(file):
    document = Document(file)
    return document

def translate_text(text, system, model):
    llm = Ollama(
        model=model,
        system=system
    )
    translated_text = str(llm.invoke(f"'{text}'"))
    return translated_text

if __name__ == '__main__':
    config = read_config()
    document = read_docfile(
        file = config["input_file"]
    )
    blacklist = config["blacklist"]

    for p in document.paragraphs:
        if len(p.text) > 0 and not (any(item in p.text for item in blacklist)):
            text = translate_text(
                text=p.text,
                model = config["model"],
                system=config["custom_system"]
            )
            p.text = str(text)[1:-1]
    document.save(f"{config['output_file']}.docx")