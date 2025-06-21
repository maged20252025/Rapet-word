import streamlit as st
from docx import Document
import re

st.title("تحديد موضوع الحكم من ملفات Word")

uploaded_files = st.file_uploader("ارفع ملفات Word (.docx)", type=["docx"], accept_multiple_files=True)

subject_keywords = {
    "تجارية": ["شركة", "شراكة", "فاتورة", "توريد", "عقد تجاري", "وكالة تجارية", "أتعاب", "مقاولة", "عمولة", "سعي", "سمسرة", "مبلغ مالي", "مطالبة مالية"],
    "مدنية": ["ملكية", "حيازة", "عقار", "دعوى صحة توقيع", "دعوى صحة ونفاذ", "دعوى تمكين", "دعوى إخلاء", "تسليم عقار"],
    "أحوال شخصية": ["حضانة", "نفقة", "طلاق", "رجعة", "عدة", "زواج", "نسب", "ولاية", "متعة", "مهر"],
    "إيجارات": ["عقد إيجار", "إخلاء", "مستأجر", "مؤجر", "أجرة", "مدة الإيجار"],
    "إدارية": ["موظف", "قرار إداري", "إلغاء قرار", "جهة إدارية", "خدمة مدنية", "ترقية", "عزل", "تعيين", "الوظيفة العامة"],
    "جنائية": ["قتل", "سرقة", "تزوير", "احتيال", "جريمة", "عقوبة", "حبس", "سجن", "قانون العقوبات"]
}

def extract_text(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def detect_subject(text):
    scores = {subject: 0 for subject in subject_keywords}
    for subject, keywords in subject_keywords.items():
        for kw in keywords:
            scores[subject] += len(re.findall(re.escape(kw), text))
    top = max(scores, key=scores.get)
    return top if scores[top] > 0 else "غير معروف"

if uploaded_files:
    for file in uploaded_files:
        text = extract_text(file)
        subject = detect_subject(text)
        st.write(f"📄 **{file.name}** → 🏷️ موضوع الحكم: **{subject}**")
