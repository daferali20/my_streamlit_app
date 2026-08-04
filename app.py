import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="AI Breakout Scanner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. إدارة المسارات وتشييد الـ CSS بأمان
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def load_css():
    css_path = os.path.join(PROJECT_ROOT, "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception:
            pass

load_css()

# 3. الاستيراد الصحيح للمحرك والأنواع بدون تعديل sys.path
try:
    from backend.opportunity.opportunity_engine import OpportunityEngine
    from backend.opportunity.models import MarketPhase, OpportunityScoreLevel
except ImportError:
    # في حال كان مجلد backend هو الجذر مباشرة على خادمك
    from opportunity.opportunity_engine import OpportunityEngine
    from opportunity.models import MarketPhase, OpportunityScoreLevel

# 4. تهيئة المحرك
@st.cache_resource
def get_opportunity_engine():
    return OpportunityEngine()

engine = get_opportunity_engine()

# 5. الواجهة الجانبية (Sidebar) لتحديد المدخلات والمؤشرات
st.sidebar.title("🎛️ إعدادات التحليل")
symbol = st.sidebar.text_input("رمز السهم / الأداة المالية", value="AAPL").upper()

st.sidebar.subheader("📊 البيانات المباشرة / المؤشرات")
bollinger_width = st.sidebar.slider("عرض نطاق بولينجر (Bollinger Width)", 0.0, 1.0, 0.25)
atr_ratio = st.sidebar.slider("نسبة ATR (ATR Ratio)", 0.0, 1.0, 0.35)
volume_trend = st.sidebar.slider("اتجاه الحجم (Volume Trend)", 0.5, 5.0, 2.1)
rsi = st.sidebar.slider("مؤشر القوة النسبية (RSI)", 0, 100, 62)
pattern_score = st.sidebar.slider("جودة النموذج الفني (Pattern Score)", 0.0, 1.0, 0.8)
smart_money_flow = st.sidebar.slider("تدفق السيولة الذكية (Smart Money)", 0.0, 1.0, 0.7)

# تجميع البيانات للتمرير للمحرك
market_data = {
    'bollinger_width': bollinger_width,
    'atr_ratio': atr_ratio,
    'volume_trend': volume_trend,
    'volume_spike': volume_trend,
    'rsi': rsi,
    'pattern_score': pattern_score,
    'smart_money_flow': smart_money_flow,
    'trend_strength': 0.75,
    'volatility': 0.35,
    'market_regime': 0.8
}

# 6. شاشة العرض الرئيسية
st.title("🚀 نظام فحص وتنبؤ الاختراقات (AI Breakout Scanner)")
st.caption("تحليل مراحل السوق، المحفزات، واحتمالات الانتقال باستخدام الذكاء الاصطناعي")

if st.button("🔎 تشغيل التحليل الشامل", type="primary"):
    with st.spinner(f"جاري معالجة المؤشرات والمحفزات لـ {symbol}..."):
        # استدعاء دالة التحليل من opportunity_engine
        result = engine.analyze(symbol, market_data)

        st.success("تم إكمال التحليل بنجاح!")

        # عرض الكروت والعدادات الرئيسية
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("المرحلة الحالية", result.phase_metrics.phase.value)
        col2.metric("درجة الفرصة", f"{result.score:.1f}%", delta=result.score_level.value)
        col3.metric("مستوى الثقة", f"{result.phase_metrics.confidence:.1f}%")
        col4.metric(
            "المرحلة القادمة المتوقعة", 
            result.phase_metrics.next_phase.value if result.phase_metrics.next_phase else "N/A"
        )

        st.markdown("---")

        # تفاصيل المحفزات والأسباب
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("💡 أسباب وتقييم AI")
            for reason in result.reasons:
                st.write(f"- {reason}")

            st.subheader("⚠️ أخطار ومخاطر محتملة")
            for risk in result.risks:
                st.warning(f"• {risk}")

        with col_right:
            st.subheader("⚡ المحفزات المرصودة (Catalysts)")
            cats = result.catalysts
            st.write(f"**الفنية:** {', '.join(cats.technical) if cats.technical else 'لا يوجد'}")
            st.write(f"**الأساسية:** {', '.join(cats.fundamental) if cats.fundamental else 'لا يوجد'}")
            st.write(f"**المؤسسية:** {', '.join(cats.institutional) if cats.institutional else 'لا يوجد'}")
            st.write(f"**المشاعر:** {', '.join(cats.sentiment) if cats.sentiment else 'لا يوجد'}")

        # التقرير النصي الشامل
        with st.expander("📄 التقرير الشامل المولد بواسطة الذكاء الاصطناعي"):
            st.markdown(result.ai_report)
