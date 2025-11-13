# simulador_refrigeracao_otimizado.py
import streamlit as st, matplotlib.pyplot as plt, numpy as np
from math import sqrt

st.set_page_config(page_title="Simulador de Refrigeração", layout="wide")

CPUS = [
    {"modelo": "AMD Ryzen 5 1600X", "tdp": 95, "ano": 2017, "socket": "AM4", "frequencia_base": 3.6, "frequencia_turbo": 4.0, "arquitetura": "Zen"},
    {"modelo": "AMD Ryzen 5 3600", "tdp": 65, "ano": 2019, "socket": "AM4", "frequencia_base": 3.6, "frequencia_turbo": 4.2, "arquitetura": "Zen 2"},
    {"modelo": "AMD Ryzen 5 5600", "tdp": 65, "ano": 2021, "socket": "AM4", "frequencia_base": 3.5, "frequencia_turbo": 4.4, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 5 5600X", "tdp": 65, "ano": 2020, "socket": "AM4", "frequencia_base": 3.7, "frequencia_turbo": 4.6, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 5 5600X3D", "tdp": 105, "ano": 2022, "socket": "AM4", "frequencia_base": 3.3, "frequencia_turbo": 4.4, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 5 5500X3D", "tdp": 105, "ano": 2024, "socket": "AM4", "frequencia_base": 3.0, "frequencia_turbo": 4.0, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 5 7400F", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.7, "frequencia_turbo": 4.7, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7500F", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.7, "frequencia_turbo": 5.0, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600", "tdp": 65, "ano": 2022, "socket": "AM5", "frequencia_base": 3.8, "frequencia_turbo": 5.1, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600X", "tdp": 105, "ano": 2022, "socket": "AM5", "frequencia_base": 4.7, "frequencia_turbo": 5.3, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 5 7600X3D", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 4.1, "frequencia_turbo": 4.7, "arquitetura": "Zen 4 (3D)"},
    {"modelo": "AMD Ryzen 5 8400F", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 4.2, "frequencia_turbo": 4.7, "arquitetura": "Zen 5"},
    {"modelo": "AMD Ryzen 5 8500G", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.5, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)"},
    {"modelo": "AMD Ryzen 5 8600G", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 4.3, "frequencia_turbo": 5.0, "arquitetura": "Zen 5 (G)"},
    {"modelo": "AMD Ryzen 5 9600X", "tdp": 65, "ano": 2024, "socket": "AM5", "frequencia_base": 3.9, "frequencia_turbo": 5.4, "arquitetura": "Zen 5"},
    {"modelo": "AMD Ryzen 7 7700", "tdp": 65, "ano": 2023, "socket": "AM5", "frequencia_base": 3.8, "frequencia_turbo": 5.3, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 7 7700X", "tdp": 105, "ano": 2023, "socket": "AM5", "frequencia_base": 4.5, "frequencia_turbo": 5.4, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 7 5800X", "tdp": 105, "ano": 2020, "socket": "AM4", "frequencia_base": 3.8, "frequencia_turbo": 4.7, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 7 5800X3D", "tdp": 105, "ano": 2022, "socket": "AM4", "frequencia_base": 3.4, "frequencia_turbo": 4.5, "arquitetura": "Zen 3 (3D)"},
    {"modelo": "AMD Ryzen 9 5900X", "tdp": 105, "ano": 2020, "socket": "AM4", "frequencia_base": 3.7, "frequencia_turbo": 4.8, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 9 5950X", "tdp": 105, "ano": 2020, "socket": "AM4", "frequencia_base": 3.4, "frequencia_turbo": 4.9, "arquitetura": "Zen 3"},
    {"modelo": "AMD Ryzen 9 7950X", "tdp": 170, "ano": 2022, "socket": "AM5", "frequencia_base": 4.5, "frequencia_turbo": 5.7, "arquitetura": "Zen 4"},
    {"modelo": "AMD Ryzen 9 7950X3D", "tdp": 120, "ano": 2023, "socket": "AM5", "frequencia_base": 4.2, "frequencia_turbo": 5.7, "arquitetura": "Zen 4 (3D)"},
    {"modelo": "Intel Core 2 Duo E8400", "tdp": 65, "ano": 2008, "socket": "LGA775", "frequencia_base": 3.0, "frequencia_turbo": 3.0, "arquitetura": "Core (65nm)"},
    {"modelo": "Intel Core i3-530", "tdp": 73, "ano": 2010, "socket": "LGA1156", "frequencia_base": 2.93, "frequencia_turbo": 3.06, "arquitetura": "Clarksfield"},
    {"modelo": "Intel Core i3-3240", "tdp": 55, "ano": 2012, "socket": "LGA1155", "frequencia_base": 3.4, "frequencia_turbo": 3.4, "arquitetura": "Ivy Bridge"},
    {"modelo": "Intel Core i7-920", "tdp": 130, "ano": 2008, "socket": "LGA1366", "frequencia_base": 2.66, "frequencia_turbo": 2.93, "arquitetura": "Nehalem"},
    {"modelo": "Intel Core i3-6100", "tdp": 51, "ano": 2015, "socket": "LGA1151", "frequencia_base": 3.7, "frequencia_turbo": 3.7, "arquitetura": "Skylake"},
    {"modelo": "Intel Core i5-6600K", "tdp": 91, "ano": 2015, "socket": "LGA1151", "frequencia_base": 3.5, "frequencia_turbo": 3.9, "arquitetura": "Skylake"},
    {"modelo": "Intel Core i5-8400", "tdp": 65, "ano": 2018, "socket": "LGA1151", "frequencia_base": 2.8, "frequencia_turbo": 4.0, "arquitetura": "Coffee Lake"},
    {"modelo": "Intel Core i5-10400F", "tdp": 65, "ano": 2020, "socket": "LGA1200", "frequencia_base": 2.9, "frequencia_turbo": 4.3, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i5-10600K", "tdp": 125, "ano": 2020, "socket": "LGA1200", "frequencia_base": 4.1, "frequencia_turbo": 4.8, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i5-12400F", "tdp": 65, "ano": 2022, "socket": "LGA1700", "frequencia_base": 2.5, "frequencia_turbo": 4.4, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i5-13400F", "tdp": 65, "ano": 2023, "socket": "LGA1700", "frequencia_base": 2.5, "frequencia_turbo": 4.6, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i5-14600K", "tdp": 180, "ano": 2024, "socket": "LGA1700", "frequencia_base": 3.1, "frequencia_turbo": 5.1, "arquitetura": "Raptor Lake Refresh"},
    {"modelo": "Intel Core i7-11700K", "tdp": 125, "ano": 2021, "socket": "LGA1200", "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Rocket Lake"},
    {"modelo": "Intel Core i7-12700K", "tdp": 190, "ano": 2022, "socket": "LGA1700", "frequencia_base": 3.6, "frequencia_turbo": 5.0, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i7-13700K", "tdp": 250, "ano": 2023, "socket": "LGA1700", "frequencia_base": 3.4, "frequencia_turbo": 5.4, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i9-10900K", "tdp": 125, "ano": 2020, "socket": "LGA1200", "frequencia_base": 3.7, "frequencia_turbo": 5.3, "arquitetura": "Comet Lake"},
    {"modelo": "Intel Core i9-12900K", "tdp": 240, "ano": 2022, "socket": "LGA1700", "frequencia_base": 3.2, "frequencia_turbo": 5.2, "arquitetura": "Alder Lake"},
    {"modelo": "Intel Core i9-13900K", "tdp": 250, "ano": 2023, "socket": "LGA1700", "frequencia_base": 3.0, "frequencia_turbo": 5.8, "arquitetura": "Raptor Lake"},
    {"modelo": "Intel Core i9-14900K", "tdp": 250, "ano": 2024, "socket": "LGA1700", "frequencia_base": 3.2, "frequencia_turbo": 6.0, "arquitetura": "Raptor Lake Refresh"},
    {"modelo": "Intel Xeon E5-2666 v3", "tdp": 115, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.9, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2667 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 3.2, "frequencia_turbo": 3.6, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2667 v4", "tdp": 160, "ano": 2016, "socket": "LGA2011-v3", "frequencia_base": 3.2, "frequencia_turbo": 3.7, "arquitetura": "Broadwell-EP"},
    {"modelo": "Intel Xeon E5-2680 v4", "tdp": 120, "ano": 2016, "socket": "LGA2011-v3", "frequencia_base": 2.4, "frequencia_turbo": 3.3, "arquitetura": "Broadwell-EP"},
    {"modelo": "Intel Xeon E5-1660 v3", "tdp": 140, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 3.0, "frequencia_turbo": 3.7, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2680 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.5, "frequencia_turbo": 3.3, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2690 v3", "tdp": 135, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.6, "frequencia_turbo": 3.5, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2670 v3", "tdp": 120, "ano": 2014, "socket": "LGA2011-v3", "frequencia_base": 2.3, "frequencia_turbo": 3.1, "arquitetura": "Haswell-EP"},
    {"modelo": "Intel Xeon E5-2699 v4", "tdp": 145, "ano": 2016, "socket": "LGA2011-v3", "frequencia_base": 2.2, "frequencia_turbo": 3.6, "arquitetura": "Broadwell-EP"},
    {"modelo": "AMD FX-8350", "tdp": 125, "ano": 2012, "socket": "AM3+", "frequencia_base": 4.0, "frequencia_turbo": 4.2, "arquitetura": "Piledriver"},
]

COOLERS = [
    {"modelo": "SuperFrame SuperFlow 450 (Air)", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 25, "durabilidade_anos": 4},
    {"modelo": "Gamdias Boreas E1-410 (Air)", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 28, "durabilidade_anos": 4},
    {"modelo": "TGT Glacier 120 (Air)", "tipo": "Air", "tdp_manufacturer": 100, "ruido_db": 36, "durabilidade_anos": 3},
    {"modelo": "DeepCool Gammaxx 400 (Air)", "tipo": "Air", "tdp_manufacturer": 120, "ruido_db": 38, "durabilidade_anos": 4},
    {"modelo": "Redragon TYR (Air)", "tipo": "Air", "tdp_manufacturer": 130, "ruido_db": 22, "durabilidade_anos": 4},
    {"modelo": "Cooler Master Hyper 212 (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK500S (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Thermalright TRUE Spirit 140 (Air)", "tipo": "Air", "tdp_manufacturer": 200, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Arctic Freezer 34 (Air)", "tipo": "Air", "tdp_manufacturer": 180, "ruido_db": 28, "durabilidade_anos": 5},
    {"modelo": "DeepCool AK400 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 29, "durabilidade_anos": 6},
    {"modelo": "DeepCool Gammaxx AG400 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 4},
    {"modelo": "GameMax Sigma 520 (Air)", "tipo": "Air", "tdp_manufacturer": 220, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Storm 8 (Air)", "tipo": "Air", "tdp_manufacturer": 280, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Be Quiet! Dark Rock Pro 4 (Air)", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 7},
    {"modelo": "Noctua NH-D15 (Air)", "tipo": "Air", "tdp_manufacturer": 250, "ruido_db": 24, "durabilidade_anos": 8},
    {"modelo": "DeepCool AK620 (Air)", "tipo": "Air", "tdp_manufacturer": 260, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Black 240 (Water)", "tipo": "Water", "tdp_manufacturer": 250, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "GameMax IceBurg 240 (Water)", "tipo": "Water", "tdp_manufacturer": 245, "ruido_db": 31, "durabilidade_anos": 6},
    {"modelo": "Corsair H100i (AIO 240) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Arctic Liquid Freezer II 240 (Water)", "tipo": "Water", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "TGT Storm 240 (Water)", "tipo": "Water", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "DeepCool LS720 (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 7},
    {"modelo": "Corsair H150i (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool Castle 360EX (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "Rise Mode Gamer Black 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Pichau AIO 240 (Water)", "tipo": "Water", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Husky Hunter 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Sentinel 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Ventus (Air)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 36, "durabilidade_anos": 4},
    {"modelo": "Redragon TYR (Air)", "tipo": "Air", "tdp_manufacturer": 130, "ruido_db": 22, "durabilidade_anos": 4},
    {"modelo": "DeepCool AK620 (Air)", "tipo": "Air", "tdp_manufacturer": 260, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "DeepCool Castle 360EX (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "Corsair H150i (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280) (Water)", "tipo": "Water", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "DeepCool LS720 (AIO 360) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 7},
    {"modelo": "Arctic Liquid Freezer II 240 (Water)", "tipo": "Water", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "Corsair H100i (AIO 240) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "TGT Storm 240 (Water)", "tipo": "Water", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Pichau AIO 240 (Water)", "tipo": "Water", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Gamer Black 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Husky Hunter 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Rise Mode Sentinel 240 (AIO) (Water)", "tipo": "Water", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Storm 8 (Air) - DUP (entry)", "tipo": "Air", "tdp_manufacturer": 280, "ruido_db": 30, "durabilidade_anos": 5},
    {"modelo": "Cooler Master Hyper 212 (Air) - DUP (entry)", "tipo": "Air", "tdp_manufacturer": 150, "ruido_db": 35, "durabilidade_anos": 5},
]

for c in COOLERS:
    c["tdp_nominal"] = round(0.95 * c.get("tdp_manufacturer", 0.0), 1)

BASE_SAFETY_PCT = 0.10

def avg_frequency(cpu):
    b,t = cpu.get("frequencia_base"), cpu.get("frequencia_turbo")
    return (b+t)/2.0 if b and t else (b or 3.5)

def architecture_factor(cpu):
    a = cpu.get("ano",2018)
    return 0.95 if a>=2022 else (1.00 if a>=2017 else (1.05 if a>=2010 else 1.10))

def compute_adjusted_tdp_for_frequency(cpu):
    base = cpu["tdp"]; f_avg = avg_frequency(cpu); delta = f_avg-3.5
    freq_factor = max(-0.30, min(0.60, 0.16*delta + 0.02*(delta**2)))
    arch = architecture_factor(cpu); diss = 0.97 if cpu.get("ano",0)>=2022 else 1.0
    extra = 1.0 + (0.05*delta if cpu.get("ano",0)<2018 and delta>0 else 0.0)
    adjusted = max(5.0, base * (1.0 + freq_factor*extra) * arch * diss)
    return adjusted, round(freq_factor*100,1), arch

def tdp_scale_multiplier(tdp):
    pts = [(65,1.35),(95,1.22),(105,1.22),(120,1.20)]
    if tdp <= pts[0][0]: return pts[0][1]
    for i in range(len(pts)-1):
        x0,y0 = pts[i]; x1,y1 = pts[i+1]
        if x0 <= tdp <= x1:
            if x1==x0: return y0
            return y0 + (y1-y0)*(tdp-x0)/(x1-x0)
    return pts[-1][1]

def compute_effective_capacity(nominal, cpu_adj, vent=1.0):
    if nominal<=0: return 0.0,0.0,0.0
    nominal_v = nominal*vent
    dynamic_pct = min(0.20, 0.15*(cpu_adj/nominal_v))
    eff = nominal_v*(1-BASE_SAFETY_PCT)*(1-dynamic_pct)
    return eff, round(BASE_SAFETY_PCT*100,1), round(dynamic_pct*100,1)

def estimate_temperature(cpu_adj, cap_eff, ambient=25.0, workload=1.0, f_avg=3.5):
    power = cpu_adj*workload
    if cap_eff<=0: return 120.0
    ratio = power/cap_eff
    K = 55.0 + max(0.0,f_avg-3.5)*10.0
    delta = ratio*(K*0.9) if ratio<=1.0 else (K*0.9)+((ratio-1.0)*(K*2.0))
    return round(ambient + delta,1)

def estimate_noise(cooler, util_pct):
    base = cooler.get("ruido_db",30); scale = sqrt(min(1.0, max(0.0, util_pct/100.0)))
    return round(base*(0.6+0.4*scale),1)

def estimate_durability(cooler, util_pct):
    b = cooler.get("durabilidade_anos",5)
    return b if util_pct<=80 else max(1, int(b*(1.0-0.5*((util_pct-80)/20.0))))

CPUS_sorted = sorted(CPUS, key=lambda x:(x.get("ano",9999), x["modelo"]))
COOLERS_sorted = sorted(COOLERS, key=lambda x: x["tdp_nominal"], reverse=True)

st.title("Simulador de Refrigeração de CPU")
st.markdown("Selecione CPU e cooler e clique em **Simular**.")

with st.expander("Instruções rápidas"):
    st.write("TDP ajustado por frequência+arquitetura; aplicamos fator de escala interpolado (65→+35%, 95/105→+22%, 120→+20%).")

colL,colR = st.columns((2,1))
with colL:
    cpu_choice = st.selectbox("Processador", [c["modelo"] for c in CPUS_sorted])
    cooler_choice = st.selectbox("Cooler", [c["modelo"] for c in COOLERS_sorted])
    ventilacao = st.selectbox("Ventilação do gabinete", ["Bem ventilado 🟢","Moderado 🟡","Pouco ventilado 🔴"])
    ambient = st.number_input("Temperatura ambiente (°C)", 10.0,40.0,25.0,1.0)
    workload = st.slider("Carga (% do TDP)",10,150,100)
    st.caption("Dica: ~80% representa aproximadamente o TDP nominal.")
    show_detailed = st.checkbox("Mostrar gráfico detalhado", True)

    if st.button("Simular"):
        cpu = next(c for c in CPUS_sorted if c["modelo"]==cpu_choice)
        cooler = next(c for c in COOLERS_sorted if c["modelo"]==cooler_choice)
        cpu_adj_no_extra, freq_pct, arch = compute_adjusted_tdp_for_frequency(cpu)
        mult = tdp_scale_multiplier(cpu["tdp"])
        applied_pct = round((mult-1.0)*100,1)
        cpu_adj = cpu_adj_no_extra * mult
        vent_factor = 1.0 if ventilacao.startswith("Bem") else (0.9 if ventilacao.startswith("Moderado") else 0.8)
        nominal = cooler["tdp_nominal"]
        cap_eff, base_pct, dyn_pct = compute_effective_capacity(nominal, cpu_adj, vent_factor)
        power = cpu_adj * (workload/100.0)
        util_pct = round((power/cap_eff)*100.0,1) if cap_eff>0 else 999.9
        temp = estimate_temperature(cpu_adj, cap_eff, ambient, workload/100.0, avg_frequency(cpu))
        noise = estimate_noise(cooler, util_pct)
        dur = estimate_durability(cooler, util_pct)

        st.markdown("### Resultado")
        st.write(f"*CPU:* {cpu['modelo']} — TDP nominal: {cpu['tdp']} W")
        st.write(f"*Frequência média:* {avg_frequency(cpu):.2f} GHz (ajuste freq: {freq_pct}%)")
        st.write(f"*Arquitetura:* {cpu.get('arquitetura','-')} → fator {arch}")
        st.write(f"*TDP ajustado (freq+arch) sem escala:* {cpu_adj_no_extra:.1f} W")
        st.write(f"*Fator de escala interpolado aplicado:* x{mult:.3f} (+{applied_pct}%)")
        st.write(f"*TDP usado no cálculo:* {cpu_adj:.1f} W")
        st.write(f"*Cooler:* {cooler['modelo']} ({cooler['tipo']}) — Nominal ajustado (95%): {nominal} W")
        if "tdp_manufacturer" in cooler: st.write(f"*Especificação fabricante:* {cooler['tdp_manufacturer']} W")
        st.write(f"*Condição do gabinete:* {ventilacao} (fator {vent_factor})")
        st.write(f"*Capacidade efetiva aplicada:* {cap_eff:.1f} W (redução base {base_pct}% + dinâmica {dyn_pct}%)")
        st.write(f"*Carga aplicada:* {workload}% → potência gerada: {power:.1f} W")
        st.write(f"*Utilização da capacidade efetiva:* {util_pct}%")
        st.write(f"*Temperatura estimada (IHS):* {temp} °C (ambiente {ambient} °C)")
        st.write(f"*Ruído estimado:* {noise} dB")
        st.write(f"*Durabilidade estimada:* ~{dur} anos")

        if util_pct <= 70: st.success("Sistema seguro: cooler com folga adequada.")
        elif util_pct <= 90: st.info("Sistema adequado: operação dentro dos limites.")
        else: st.error("Risco: capacidade efetiva do cooler pode ser insuficiente.")

        if show_detailed:
            loads = np.linspace(10,150,80)
            temps = [estimate_temperature(cpu_adj, cap_eff, ambient, l/100.0, avg_frequency(cpu)) for l in loads]
            fig,ax = plt.subplots(figsize=(10,4))
            ax.plot(loads,temps,linewidth=2,label="Temperatura (°C)")
            ax.scatter([workload],[temp],zorder=6)
            ax.axvline(workload, color='gray', linestyle=':', linewidth=1)
            ax.set_xlabel("Carga (% do TDP)"); ax.set_ylabel("Temperatura (°C)"); ax.grid(True,linestyle='--',alpha=0.6)
            st.pyplot(fig)

        fig2,ax2 = plt.subplots(figsize=(6,3))
        ax2.bar(["TDP efetivo (W)","Capacidade Efetiva (W)"], [power, cap_eff], color=["#2f72b7","#7f8fa6"])
        ax2.set_ylabel("Potência (W)"); ax2.set_ylim(0, max(cap_eff,power)+20)
        for i,val in enumerate([power,cap_eff]): ax2.text(i, val+max(1,0.02*val), f"{val:.1f}", ha='center', fontsize=10)
        st.pyplot(fig2)

with colR:
    st.subheader("Detalhes rápidos")
    sel = st.selectbox("Visualizar cooler", [c["modelo"] for c in COOLERS_sorted])
    cinfo = next(c for c in COOLERS_sorted if c["modelo"]==sel)
    st.write(f"Modelo: {cinfo['modelo']}")
    st.write(f"Tipo: {cinfo['tipo']}")
    st.write(f"Nominal (ajustado): {cinfo['tdp_nominal']} W")
    if "tdp_manufacturer" in cinfo: st.write(f"Especificação: {cinfo['tdp_manufacturer']} W")
    sample_adj,_,_ = compute_adjusted_tdp_for_frequency({"tdp":95,"frequencia_base":3.5,"frequencia_turbo":3.5,"ano":2018})
    eff,bp,dp = compute_effective_capacity(cinfo['tdp_nominal'], sample_adj, 1.0)
    st.write(f"Capacidade efetiva (ex.: CPU 95W): {eff:.1f} W")
    st.write(f"Ruído (médio): {cinfo['ruido_db']} dB")
    st.write(f"Durabilidade (estimada): {cinfo['durabilidade_anos']} anos")

st.markdown("---")
st.caption("Versão compacta — todos os CPUs e coolers preservados; fator de TDP interpolado aplicado.")
