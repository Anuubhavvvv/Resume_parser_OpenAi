import streamlit as st
import pandas as pd
import openai_helper
from openai import OpenAI
from JD_Resume import Calculate_score

############################
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

score =0
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "jd" not in st.session_state:
    st.session_state.jd = ""

resume_data = pd.DataFrame({
    "Entities": ["Name", "email_id", "mob_number", "qualification", "experience", "skills", "certification",
                 "achievement"],
    "value": ["", "", "", "", "", "", "", ""]
})

st.title("HR Assistant")

# Resume Uploading
uploaded_file = st.file_uploader("upload a file", type=["pdf", "docx", "png", "jpg", "jpeg"])
if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        st.session_state.resume_text = openai_helper.extract_from_pdf(uploaded_file)

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        st.session_state.resume_text = openai_helper.extract_from_doc(uploaded_file)

    elif file_type.startswith("image"):
        st.session_state.resume_text = openai_helper.extract_from_image(uploaded_file)

    else:
        st.error("Unsupported file.please upload a Pdf,Docx,or Image file .")

# JD comparison
st.write("")
st.title("Compare your resume with Job description")
job_description = st.text_area("enter the job description here:")
st.session_state.jd = job_description

if st.button("Check Similarity"):
    score = Calculate_score(st.session_state.jd, st.session_state.resume_text)
    st.write(f"Similarity Score:{score}")
    if score:
        st.progress(score / 100.0)
    if score < 50:
        st.write("Less Similar to the Given Job description ")
    elif 50 <= score < 70:
        st.write("Similar to The given Job description, May Consider")
    else:
        st.write("Excellent! You can consider the CV")


st.write("")
st.write("")
st.markdown("***")
st.write("")
st.write("")

# Resume Extractor
st.title("Resume Extractor ")

if st.button("Extract"):
    resume_data = openai_helper.extract_resume_data(client, st.session_state.resume_text)

st.dataframe(resume_data,
             column_config={
                 "Entities": st.column_config.Column(width=150),
                 "value": st.column_config.Column(width=450)

             },
             hide_index=True)

####################################
