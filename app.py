import os
import streamlit as st
from backend.opportunity import BusinessProfile, OpportunityEngine

# 1. تحديد المسار الرئيسي
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 2. تحميل الـ CSS بأمان
def load_css():
    css_path = os.path.join(PROJECT_ROOT, "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception:
            pass

# 3. إعداد الواجهة
st.set_page_config(page_title="محلل الفرص - متجر رنة جرس", page_icon="🔔", layout="wide")
load_css()

st.title("🔔 نظام تحليل الفرص والتطوير - متجر رنة جرس")
st.caption("https://axssor.com/ | إكسسوارات موضة")

# 4. التحقق من مفتاح API بأمان
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.warning("⚠️ ملاحظة: لم يتم العثور على `OPENAI_API_KEY` في secrets. سيتم العمل بالنموذج المحلي التجريبي.")

# 5. تهيئة المحرك مع التخزين المؤقت
@st.cache_resource
def get_engine():
    return OpportunityEngine(api_key=api_key)

engine = get_engine()

# 6. عرض بيانات المتجر واستقبال المدخلات
with st.sidebar:
    st.header("📋بيانات النشاط التجارية")
    business_name = st.text_input("اسم المتجر", value="متجر رنة جرس")
    category = st.text_input("التصنيف", value="Fashion accessories store")
    phone = st.text_input("رقم الهاتف", value="055 484 0091")
    address = st.text_input("المنطقة", value="Saudi Arabia")

profile = BusinessProfile(
    name=business_name,
    category=category,
    phone=phone,
    address=address
)

if st.button("🚀 تشغيل تحليل الفرصة", type="primary"):
    with st.spinner("جاري تحليل الفرصة والتوصيات..."):
        result = engine.analyze_business(profile)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("النتيجة (Score)", f"{result.score}%")
        col2.metric("المرحلة الحالية", result.phase)
        col3.metric("مستوى الثقة", f"{int(result.confidence * 100)}%")
        
        st.subheader("💡 التوصيات المقترحة:")
        for rec in result.recommendations:
            st.write(f"- {rec}")
            
        st.subheader("📝 التفسير:")
        st.info(result.explanation)
