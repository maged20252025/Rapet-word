import streamlit as st from collections import Counter import docx import re from io import BytesIO from docx import Document

st.title("تحليل أكثر الكلمات تكرارًا في ملفات Word")

uploaded_files = st.file_uploader("ارفع ملفات Word (DOCX)", type=["docx"], accept_multiple_files=True)

قائمة الكلمات الشائعة وغير المهمة (Stop Words + كلمات قانونية عامة)

stop_words = { "من", "في", "على", "إلى", "عن", "أن", "إن", "لن", "لم", "قد", "هو", "هي", "هم", "ها", "كان", "كانت", "يكون", "تكون", "ما", "لا", "كل", "هذا", "هذه", "ذلك", "تلك", "أو", "أي", "إذ", "ثم", "بين", "بعد", "قبل", "مع", "حتى", "إذا", "وقد", "فقد", # كلمات قانونية عامة مكررة لا تدل على نوع القضية "القاضي", "محكمة", "محكمة", "المحكمة", "الدائرة", "القانون", "المادة", "مادة", "رقم", "رئيس", "رئيساً", "العدالة", "الشرعية", "المدعي", "المدعى", "المطعون", "الطاعن", "الحكم", "الحكمة", "قانون" }

if uploaded_files: all_results = [] for uploaded_file in uploaded_files: # قراءة الملف doc = docx.Document(uploaded_file) full_text = " ".join([para.text for para in doc.paragraphs])

# تنظيف النص
    cleaned_text = re.sub(r'[^؀-ۿ\s]', '', full_text)  # فقط الحروف العربية
    words = cleaned_text.split()

    # إزالة الكلمات غير المهمة
    filtered_words = [w for w in words if w not in stop_words]

    # حساب التكرار
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(3)

    st.write(f"**أكثر الكلمات تكرارًا في الملف {uploaded_file.name}:**")
    for word, count in top_words:
        st.write(f"- {word}: {count} مرة")

    # حفظ النتائج لتصديرها لاحقًا
    result_text = f"نتائج الملف: {uploaded_file.name}\n"
    for word, count in top_words:
        result_text += f"- {word}: {count} مرة\n"
    result_text += "\n"
    all_results.append(result_text)

# زر لتصدير النتائج
if st.button("تحميل النتائج في ملف Word"):
    export_doc = Document()
    export_doc.add_heading("نتائج تحليل الكلمات", level=1)
    for result in all_results:
        export_doc.add_paragraph(result)

    buffer = BytesIO()
    export_doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="اضغط هنا لتحميل النتائج",
        data=buffer,
        file_name="تحليل_الكلمات.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

