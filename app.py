import streamlit as st
import google.generativeai as genai

# 1. AYARLAR: Kendi API Anahtarını tırnak içine yapıştır
genai.configure(api_key="AIzaSyACo_b2KfNo7WyAitVNaXHLdn7r-UewhF8")
model = genai.GenerativeModel('gemini-3.1-pro-preview')

# 2. HAFIZA: Senin önceden aldığın ID'ler (Burası değişmez, çok hızlı çalışır)
DOSYA_KUTUPHANESI = {
    "Tanzimat - Servetifünun": "files/zjqlna9sb89s",
    "Milli Edebiyat": "files/fv556sw4n1ie",
    "Divan Edebiyatı": "files/8nbnbn0htcfv",
    "Cumhuriyet Dönemi": "files/uf2ppbawyp2l",
    "Halk Edebiyatı": "files/4g98e60cfsqi"
}

st.set_page_config(page_title="Edebiyat Soru Botu", page_icon="📚")
st.title("🎓 Edebiyat Sınav Asistanı")
st.info("Jarvis 0.1 altyapısıyla hazırlanmıştır.") # Senin proje ismin ;)

# Kategori Seçimi
secilen_kategori = st.selectbox("Hangi dönemden soru gelsin?", list(DOSYA_KUTUPHANESI.keys()))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Soru Sorma Butonu
# Soru Sorma Butonu
if st.button("Yeni Soru Sor 🚀"):
    file_uri = DOSYA_KUTUPHANESI[secilen_kategori]
    
    with st.spinner("Büyük dosyalar taranıyor, saniyeler içinde hazır..."):
        try:
            # DOĞRU FORMAT BURASI: 'file_data' anahtarını ekledik
            response = model.generate_content([
                {
                    "file_data": {
                        "mime_type": "application/pdf",
                        "file_uri": file_uri # 'files/...' formatındaki ID yeterli
                    }
                },
                f"Sana verdiğim {secilen_kategori} dosyasını incele ve bana 4 şıklı bir edebiyat sorusu sor. Cevabı en sona sakla."
            ])
            
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

# Sohbet Geçmişini Göster
for message in reversed(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.write(message["content"])

