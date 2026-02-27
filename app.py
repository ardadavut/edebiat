import streamlit as st
import google.generativeai as genai
import json

# API ve Model Ayarları
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3-flash-preview')

# Dosya ID'lerin
DOSYA_KUTUPHANESI = {
    "Tanzimat - Servetifünun": "files/zjqlna9sb89s",
    "Milli Edebiyat": "files/fv556sw4n1ie",
    "Divan Edebiyatı": "files/8nbnbn0htcfv",
    "Cumhuriyet Dönemi": "files/uf2ppbawyp2l",
    "Halk Edebiyatı": "files/4g98e60cfsqi"
}

st.set_page_config(page_title="Edebiyat Soru Botu", page_icon="📚")
st.title("🎓 Edebiyat Sınav Asistanı")

secilen_kategori = st.selectbox("Dönem Seçin:", list(DOSYA_KUTUPHANESI.keys()))

# Soru ve Şıkları Hafızada Tutmak İçin
if "soru_data" not in st.session_state:
    st.session_state.soru_data = None

if st.button("Yeni Soru Getir 🚀"):
    file_id = DOSYA_KUTUPHANESI[secilen_kategori]
    tam_adres = f"https://generativelanguage.googleapis.com/v1beta/{file_id}"
    
    with st.spinner("Soru hazırlanıyor..."):
        try:
            # Gemini'ye "Bana sadece JSON formatında cevap ver" diyoruz
            prompt = (
                f"Sana verdiğim {secilen_kategori} dosyasından zor bir soru seç. "
                "Cevabı tam olarak şu JSON formatında ver: "
                '{"soru": "Soru metni", "siklar": ["A şıkkı", "B şıkkı", "C şıkkı", "D şıkkı"], "cevap": "Doğru Şık Metni"}'
            )
            
            response = model.generate_content([
                {"file_data": {"mime_type": "application/pdf", "file_uri": tam_adres}},
                prompt
            ], generation_config={"response_mime_type": "application/json"})
            
            # Gelen JSON'u temizleyip sözlüğe çeviriyoruz
            st.session_state.soru_data = json.loads(response.text)
            st.session_state.cevap_verildi = False
        except Exception as e:
            st.error(f"Hata: {e}")

# Eğer ekranda bir soru varsa şıkları buton olarak göster
if st.session_state.soru_data:
    st.subheader("Soru:")
    st.write(st.session_state.soru_data["soru"])
    
    # Şıkları buton (kutucuk) yapma
    for sik in st.session_state.soru_data["siklar"]:
        if st.button(sik):
            if sik == st.session_state.soru_data["cevap"]:
                st.success("✅ Tebrikler! Doğru cevap.")
            else:
                st.error(f"❌ Maalesef yanlış. Doğru cevap: {st.session_state.soru_data['cevap']}")
