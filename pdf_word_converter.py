import streamlit as st
import os
from pdf2docx import Converter
from docx2pdf import convert
import tempfile

def pdf_to_word(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
        tmp_pdf.write(pdf_file.getvalue())
        pdf_path = tmp_pdf.name

    docx_path = pdf_path.replace('.pdf', '.docx')
    
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    with open(docx_path, 'rb') as docx_file:
        docx_bytes = docx_file.read()

    os.unlink(pdf_path)
    os.unlink(docx_path)

    return docx_bytes

def word_to_pdf(docx_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_docx:
        tmp_docx.write(docx_file.getvalue())
        docx_path = tmp_docx.name

    pdf_path = docx_path.replace('.docx', '.pdf')
    
    convert(docx_path, pdf_path)

    with open(pdf_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()

    os.unlink(docx_path)
    os.unlink(pdf_path)

    return pdf_bytes

st.title("PDF-Word Converter")

conversion_type = st.radio("Select conversion type:", ("PDF to Word", "Word to PDF"))

if conversion_type == "PDF to Word":
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        if st.button("Convert to Word"):
            docx_bytes = pdf_to_word(uploaded_file)
            st.download_button(
                label="Download Word Document",
                data=docx_bytes,
                file_name="converted_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

else:  # Word to PDF
    uploaded_file = st.file_uploader("Choose a Word file", type="docx")
    if uploaded_file is not None:
        if st.button("Convert to PDF"):
            pdf_bytes = word_to_pdf(uploaded_file)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="converted_document.pdf",
                mime="application/pdf"
            )