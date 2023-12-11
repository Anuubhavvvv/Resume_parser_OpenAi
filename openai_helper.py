import json
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

import JD_Resume


def extract_resume_data(client,text):
    prompt = get_prompt() + text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": prompt
             }
        ]
    )
    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["measure", "value"])
    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Entities": ["Name", "email_id", "mob_number", "qualification", "experience", "skills", "certification",
                     "achievement"],
        "value": ["", "", "", "", "", "", "", ""]

    })


def get_prompt():
    return '''Please retrieve Name,email_id,mob_number,qualification,experience,skills,certification,achievement from 
    the following resume article. If you can't find the information from this article then return "". if there is no 
    experience return "Fresher",if there is not skills,certification,achievements return "NIL". Do not make things 
    up. Always return your response as a valid JSON string. The format of that string should be this,
    
    {
              "Name":"Abuthalib",
              "email_id":"abuthalib@gamil.com,
              "mob_number":"8138032213",
              "qualification":"Bachelor of computer Application",
              "experience" : "Fresher", 
              "skills" : "python,datascience,machinelearning,nlp",
              "certification" :"IBM Data Analyst with python,
              "achievement": "NIL"
           }
           News Article:
           ============
           

           '''


# Document extraction

def extract_from_pdf(file):
    pdf_text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text


def extract_from_doc(file):
    doc = Document(file)
    doc_text = ""
    for paragraph in doc.paragraphs:
        doc_text += paragraph.text + "\n"
    return doc_text


def extract_from_image(file):
    img = Image.open(file)
    ocr_text = pytesseract.image_to_string(img)
    return ocr_text


if __name__ == '__main__':
    text = " "
    df = extract_resume_data(text)
    print(df.to_string())

