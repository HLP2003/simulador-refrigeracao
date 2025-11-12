# simulador_refrigeracao_unico.py
# Simulador único com DB embutido (Streamlit)
# Requisitos: streamlit, matplotlib, pandas, numpy
#
# Uso:
# pip install streamlit matplotlib pandas numpy
# streamlit run simulador_refrigeracao_unico.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração - 2010–2025", layout="wide")

# --------------------------
# Banco de dados embutido
# --------------------------
# CPUs (seleção representativa 2010-2025; acrescente conforme desejar)
CPUS = [
    {"modelo": "AMD Ryzen 5 5600", "tdp": 65, "ano": 2021, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5600X", "tdp": 65, "ano": 2020, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5600X3D", "tdp": 65, "ano": 2023, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5700X", "tdp": 65, "ano": 2022, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5500X3D", "tdp": 65, "ano": 2024, "socket": "AM4"},
    {"modelo": "AMD Ryzen 7 5800X", "tdp": 105, "ano": 2020, "socket": "AM4"},
    {"modelo": "AMD Ryzen 7 5700X", "tdp": 65, "ano": 2022, "socket": "AM4"},
    {"modelo": "AMD Ryzen 7 5800X3D", "tdp": 105, "ano": 2022, "socket": "AM4"},
    {"modelo": "AMD Ryzen 9 5900X", "tdp": 105, "ano": 2020, "socket": "AM4"},
    {"modelo": "AMD Ryzen 9 5950X", "tdp": 105, "ano": 2020, "socket": "AM4"},
    {"modelo": "AMD Ryzen 9 7950X", "tdp": 170, "ano": 2022, "socket": "AM5"},
    {"modelo": "AMD Ryzen 9 7950X3D", "tdp": 120, "ano": 2023, "socket": "AM5"},
    {"modelo": "AMD Ryzen 7 7800X3D", "tdp": 120, "ano": 2023, "socket": "AM5"},
    {"modelo": "AMD Ryzen 5 7600", "tdp": 65, "ano": 2022, "socket": "AM5"},
    {"modelo": "AMD Ryzen 5 7600X", "tdp": 105, "ano": 2022, "socket": "AM5"},
    {"modelo": "Intel Core i3-12100F", "tdp": 58, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i5-10400F", "tdp": 65, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i5-10600K", "tdp": 125, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i5-12400F", "tdp": 65, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i5-13400F", "tdp": 65, "ano": 2023, "socket": "LGA1700"},
    {"modelo": "Intel Core i5-14600K", "tdp": 125, "ano": 2024, "socket": "LGA1700"},
    {"modelo": "Intel Core i7-10700K", "tdp": 125, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i7-11700K", "tdp": 125, "ano": 2021, "socket": "LGA1200"},
    {"modelo": "Intel Core i7-12700K", "tdp": 125, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i7-13700K", "tdp": 125, "ano": 2023, "socket": "LGA1700"},
    {"modelo": "Intel Core i7-14700K", "tdp": 125, "ano": 2024, "socket": "LGA1700"},
    {"modelo": "Intel Core i9-10900K", "tdp": 125, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i9-11900K", "tdp": 125, "ano": 2021, "socket": "LGA1200"},
    {"modelo": "Intel Core i9-12900K", "tdp": 125, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i9-13900K", "tdp": 125, "ano": 2023, "socket": "LGA1700"},
    {"modelo": "Intel Core i9-14900K", "tdp": 125, "ano": 2024, "socket": "LGA1700"},
    {"modelo": "Intel Core i7-7700K", "tdp": 91, "ano": 2017, "socket": "LGA1151"},
    {"modelo": "Intel Core i7-6700K", "tdp": 91, "ano": 2015, "socket": "LGA1151"},
    {"modelo": "Intel Core i7-4790K", "tdp": 88, "ano": 2014, "socket": "LGA1150"},
    {"modelo": "Intel Core 2 Duo E8400", "tdp": 65, "ano": 2008, "socket": "LGA775"},
    {"modelo": "AMD FX-8350", "tdp": 125, "ano": 2012, "socket": "AM3+"}
]

# Coolers (inclui marcas populares no Brasil; tdp_suportado_nominal é referencial)
COOLERS = [
    {"modelo": "Noctua NH-D15", "tipo": "Air", "tdp_nominal": 250, "ruido_db": 24, "durabilidade_anos": 8},
    {"modelo": "Cooler Master Hyper 212", "tipo": "Air", "tdp_nominal": 150, "ruido_db": 35, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK620", "tipo": "Air", "tdp_nominal": 260, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Be Quiet! Dark Rock Pro 4", "tipo": "Air", "tdp_nominal": 250, "ruido_db": 24, "durabilidade_anos": 7},
    {"modelo": "DeepCool Gammaxx 400", "tipo": "Air", "tdp_nominal": 120, "ruido_db": 38, "durabilidade_anos": 4},
    {"modelo": "Arctic Freezer 34", "tipo": "Air", "tdp_nominal": 180, "ruido_db": 28, "durabilidade_anos": 5},
    {"modelo": "Corsair H100i (AIO 240)", "tipo": "AIO", "tdp_nominal": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Corsair H150i (AIO 360)", "tipo": "AIO", "tdp_nominal": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280)", "tipo": "AIO", "tdp_nominal": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool LS720 (AIO 360)", "tipo": "AIO", "tdp_nominal": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "TGT Storm 240 (AIO)", "tipo": "AIO", "tdp_nominal": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "TGT Glacier 120 (Air)", "tipo": "Air", "tdp_nominal": 100, "ruido_db": 36, "durabilidade_anos": 3},
    {"modelo": "Pichau AIO 240", "tipo": "AIO", "tdp_nominal": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Pichau Vento (Air)", "tipo": "Air", "tdp_nominal": 140, "ruido_db": 34, "durabilidade_anos": 4},
    {"modelo": "Husky Hunter 240 (AIO)", "tipo": "AIO", "tdp_nominal": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Husky Frost (Air)", "tipo": "Air", "tdp_nominal": 130, "ruido_db": 35, "durabilidade_anos": 4},
    {"modelo": "Rise Mode Sentinel 240 (AIO)", "tipo": "AIO", "tdp_nominal": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Ventus (Air)", "tipo": "Air", "tdp_nominal": 150, "ruido_db": 36, "durabilidade_anos": 4},
    {"modelo": "Arctic Liquid Freezer II 240", "tipo": "AIO", "tdp_nominal": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "Arctic Freezer 2 (Air)", "tipo": "Air", "tdp_nominal": 180, "ruido_db": 29, "durabilidade_anos": 5},
    {"modelo": "Gigabyte AORUS LIQUID 240", "tipo": "AIO", "tdp_nominal": 300, "ruido_db": 31, "durabilidade_anos": 6},
    {"modelo": "DeepCool Castle 360EX", "tipo": "AIO", "tdp_nominal": 350, "ruido_db": 31, "durabilidade_anos": 7}
]

# Safety configuration (base safety reduction applied to all coolers)
BASE_SAFETY_PCT = 0.12  # 12% base reduction

# --------------------------
# Utilitários
# --------------------------
def find_cpus_by_text(q):
    ql = q.strip().lower()
    if not ql:
        return CPUS
    return [c for c in CPUS if ql in c["modelo"].lower()]

def find_coolers_by_text(q):
    ql = q.strip().lower()
    if not ql:
        return COOLERS
    return [c for c in COOLERS if ql in c["modelo"].lower()]

def compute_effective_capacity(cooler_nominal, cpu_tdp):
    """
    Retorna a capacidade efetiva do cooler aplicando:
     - redução base (BASE_SAFETY_PCT)
     - redução dinâmica adicional proporcional ao quão perto o CPU está do nominal.
       dinâmica = min(0.20, 0.15 * (cpu_tdp / cooler_nominal))
    """
    if cooler_nominal <= 0:
        return 0.0
    dynamic_pct = min(0.20, 0.15 * (cpu_tdp / cooler_nominal))
    effective = cooler_nominal * (1.0 - BASE_SAFETY_PCT) * (1.0 - dynamic_pct)
    return effective, round(BASE_SAFETY_PCT*100,1), round(dynamic_pct*100,1)

def estimate_temperature(cpu_tdp, capacity_effective, ambient_c=25.0, workload=1.0):
    """
    Modelo heurístico:
    - calor gerado = cpu_tdp * workload
    - se capacidade_effective >= calor -> delta proporcional menor
    - se capacidade_effective < calor -> delta cresce mais rápido (throttling risco)
    A constante K ajusta escala de temperatura. Valores calibrados para saída plausível.
    """
    power = cpu_tdp * workload
    if capacity_effective <= 0:
        return 120.0  # fallback
    ratio = power / capacity_effective  # >1 means over-capacity
    K = 55.0
    # penaliza quando ratio>1
    if ratio <= 1.0:
        delta = ratio * (K * 0.9)  # dentro do limite temperatura sobe menos
    else:
        # quando excede, aumenta mais agressivamente
        delta = (1.0 * (K * 0.9)) + ((ratio - 1.0) * (K * 2.0))
    return round(ambient_c + delta, 1)

def estimate_noise(cooler, utilization_pct):
    """
    Estimativa de ruído: assumimos ruído nominal representa nível médio em uso.
    O ruído escala com raiz da utilização para suavizar subida.
    """
    base = cooler.get("ruido_db", 30)
    scale = sqrt(min(1.0, utilization_pct/100.0))
    return round(base * (0.6 + 0.4*scale), 1)  # 0.6..1.0 escala

def estimate_durability(cooler, utilization_pct):
    """
    Diminui a durabilidade se o cooler trabalhasse perto do limite constantemente.
    Se utilização efetiva > 80% diminui até 50%.
    """
    base_years = cooler.get("durabilidade_anos", 5)
    if utilization_pct <= 80:
        return base_years
    else:
        excess = (utilization_pct - 80) / 20.0  # 0..1 quando 80..100%
        return max(1, int(base_years * (1.0 - 0.5*excess)))

# --------------------------
# Interface Streamlit
# --------------------------
# Layout: duas colunas principais
st.title("Simulador de Refrigeração de CPU (2010–2025)")
st.markdown("Simulação comparativa com fator de segurança dinâmico. Use o campo de pesquisa para encontrar modelos rapidamente.")

with st.expander("Instruções rápidas (clique para abrir)"):
    st.write("""
    - Pesquise por parte do nome do processador ou cooler (ex.: 'Ryzen 5', 'Noctua', 'TGT').
    - Selecione CPU e cooler e clique em 'Simular'.
    - O sistema aplica um fator base de segurança (12%) e uma redução dinâmica (até 15-20%) dependendo da combinação.
    - O gráfico mostra Temperatura × Carga; painel lateral apresenta métricas detalhadas.
    """)

col_left, col_right = st.columns((2,1))

with col_left:
    st.subheader("Busca e seleção")
    q = st.text_input("Pesquisar (CPU ou Cooler)", value="")
    cpus_list = find_cpus_by_text(q)
    coolers_list = find_coolers_by_text(q)

    st.markdown("**Processadores encontrados**")
    cpu_df = pd.DataFrame(cpus_list).loc[:, ["modelo","tdp","ano","socket"]]
    st.dataframe(cpu_df, height=200)

    st.markdown("**Coolers encontrados**")
    cool_df = pd.DataFrame(coolers_list).loc[:, ["modelo","tipo","tdp_nominal","ruido_db","durabilidade_anos"]]
    st.dataframe(cool_df, height=200)

    # selectors
    cpu_choice = st.selectbox("Selecione o processador para simular", [c["modelo"] for c in cpus_list])
    cooler_choice = st.selectbox("Selecione o cooler", [c["modelo"] for c in coolers_list])

    ambient = st.number_input("Temperatura ambiente (°C)", min_value=10.0, max_value=40.0, value=25.0, step=1.0)
    workload_slider = st.slider("Carga (percentual do TDP)", 10, 150, 100)  # 10% .. 150%
    show_detailed = st.checkbox("Mostrar gráfico detalhado (Temperatura vs carga)", value=True)

    if st.button("Simular"):
        # fetch objects
        cpu = next((c for c in CPUS if c["modelo"] == cpu_choice), None)
        cooler = next((c for c in COOLERS if c["modelo"] == cooler_choice), None)

        if cpu is None or cooler is None:
            st.error("Selecionar CPU e cooler válidos.")
        else:
            cpu_tdp = cpu["tdp"]
            nominal = cooler["tdp_nominal"]
            capacity_eff, base_pct, dynamic_pct = compute_effective_capacity(nominal, cpu_tdp)

            # utilization percentage relative to effective capacity
            utilization_pct = round((cpu_tdp * (workload_slider/100.0)) / capacity_eff * 100.0, 1) if capacity_eff>0 else 999.9

            temp_est = estimate_temperature(cpu_tdp, capacity_eff, ambient_c=ambient, workload=workload_slider/100.0)
            noise_est = estimate_noise(cooler, utilization_pct)
            dur_est = estimate_durability(cooler, utilization_pct)

            # textual results - right column will also show
            st.markdown("### Resultado")
            st.write(f"**CPU:** {cpu['modelo']} — TDP: {cpu_tdp} W")
            st.write(f"**Cooler:** {cooler['modelo']} ({cooler['tipo']}) — Nominal: {nominal} W")
            st.write(f"**Capacidade efetiva aplicada:** {capacity_eff:.1f} W (redução base {base_pct}% + dinâmica {dynamic_pct}%)")
            st.write(f"**Carga aplicada:** {workload_slider}% → potência gerada: {cpu_tdp * workload_slider/100.0:.1f} W")
            st.write(f"**Utilização da capacidade efetiva:** {utilization_pct}%")
            st.write(f"**Temperatura estimada (IHS) em carga:** {temp_est} °C (ambiente {ambient} °C)")
            st.write(f"**Ruído estimado:** {noise_est} dB")
            st.write(f"**Durabilidade estimada:** ~{dur_est} anos")

            # recommendation
            if utilization_pct <= 70:
                st.success("Sistema seguro: cooler com folga adequada.")
            elif utilization_pct <= 90:
                st.info("Sistema adequado: operação dentro dos limites, mas próxima do limite em cargas elevadas.")
            else:
                st.error("Risco: capacidade efetiva do cooler pode ser insuficiente. Considere um modelo mais potente ou ajuste de perfil de uso.")

            # Graphs
            if show_detailed:
                st.markdown("### Gráfico: Temperatura vs Carga")
                loads = np.linspace(10, 150, 30)  # percent
                temps = [estimate_temperature(cpu_tdp, capacity_eff, ambient_c=ambient, workload=l/100.0) for l in loads]

                fig, ax = plt.subplots(figsize=(8,4))
                ax.plot(loads, temps, linewidth=2)
                ax.scatter([workload_slider], [temp_est], color="red", zorder=5)
                ax.set_xlabel("Carga do processador (% do TDP)")
                ax.set_ylabel("Temperatura estimada (°C)")
                ax.set_title(f"Temperatura estimada — {cpu['modelo']} + {cooler['modelo']}")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.axvline(workload_slider, color='gray', linestyle=':', linewidth=1)
                st.pyplot(fig)

            # capacity comparison chart
            st.markdown("### Comparativo: TDP vs Capacidade efetiva")
            fig2, ax2 = plt.subplots(figsize=(6,3))
            ax2.bar(["TDP (W)","Capacidade Efetiva (W)"], [cpu_tdp * (workload_slider/100.0), capacity_eff], color=["#2f72b7","#7f8fa6"])
            ax2.set_ylabel("Potência (W)")
            ax2.set_ylim(0, max(capacity_eff, cpu_tdp*1.6)+20)
            for i,(val,lab) in enumerate(zip([cpu_tdp*(workload_slider/100.0),capacity_eff], ["TDP","Capacidade"])):
                ax2.text(i, val + max(1,0.02*val), f"{val:.1f}", ha='center', fontsize=10)
            st.pyplot(fig2)

with col_right:
    st.subheader("Detalhes rápidos")
    st.write("Use este painel para comparar rapidamente as métricas do cooler.")
    selected_cooler = st.selectbox("Visualizar dados do cooler", [c["modelo"] for c in COOLERS])
    cinfo = next((c for c in COOLERS if c["modelo"]==selected_cooler), None)
    if cinfo:
        st.write(f"Modelo: {cinfo['modelo']}")
        st.write(f"Tipo: {cinfo['tipo']}")
        st.write(f"Nominal (referencial): {cinfo['tdp_nominal']} W")
        # show effective capacity for a sample CPU (median)
        sample_cpu_tdp = 95
        eff, bp, dp = compute_effective_capacity(cinfo['tdp_nominal'], sample_cpu_tdp)
        st.write(f"Capacidade efetiva (exemplo com CPU 95W): {eff:.1f} W")
        st.write(f"Ruído (médio): {cinfo['ruido_db']} dB")
        st.write(f"Durabilidade (estimada): {cinfo['durabilidade_anos']} anos")
    st.markdown("---")
    st.subheader("Observações sobre o modelo")
    st.write("""
    - Este simulador usa modelos heurísticos para comparações e estimativas.  
    - `tdp_nominal` é um valor referencial; `capacidade efetiva` incorpora margem de segurança.  
    - Para medições precisas de temperatura utilize sensores reais (HWMonitor, HWiNFO) e testes práticos.  
    - Valores de ruído e durabilidade são estimativas médias baseadas em reviews e especificações.
    """)

st.markdown("---")
st.caption("Versão unificada — banco interno 2010–2025. Ajuste o banco de dados no código caso queira incluir mais modelos.")
