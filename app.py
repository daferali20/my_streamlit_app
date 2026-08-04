import streamlit as st
# استيراد المحرك الرئيسي أو النماذج من المجلد الخلفي
from backend.opportunity.opportunity_engine import OpportunityEngine
from backend.opportunity.models import OpportunityData

st.set_page_config(page_title="Opportunity Analysis", layout="wide")
st.title("🎯 نظام تحليل الفرص")

# تهيئة المحرك أو تحميل البيانات
@st.cache_resource  # لاستخدام التخزين المؤقت وتجنب إعادة تحميل المحرك عند كل ضغطة
def load_engine():
    return OpportunityEngine()

engine = load_engine()

# واجهة المستخدم لإدخال البيانات
st.sidebar.header("إعدادات الفرصة")
input_data = st.sidebar.text_input("ادخل البيانات:")

if st.button("تحليل الفرصة"):
    # استدعاء الوظائف الخلفية
    result = engine.analyze(input_data)
    
    # عرض النتائج في الواجهة
    st.write("### النتيجة:")
    st.json(result)
