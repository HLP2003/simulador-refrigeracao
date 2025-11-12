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
# Observações:
# - tdp_manufacturer: valor declarado pelo fabricante (quando conhecido)
# - tdp_nominal: valor efetivo usado no simulador = 0.8 * tdp_manufacturer,
#   aplicando a redução de 20% de eficiência prática que você solicitou.
# --------------------------

CPUS = [
    # (mantive os originais, verifiquei alguns TDPs; adicionei novas linhas)
    {"modelo": "AMD Ryzen 5 5600", "tdp": 65, "ano": 2021, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5600X", "tdp": 65, "ano": 2020, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5600X3D", "tdp": 105, "ano": 2023, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 5500X3D", "tdp": 105, "ano": 2024, "socket": "AM4"},
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

    # Intel mainstream (adicionei representativos das 1ª→7ª gerações)
    {"modelo": "Intel Core i3-530", "tdp": 73, "ano": 2010, "socket": "LGA1156"},  # 1ª gen (representativo)
    {"modelo": "Intel Core i3-3240", "tdp": 55, "ano": 2012, "socket": "LGA1155"},  # 3ª gen
    {"modelo": "Intel Core i3-6100", "tdp": 51, "ano": 2015, "socket": "LGA1151"},  # 6ª gen (Skylake)
    {"modelo": "Intel Core i3-8100", "tdp": 65, "ano": 2017, "socket": "LGA1151"},  # 8ª gen (adicional)
    {"modelo": "Intel Core i5-10400F", "tdp": 65, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i5-10600K", "tdp": 125, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i5-12400F", "tdp": 120, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i5-13400F", "tdp": 150, "ano": 2023, "socket": "LGA1700"},
    {"modelo": "Intel Core i7-920", "tdp": 130, "ano": 2008, "socket": "LGA1366"},  # 1ª era Core i7 (represent.)
    {"modelo": "Intel Core i7-7700K", "tdp": 91, "ano": 2017, "socket": "LGA1151"},
    {"modelo": "Intel Core i7-11700K", "tdp": 125, "ano": 2021, "socket": "LGA1200"},
    {"modelo": "Intel Core i7-12700K", "tdp": 190, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i7-13700K", "tdp": 250, "ano": 2023, "socket": "LGA1700"},

    {"modelo": "Intel Core i9-10900K", "tdp": 125, "ano": 2020, "socket": "LGA1200"},
    {"modelo": "Intel Core i9-11900K", "tdp": 125, "ano": 2021, "socket": "LGA1200"},
    {"modelo": "Intel Core i9-12900K", "tdp": 240, "ano": 2022, "socket": "LGA1700"},
    {"modelo": "Intel Core i9-13900K", "tdp": 250, "ano": 2023, "socket": "LGA1700"},
    {"modelo": "Intel Core i9-14900K", "tdp": 250, "ano": 2023, "socket": "LGA1700"},
    
    {"modelo": "Intel Core 2 Duo E8400", "tdp": 65, "ano": 2008, "socket": "LGA775"},
    {"modelo": "AMD FX-8350", "tdp": 125, "ano": 2012, "socket": "AM3+"},

    # Xeon E5 v3 / v4 (adicionados)
    {"modelo": "Intel Xeon E5-2670 v3", "tdp": 120, "ano": 2014, "socket": "LGA2011-v3"},
    {"modelo": "Intel Xeon E5-2680 v3", "tdp": 120, "ano": 2014, "socket": "LGA2011-v3"},
    {"modelo": "Intel Xeon E5-2690 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3"},
    {"modelo": "Intel Xeon E5-2680 v4", "tdp": 120, "ano": 2016, "socket": "LGA2011-v3"},
    {"modelo": "Intel Xeon E5-2699 v4", "tdp": 145, "ano": 2016, "socket": "LGA2011-v3"},
    {"modelo": "Intel Xeon E5-2650 v3", "tdp": 105, "ano": 2014, "socket": "LGA2011-v3"}
]

# Coolers: adicionei vários e incluí tdp_manufacturer + tdp_nominal (ajustado -20%)
COOLERS = [
    # manufacturer TDP listed (tdp_manufacturer) -> tdp_nominal = 0.8 * tdp_manufacturer
    {"modelo": "Noctua NH-D15", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 8},
    {"modelo": "Cooler Master Hyper 212", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK400", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 29, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK620", "tipo": "Air", "tdp_manufacturer": 260, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Be Quiet! Dark Rock Pro 4", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 7},
    {"modelo": "DeepCool Gammaxx 400", "tipo": "Air", "tdp_manufacturer": 120, "ruido_db": 38, "durabilidade_anos": 4},
    {"modelo": "Arctic Freezer 34", "tipo": "Air", "tdp_manufacturer": 180, "ruido_db": 28, "durabilidade_anos": 5},
    {"modelo": "Rise Mode G800 (Ventus/G800)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 36, "durabilidade_anos": 4},
    {"modelo": "Thermalright Macho 120 (Macho 120 Rev.A)", "tipo": "Air", "tdp_manufacturer": 200, "ruido_db": 30, "durabilidade_anos": 6},
    {"modelo": "Thermalright TRUE Spirit 140", "tipo": "Air", "tdp_manufacturer": 200, "ruido_db": 28, "durabilidade_anos": 6},

    # AIO / Water coolers (manufacturer spec)
    {"modelo": "Corsair H100i (AIO 240)", "tipo": "AIO", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Corsair H150i (AIO 360)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "Arctic Liquid Freezer II 240", "tipo": "AIO", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "DeepCool LS720 (AIO 360)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "Rise Mode Sentinel 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},

    # outros modelos populares
    {"modelo": "TGT Storm 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Pichau AIO 240", "tipo": "AIO", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "DeepCool Castle 360EX", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "TGT Glacier 120 (Air)", "tipo": "Air", "tdp_manufacturer": 100, "ruido_db": 36, "durabilidade_anos": 3},
    {"modelo": "Pichau Vento (Air)", "tipo": "Air", "tdp_manufacturer": 140, "ruido_db": 34, "durabilidade_anos": 4},
    {"modelo": "AK400 DIGITAL (DeepCool)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 5},
    {"modelo": "Husky Hunter 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
]

# aplicar ajuste de 20% de eficiência: criar campo tdp_nominal = 0.8 * tdp_manufacturer
for c in COOLERS:
    if "tdp_manufacturer" in c and c.get("tdp_manufacturer") is not None:
        c["tdp_nominal"] = round(0.8 * c["tdp_manufacturer"], 1)
    else:
        # fallback para compatibilidade com o código anterior
        c["tdp_nominal"] = c.get("tdp_nominal", 0)

# Safety configuration (base safety reduction applied to all coolers)
BASE_SAFETY_PCT = 0.12  # 12% base reduction

# --------------------------
# Utilitários (mantive a lógica original)
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
        return 0.0, 0.0, 0.0
    dynamic_pct = min(0.20, 0.15 * (cpu_tdp / cooler_nominal))
    effective = cooler_nominal * (1.0 - BASE_SAFETY_PCT) * (1.0 - dynamic_pct)
    return effective, round(BASE_SAFETY_PCT*100,1), round(dynamic_pct*100,1)

def estimate_temperature(cpu_tdp, capacity_effective, ambient_c=25.0, workload=1.0):
    power = cpu_tdp * workload
    if capacity_effective <= 0:
        return 120.0  # fallback
    ratio = power / capacity_effective  # >1 means over-capacity
    K = 55.0
    if ratio <= 1.0:
        delta = ratio * (K * 0.9)
    else:
        delta = (1.0 * (K * 0.9)) + ((ratio - 1.0) * (K * 2.0))
    return round(ambient_c + delta, 1)

def estimate_noise(cooler, utilization_pct):
    base = cooler.get("ruido_db", 30)
    scale = sqrt(min(1.0, utilization_pct/100.0))
    return round(base * (0.6 + 0.4*scale), 1)

def estimate_durability(cooler, utilization_pct):
    base_years = cooler.get("durabilidade_anos", 5)
    if utilization_pct <= 80:
        return base_years
    else:
        excess = (utilization_pct - 80) / 20.0
        return max(1, int(base_years * (1.0 - 0.5*excess)))

# --------------------------
# Interface Streamlit (ajustada: sem busca livre — apenas seletores)
# --------------------------
st.title("Simulador de Refrigeração de CPU (2010–2025)")
st.markdown("Simulação comparativa com fator de segurança dinâmico. Selecione CPU e cooler e clique em 'Simular'.")

with st.expander("Instruções rápidas (clique para abrir)"):
    st.write("""
    - Selecione o processador e o cooler nos menus.
    - Os valores de TDP dos coolers foram ajustados para refletir 20% menos eficiência prática.
    - O gráfico mostra Temperatura × Carga; painel lateral apresenta métricas detalhadas.
    """)

col_left, col_right = st.columns((2,1))

with col_left:
    st.subheader("Seleção")
    # lista completa nos selects (removida a busca por texto)
    cpu_choice = st.selectbox("Selecione o processador para simular", [c["modelo"] for c in CPUS])
    cooler_choice = st.selectbox("Selecione o cooler", [c["modelo"] for c in COOLERS])

    ambient = st.number_input("Temperatura ambiente (°C)", min_value=10.0, max_value=40.0, value=25.0, step=1.0)
    workload_slider = st.slider("Carga (percentual do TDP)", 10, 150, 100)  # 10% .. 150%
    show_detailed = st.checkbox("Mostrar gráfico detalhado (Temperatura vs carga)", value=True)

    if st.button("Simular"):
        cpu = next((c for c in CPUS if c["modelo"] == cpu_choice), None)
        cooler = next((c for c in COOLERS if c["modelo"] == cooler_choice), None)

        if cpu is None or cooler is None:
            st.error("Selecionar CPU e cooler válidos.")
        else:
            cpu_tdp = cpu["tdp"]
            nominal = cooler.get("tdp_nominal", 0)
            capacity_eff, base_pct, dynamic_pct = compute_effective_capacity(nominal, cpu_tdp)

            utilization_pct = round((cpu_tdp * (workload_slider/100.0)) / capacity_eff * 100.0, 1) if capacity_eff>0 else 999.9

            temp_est = estimate_temperature(cpu_tdp, capacity_eff, ambient_c=ambient, workload=workload_slider/100.0)
            noise_est = estimate_noise(cooler, utilization_pct)
            dur_est = estimate_durability(cooler, utilization_pct)

            st.markdown("### Resultado")
            st.write(f"*CPU:* {cpu['modelo']} — TDP: {cpu_tdp} W")
            st.write(f"*Cooler:* {cooler['modelo']} ({cooler['tipo']}) — Nominal (ajustado): {nominal} W")
            if "tdp_manufacturer" in cooler:
                st.write(f"*Especificação fabricante:* {cooler['tdp_manufacturer']} W (ajustado -20% → {nominal} W)")
            st.write(f"*Capacidade efetiva aplicada:* {capacity_eff:.1f} W (redução base {base_pct}% + dinâmica {dynamic_pct}%)")
            st.write(f"*Carga aplicada:* {workload_slider}% → potência gerada: {cpu_tdp * workload_slider/100.0:.1f} W")
            st.write(f"*Utilização da capacidade efetiva:* {utilization_pct}%")
            st.write(f"*Temperatura estimada (IHS) em carga:* {temp_est} °C (ambiente {ambient} °C)")
            st.write(f"*Ruído estimado:* {noise_est} dB")
            st.write(f"*Durabilidade estimada:* ~{dur_est} anos")

            if utilization_pct <= 70:
                st.success("Sistema seguro: cooler com folga adequada.")
            elif utilization_pct <= 90:
                st.info("Sistema adequado: operação dentro dos limites, mas próxima do limite em cargas elevadas.")
            else:
                st.error("Risco: capacidade efetiva do cooler pode ser insuficiente. Considere um modelo mais potente ou ajuste de perfil de uso.")

            # Gráficos
            if show_detailed:
                st.markdown("### Gráfico: Temperatura vs Carga")
                loads = np.linspace(10, 150, 30)
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
        st.write(f"Nominal (ajustado): {cinfo['tdp_nominal']} W")
        if "tdp_manufacturer" in cinfo:
            st.write(f"Especificação do fabricante: {cinfo['tdp_manufacturer']} W (aplicado -20% → {cinfo['tdp_nominal']} W)")
        st.write(f"Ruído (médio): {cinfo['ruido_db']} dB")
        st.write(f"Durabilidade (estimada): {cinfo['durabilidade_anos']} anos")
    st.markdown("---")
    st.subheader("Observações sobre o modelo")
    st.write("""
    - Este simulador usa modelos heurísticos para comparações e estimativas.  
    - tdp_manufacturer é um valor declarado pelo fabricante; tdp_nominal aplica -20% de eficiência prática.  
    - Para medições precisas de temperatura utilize sensores reais (HWMonitor, HWiNFO) e testes práticos.  
    - Valores de ruído e durabilidade são estimativas médias baseadas em reviews e especificações.
    """)

st.markdown("---")
st.caption("Versão modificada — busca removida e banco estendido (Xeon E5 v3/v4, mais coolers). Ajuste os dados no código conforme necessário.")




