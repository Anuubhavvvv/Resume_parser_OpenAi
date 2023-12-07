import streamlit as st
import pandas as pd
import openai_helper
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

resume_data = pd.DataFrame({
    "Entities": ["Name", "email_id", "mob_number", "qualification", "experience", "skills", "certification",
                "achievement"],
    "value": ["", "", "", "", "", "", "", ""]
})

st.title("Resume Extractor App")
uploaded_file = st.file_uploader("upload a file", type=["pdf", "docx", "png", "jpg", "jpeg"])
if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        text = openai_helper.extract_from_pdf(uploaded_file)

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = openai_helper.extract_from_doc(uploaded_file)

    elif file_type.startswith("image"):
        text = openai_helper.extract_from_image(uploaded_file)

    else:
        st.error("Unsupported file.please upload a Pdf,Docx,or Image file .")

if st.button("Extract"):
    resume_data = openai_helper.extract_resume_data(text)

st.dataframe(resume_data,
             column_config={
                 "Entities": st.column_config.Column(width=150),
                 "value": st.column_config.Column(width=450)

             },
             hide_index=True)
