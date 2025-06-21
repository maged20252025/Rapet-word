
import streamlit as st
import fitz  # PyMuPDF
import os
import openai
from typing import List

st.set_page_config(page_title="استخراج القواعد القضائية من الأحكام", layout="centered")
st.title("📘 استخراج القواعد القضائية من الأحكام العليا")
st.markdown("""
قم برفع مجموعة من الأحكام بصيغة PDF، وسيقوم النظام بتحليل كل حكم واستخلاص الإشكاليات، ورد المحكمة العليا، والقواعد القضائية.
""")

uploaded_files = st.file_uploader("📂 اختر ملفات الأحكام (PDF)", type="pdf", accept_multiple_files=True)

def extract_text_from_pdf(file) -> str:
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = "\n".join([page.get_text() for page in doc])
    return text

def ask_gpt_to_extract_rule(text: str) -> str:
    prompt = f"""
أنت مساعد قانوني ذكي. إليك نص حكم صادر عن المحكمة العليا. استخرج منه باختصار:
1- الإشكالية القانونية أو الموضوعية التي أُثيرت.
2- رد المحكمة العليا عليها.
3- القاعدة القضائية التي استُخلصت.

النص:
{text}

الإخراج المطلوب:
الإشكالية: ...\nرد المحكمة: ...\nالقاعدة القضائية: ...
"""

    try:
        from langchain.llms import OpenAI
        llm = OpenAI(temperature=0)
        return llm.predict(prompt)
    except Exception:
        return "⚠️ يتطلب هذا التحليل اتصالًا فعّالًا بنموذج GPT. تأكد من توفر واجهة برمجية أو استخدم إصدار محلي من GPT."

if uploaded_files:
    st.info("جاري تحليل الملفات، الرجاء الانتظار...")
    for file in uploaded_files:
        st.subheader(f"📄 الحكم: {file.name}")
        try:
            text = extract_text_from_pdf(file)
            if len(text.strip()) < 100:
                st.warning("❌ الملف لا يحتوي على نص واضح أو أنه مسح ضوئي فقط.")
                continue
            with st.spinner("🤖 جاري استخراج القاعدة القضائية..."):
                result = ask_gpt_to_extract_rule(text[:3000])  # تحليل أول 3000 حرف فقط لتجنب الأخطاء
                st.text_area("🔍 النتيجة:", value=result, height=200)
        except Exception as e:
            st.error(f"حدث خطأ أثناء تحليل الملف: {e}")
