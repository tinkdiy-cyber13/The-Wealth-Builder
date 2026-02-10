import streamlit as st
import pandas as pd
import json
import os
import time

# Configurare stil Premium
st.set_page_config(page_title="Wealth Builder Pro", page_icon="💰", layout="wide")

DB_FILE = "baza_wealth_vizite.json"

# --- FUNCTII BAZA DE DATE (CONTOR OO) ---
def incarca_vizite():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {"vizite": 0}
    return {"vizite": 0}

def salveaza_vizite(date):
    with open(DB_FILE, "w") as f: json.dump(date, f)

date_sistem = incarca_vizite()

if 'v_w' not in st.session_state:
    date_sistem["vizite"] = date_sistem.get("vizite", 0) + 1
    salveaza_vizite(date_sistem)
    st.session_state['v_w'] = True

# --- TITLU ȘI CONTOR OO ---
st.title("💰 Wealth Builder Pro")
st.markdown(
    f"""
    <div style='text-align: right; margin-top: -55px;'>
        <span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>
            OO: {date_sistem.get('vizite', 0)}
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown("### *\"Profits are better than wages.\" - J. Earl Shoaff*")
st.write("---")

# --- SIDEBAR PENTRU INPUTURI ---
with st.sidebar:
    st.header("⚙️ Parametri Financiari")
    investitie_initiala = st.number_input("Suma Inițială (€):", value=1000, step=100)
    depunere_lunara = st.number_input("Depunere Lunară (€):", value=200, step=50)
    dobanda_anuala = st.slider("Dobândă Anuală Estimată (%):", 1, 25, 8)
    ani = st.slider("Orizont de Timp (Ani):", 1, 50, 10)

# --- LOGICA DE CALCUL ---
luni = ani * 12
rata_lunara = (dobanda_anuala / 100) / 12
balanta = investitie_initiala
date_grafic = []

for luna in range(1, luni + 1):
    balanta = (balanta + depunere_lunara) * (1 + rata_lunara)
    if luna % 12 == 0:
        date_grafic.append({"An": luna // 12, "Total": round(balanta, 2)})

df = pd.DataFrame(date_grafic)

# --- AFIȘARE REZULTATE PE PĂTRATE ---
c1, c2, c3 = st.columns(3)

total_final = date_grafic[-1]["Total"]
total_investit = investitie_initiala + (depunere_lunara * luni)
profit_pur = total_final - total_investit

c1.metric("💰 Sumă Finală", f"{total_final:,.2f} €")
c2.metric("📥 Total Investit", f"{total_investit:,.2f} €")
c3.metric("📈 Profit Pur", f"{profit_pur:,.2f} €", delta=f"{((total_final/total_investit)-1)*100:.1f}%")

# --- GRAFIC EVOLUȚIE ---
st.divider()
st.subheader("📊 Evoluția Averei în Timp")
st.area_chart(df.set_index("An"), color="#22d3ee")

# --- TABEL DE PROIECTIE ---
with st.expander("📂 Vezi Tabelul Anual de Creștere"):
    st.dataframe(df, use_container_width=True)

# --- MESAJ DE FINAL ---
st.info("💡 Această proiecție este bazată pe dobândă compusă. Rezultatele pot varia, dar disciplina rămâne constantă!")

st.divider()
st.caption("Creat de Cristian | Protocol OO-Wealth | Hardware i5 Cloud")
