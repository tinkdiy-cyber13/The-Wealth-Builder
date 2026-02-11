import streamlit as st
import pandas as pd
import json
import os
import time

# Configurare stil Premium
st.set_page_config(page_title="Wealth Builder Pro v2.0", page_icon="💰", layout="wide")

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
st.title("💰 Wealth Builder Pro v2.0")
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
st.markdown("### *\"Don't wish it were easier, wish you were better.\" - J. Earl Shoaff*")
st.write("---")

# --- SIDEBAR PENTRU INPUTURI ---
with st.sidebar:
    st.header("⚙️ Configurare Plan")
    investitie_initiala = st.number_input("Suma Inițială (€):", value=25000, step=1000)
    dobanda_anuala = st.slider("Dobândă Anuală Estimată (%):", 1, 25, 8)
    ani_total = st.slider("Orizont de Timp (Ani):", 1, 40, 15)
    
    st.divider()
    st.subheader("🔄 Modificări pe parcurs")
    st.info("Aici poți schimba strategia după un anumit număr de ani.")
    an_schimbare = st.number_input("După câți ani schimbi depunerea?", value=5, min_value=1, max_value=ani_total)
    noua_depunere = st.number_input("Noua depunere lunară (€):", value=500, step=50, help="Poate fi și negativă dacă vrei să simulezi o retragere lunară.")
    retragere_one_time = st.number_input("Retragere/Depunere unică în acel an (€):", value=0, step=1000, help="Suma extrasă sau adăugată fix în anul schimbării.")

# --- LOGICA DE CALCUL DINAMICĂ ---
rata_lunara = (dobanda_anuala / 100) / 12
balanta = investitie_initiala
date_grafic = []
total_investit_cash = investitie_initiala

for an in range(1, ani_total + 1):
    # Determinăm depunerea pentru anul curent
    depunere_curenta = 200 # Depunerea standard de start
    if an > an_schimbare:
        depunere_curenta = noua_depunere
    
    # Aplicăm depunerea unică (one-time) la începutul anului de schimbare
    if an == an_schimbare:
        balanta += retragere_one_time
        total_investit_cash += retragere_one_time
    
    # Calculăm cele 12 luni ale anului
    for luna in range(1, 13):
        balanta = (balanta + depunere_curenta) * (1 + rata_lunara)
        total_investit_cash += depunere_curenta
        
    date_grafic.append({
        "An": an, 
        "Sold Final (€)": round(balanta, 2), 
        "Bani Depuși (€)": round(total_investit_cash, 2),
        "Profit (€)": round(balanta - total_investit_cash, 2)
    })

df = pd.DataFrame(date_grafic)

# --- AFIȘARE REZULTATE PE PĂTRATE ---
c1, c2, c3 = st.columns(3)

final_sum = df.iloc[-1]["Sold Final (€)"]
invested_sum = df.iloc[-1]["Bani Depuși (€)"]
pure_profit = df.iloc[-1]["Profit (€)"]

c1.metric("💰 Sold la Final", f"{final_sum:,.2f} €")
c2.metric("📥 Total Cash Depus", f"{invested_sum:,.2f} €")
c3.metric("📈 Profit Generat", f"{pure_profit:,.2f} €", delta=f"{((final_sum/invested_sum)-1)*100:.1f}%")

# --- GRAFIC EVOLUȚIE (DUAL: SOLD vs INVESTIȚIE) ---
st.divider()
st.subheader("📊 Analiza Creșterii Exponențiale")
st.area_chart(df.set_index("An")[["Sold Final (€)", "Bani Depuși (€)"]])

# --- TABEL DE PROIECTIE ---
with st.expander("📂 Vezi Raportul Anual Detaliat"):
    st.write("În acest tabel poți vedea exact cum profitul începe să depășească suma depusă de tine (Momentul de Libertate).")
    st.dataframe(df, use_container_width=True)

# --- MESAJ DE FINAL ---
st.success(f"💡 Moment cheie: În anul {an_schimbare}, ai ajustat strategia. Observă cum curba se schimbă după acest punct!")

st.divider()
st.caption("Arhitectură de Cristian | Protocol OO-Dynamic-Wealth | i5 Cloud Engine")

