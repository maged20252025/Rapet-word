import streamlit as st
from docx import Document
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="تحليل موضوع الحكم", layout="centered")
st.title("⚖️ استخراج موضوع الحكم من الملفات")

uploaded_files = st.file_uploader("📤 ارفع ملفات Word أو PDF", type=["docx", "pdf"], accept_multiple_files=True)

# كلمات مفتاحية مرتبة حسب الموضوع
keywords_map = {
    "أتعاب محاماة": ["محامي", "أتعاب", "توكيل", "ترافع", "دعوى أتعاب"],
    "إيجارات": ["عقد إيجار", "مؤجر", "مستأجر", "أجرة", "إخلاء"],
    "حضانة": ["حضانة", "أطفال", "الولاية", "الأم", "الأب", "سن الحضانة"],
    "شراكة": ["شركة", "شراكة", "شريك", "تصفية", "حصة", "أسهم"],
    "تعويض": ["تعويض", "ضرر", "إصابة", "حادث", "مسؤولية"],
    "ملكية": ["ملكية", "حيازة", "عقار", "أرض", "نزع", "تمكين"],
    "إدارية": ["موظف", "قرار إداري", "خدمة مدنية", "تعيين", "عزل", "ترقية"],
    "تجارية": ["فاتورة", "توريد", "مقاولة", "عقد تجاري", "مطالبة مالية"]
}

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def detect_topic(text):
    scores = {topic: 0 for topic in keywords_map}
    for topic, keywords in keywords_map.items():
        for kw in keywords:
            scores[topic] += len(re.findall(re.escape(kw), text))
    top_topic = max(scores, key=scores.get)
    return top_topic if scores[top_topic] > 0 else "غير محدد"

if uploaded_files:
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        if filename.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        elif filename.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        else:
            st.warning(f"📄 الملف {filename} غير مدعوم.")
            continue

        topic = detect_topic(text)
        st.markdown(f"---\n📄 **الملف:** `{filename}`\n🏷️ **موضوع الحكم:** **{topic}**")
