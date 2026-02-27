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

# Soru Sorma Butonu İçindeki Kısım
if st.button("Yeni Soru Getir 🚀"):
    file_id = DOSYA_KUTUPHANESI[secilen_kategori]
    tam_adres = f"https://generativelanguage.googleapis.com/v1beta/{file_id}"
    
    with st.spinner("Notlar taranıyor (Hızlı Mod)..."):
        try:
            # HIZLI PROMPT: Dosyanın tamamını değil, küçük bir kısmını odakla diyoruz
            prompt = (
                f"Bu dosyanın içinden rastgele bir sayfa seç ve {secilen_kategori} hakkında zor bir soru üret. "
                "Tüm dosyayı analiz etmek için vakit kaybetme, hızlı ol. "
                "Cevabı şu JSON formatında ver: "
                '{"soru": "...", "siklar": ["...", "...", "...", "..."], "cevap": "..."}'
            )
            
            # Flash model zaten çok hızlıdır
            response = model.generate_content([
                {"file_data": {"mime_type": "application/pdf", "file_uri": tam_adres}},
                prompt
            ], generation_config={
                "response_mime_type": "application/json",
                "candidate_count": 1 # Sadece 1 cevap üretmesi hızı artırır
            })
            
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

