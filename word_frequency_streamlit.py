import streamlit as st
import fitz  # PyMuPDF
import re
import json

st.title("تحديد موضوع الحكم من ملفات PDF")

uploaded_files = st.file_uploader("ارفع ملفات PDF", type=["pdf"], accept_multiple_files=True)

subject_keywords = json.loads("{\"تجارية\": [\"شركة\", \"شراكة\", \"فاتورة\", \"توريد\", \"عقد تجاري\", \"وكالة تجارية\", \"أتعاب\", \"مقاولة\", \"عمولة\", \"سعي\", \"سمسرة\", \"مبلغ مالي\", \"مطالبة مالية\"], \"مدنية\": [\"ملكية\", \"حيازة\", \"عقار\", \"دعوى صحة توقيع\", \"دعوى صحة ونفاذ\", \"دعوى تمكين\", \"دعوى إخلاء\", \"تسليم عقار\"], \"أحوال شخصية\": [\"حضانة\", \"نفقة\", \"طلاق\", \"رجعة\", \"عدة\", \"زواج\", \"نسب\", \"ولاية\", \"متعة\", \"مهر\"], \"إيجارات\": [\"عقد إيجار\", \"إخلاء\", \"مستأجر\", \"مؤجر\", \"أجرة\", \"مدة الإيجار\"], \"إدارية\": [\"موظف\", \"قرار إداري\", \"إلغاء قرار\", \"جهة إدارية\", \"خدمة مدنية\", \"ترقية\", \"عزل\", \"تعيين\", \"الوظيفة العامة\"], \"جنائية\": [\"قتل\", \"سرقة\", \"تزوير\", \"احتيال\", \"جريمة\", \"عقوبة\", \"حبس\", \"سجن\", \"قانون العقوبات\"]}")

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def detect_subject(text):
    scores = dict()
    for subject in subject_keywords:
        scores[subject] = 0
        for kw in subject_keywords[subject]:
            pattern = re.escape(kw)
            matches = re.findall(pattern, text)
            scores[subject] += len(matches)
    top_subject = max(scores, key=scores.get)
    if scores[top_subject] == 0:
        return "غير معروف"
    return top_subject

if uploaded_files:
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        subject = detect_subject(text)
        st.write(f"📄 {file.name} → 🏷️ موضوع الحكم: **{subject}**")
