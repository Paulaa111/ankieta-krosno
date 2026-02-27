import streamlit as st
import pandas as pd
from datetime import datetime
import time
from streamlit_gsheets import GSheetsConnection

# Konfiguracja strony
st.set_page_config(
    page_title="Badanie Cyfrowe – Krosno",
    page_icon="⚡",
    layout="centered"
)

# ── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #0a0f1e;
    font-family: 'DM Sans', sans-serif;
    color: #e2e8f0;
}

/* Ukryj domyślny header Streamlit */
header[data-testid="stHeader"] { background: transparent; }
.stApp > header { display: none; }

/* ── HERO BANNER ── */
.hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2540 50%, #0a1628 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 24px;
    padding: 48px 40px 40px;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(59,130,246,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.4);
    color: #60a5fa;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 18px;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.2rem !important;
    line-height: 1.15 !important;
    color: #f8fafc !important;
    margin: 0 0 16px !important;
    padding: 0 !important;
}
.hero h1 span { color: #60a5fa; }
.hero p {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.7;
    max-width: 560px;
    margin: 0;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 12px;
    color: #cbd5e1;
    margin-top: 20px;
}

/* ── SECTION HEADERS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 40px 0 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.section-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #f1f5f9;
    margin: 0;
}
.section-sub {
    font-size: 0.78rem;
    color: #64748b;
    margin: 0;
}

/* ── CARD ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(59,130,246,0.3); }

/* ── INPUTS ── */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}

/* Label */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stRadio"] label,
div[data-testid="stCheckbox"] label,
div[data-testid="stSlider"] label,
.stSlider label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Radio buttons */
div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
div[data-testid="stRadio"] > div > label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    font-size: 0.88rem !important;
    color: #cbd5e1 !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: rgba(59,130,246,0.4) !important;
    background: rgba(59,130,246,0.05) !important;
}

/* Checkboxes */
div[data-testid="stCheckbox"] > label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 6px !important;
    transition: all 0.2s !important;
    font-size: 0.88rem !important;
    color: #cbd5e1 !important;
}
div[data-testid="stCheckbox"] > label:hover {
    border-color: rgba(59,130,246,0.4) !important;
    background: rgba(59,130,246,0.05) !important;
}

/* Slider */
div[data-testid="stSlider"] {
    padding: 4px 0;
}

/* ── SUBMIT BUTTON ── */
div[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 14px !important;
    height: 56px !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 24px rgba(37,99,235,0.35) !important;
    margin-top: 16px !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(37,99,235,0.5) !important;
}

/* ── PROGRESS ── */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
    border-radius: 100px !important;
}

/* ── SUCCESS / ERROR MESSAGES ── */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: none !important;
}

/* ── STEP COUNTER ── */
.step-counter {
    display: flex;
    gap: 6px;
    margin-bottom: 32px;
}
.step-dot {
    height: 4px;
    border-radius: 100px;
    flex: 1;
    background: rgba(255,255,255,0.08);
}
.step-dot.active { background: linear-gradient(90deg, #3b82f6, #6366f1); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── POŁĄCZENIE ──────────────────────────────────────────────────────────────
conn = st.connection("gsheets", type=GSheetsConnection)

# ── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">⚡ Badanie 2025 · Krosno</div>
    <h1>Cyfrowe potrzeby<br><span>krośnieńskiego biznesu</span></h1>
    <p>
        Cześć! Jestem Paula i realizuję projekt badawczy dotyczący wyzwań operacyjnych
        lokalnych firm. Twoje odpowiedzi pomogą mi zrozumieć, które procesy są
        najbardziej czasochłonne i jak technologia może wesprzeć nasz rynek.
    </p>
    <div class="hero-badge">🔒 Anonimowe · Zajmuje ~3 min · Dziękuję z góry!</div>
</div>
""", unsafe_allow_html=True)

# ── STEP DOTS ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-counter">
    <div class="step-dot active"></div>
    <div class="step-dot active"></div>
    <div class="step-dot active"></div>
</div>
""", unsafe_allow_html=True)

# ── FORMULARZ ───────────────────────────────────────────────────────────────
with st.form("ankieta_final"):

    # ── SEKCJA 1 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏢</div>
        <div>
            <p class="section-title">Profil firmy</p>
            <p class="section-sub">Kilka podstawowych informacji o Twoim biznesie</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        nazwa_firmy = st.text_input("Nazwa firmy", placeholder="opcjonalnie - mozesz zostawic puste")

        lista_branz = [
            "Beauty (Fryzjer, Barber, Kosmetyczka)",
            "Weterynaria", "Edukacja i Szkolenia", "Gastronomia / Cukiernie / Piekarnie",
            "Logistyka i Transport", "Budownictwo i Usługi Techniczne", "Kwiaciarnie / Rękodzieło",
            "Biblioteki i Instytucje Kultury", "Motoryzacja / Warsztaty", "Handel Detaliczny",
            "Usługi Specjalistyczne (Prawo, Księgowość)", "Inna"
        ]
        branza = st.selectbox("Branża / Profil działalności", lista_branz)
        staz = st.radio(
            "Staż firmy na rynku",
            ["Nowa firma (< 1 rok)", "1–5 lat", "Powyżej 5 lat"],
            horizontal=True
        )

    # ── SEKCJA 2 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">⏳</div>
        <div>
            <p class="section-title">Czas i organizacja</p>
            <p class="section-sub">Co pochłania najwięcej Twojej energii?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Zaznacz zadania, które zabierają Ci najwięcej czasu:")
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.checkbox("💬  Obsługa zapytań klientów")
        p2 = st.checkbox("📅  Grafik i rezerwacje")
        p3 = st.checkbox("🧾  Dokumentacja i faktury")
    with col2:
        p4 = st.checkbox("📋  Oferty i kosztorysy")
        p5 = st.checkbox("📲  Marketing i social media")

    godziny_tydzien = st.select_slider(
        "Ile godzin tygodniowo pochłaniają sprawy organizacyjne?",
        options=["0–5h", "5–10h", "10–20h", "20h+"]
    )

    # ── SEKCJA 3 ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">💡</div>
        <div>
            <p class="section-title">Potencjał usprawnień</p>
            <p class="section-sub">Co chciałbyś zmienić w pierwszej kolejności?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    proces_auto = st.multiselect(
        "Gdyby mozna bylo zautomatyzowac jeden proces - co byloby priorytetem?",
        ["Kontakt z klientem", "Rezerwacje online", "Automatyczne wyceny",
         "Raporty i faktury", "Zarzadzanie zapasami", "Inne"]
    )
    inne_proces = st.text_input("Jesli wybrales/as 'Inne' - wpisz co to za proces:", placeholder="np. planowanie dostaw")

    preferencja_narzedzia = st.radio(
        "Preferowana platforma do pracy z narzędziami:",
        ["📱  Telefon (aplikacja, powiadomienia)", "💻  Komputer (przeglądarka, Excel)", "📟  Tablet"],
        horizontal=False
    )

    wizja = st.radio(
        "Na co zostałby przeznaczony odzyskany czas (np. 10h/mies.)?",
        ["😌  Odpoczynek / czas prywatny", "📈  Więcej zleceń", "📚  Szkolenia i rozwój", "🚀  Nowe kierunki usług"]
    )

    nowoczesnosc = st.select_slider(
        "Twoje nastawienie do nowych technologii wspomagających pracę:",
        options=["Tradycyjne", "Ostrożne", "Otwarte", "Entuzjastyczne"]
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("⚡  WYŚLIJ ANKIETĘ")

# ── ZAPIS ───────────────────────────────────────────────────────────────────
if submit:
    try:
        progress_text = "Zapisuję Twoje odpowiedzi…"
        my_bar = st.progress(0, text=progress_text)

        nowe_dane = pd.DataFrame([{
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nazwa_Firmy": nazwa_firmy,
            "Branża": branza,
            "Staż": staz,
            "Godziny_Tyg": godziny_tydzien,
            "Priorytet_Auto": ", ".join(proces_auto),
            "Inne_proces": inne_proces,
            "Platforma": preferencja_narzedzia,
            "Przeznaczenie_Czasu": wizja,
            "Podejście_Tech": nowoczesnosc
        }])

        for pct in range(0, 101, 20):
            my_bar.progress(pct, text=progress_text)
            time.sleep(0.1)

        conn.update(worksheet="Sheet1", data=nowe_dane)

        my_bar.progress(100)
        time.sleep(0.4)
        my_bar.empty()

        st.balloons()
        st.success("### ✅ Dziękuję! Twoja opinia została zapisana.")
        st.toast("Dane zapisane pomyślnie!", icon="✅")

    except Exception as e:
        st.error("Wystąpił problem z połączeniem z arkuszem.")
        st.info(f"Treść błędu: {e}")
        st.warning("""
        **Co możesz teraz zrobić?**
        1. Sprawdź czy zakładka w Arkuszu Google nazywa się dokładnie **Sheet1** (bez spacji).
        2. Sprawdź czy w Secrets link jest w cudzysłowie i kończy się na `/edit`.
        """)
