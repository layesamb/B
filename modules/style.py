import streamlit as st


def appliquer_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        [data-testid="stAppViewContainer"] {
            background: radial-gradient(ellipse 120% 80% at 50% -10%, #16463A 0%, #0B2B22 55%, #081F19 100%);
        }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] {
            background: #0B2B22;
            border-right: 1px solid rgba(201, 162, 75, 0.15);
        }
        [data-testid="stSidebar"] * { color: #F2EFE6 !important; }

        h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #F2EFE6 !important; }
        p, span, label, div { color: #E7E4DA; }

        .stButton > button, .stFormSubmitButton > button {
            background: #C9A24B;
            color: #0B2B22;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            background: #E0BC64;
            color: #0B2B22;
        }

        .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
            background: rgba(255,255,255,0.05) !important;
            color: #F2EFE6 !important;
            border: 1px solid rgba(201, 162, 75, 0.25) !important;
            border-radius: 8px !important;
        }

        [data-testid="stForm"], [data-testid="stExpander"] {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(201, 162, 75, 0.15) !important;
            border-radius: 14px !important;
        }

        .jour-carte {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(201, 162, 75, 0.15);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .exercice-ligne {
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            padding: 0.5rem 0.8rem;
            margin-bottom: 0.4rem;
            font-size: 0.92rem;
        }
        .exercice-fait { color: #C9A24B !important; text-decoration: line-through; opacity: 0.7; }

        .hero-eyebrow {
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #C9A24B;
            margin-bottom: 0.6rem;
            font-weight: 600;
        }
        .hero-title {
            font-family: 'Fraunces', serif;
            font-size: 2.3rem;
            color: #F2EFE6;
            margin: 0 0 1.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)


def titre_page(eyebrow, titre):
    st.markdown(f"""
        <div class="hero-eyebrow">{eyebrow}</div>
        <h1 class="hero-title">{titre}</h1>
    """, unsafe_allow_html=True)