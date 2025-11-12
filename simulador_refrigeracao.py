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
# - tdp_nominal: valor efetivo usado no simulador = 0.85 * tdp_manufacturer,
#   aplicando a redução prática de eficiência (agora 85% do valor declarado).
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

    # Intel mainstream (mantidos e alguns corrigidos/estimados)
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
    {"modelo": "Intel Xeon E5-2650 v3", "tdp": 105, "ano": 2014, "socket": "LGA2011-v3"},

    # --- NOVOS (adicionados conforme pedido) ---
    {"modelo": "AMD Ryzen 5 5500", "tdp": 65, "ano": 2022, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 1600X", "tdp": 95, "ano": 2017, "socket": "AM4"},
    {"modelo": "AMD Ryzen 7 1700", "tdp": 65, "ano": 2017, "socket": "AM4"},
    {"modelo": "AMD Ryzen 5 3600", "tdp": 65, "ano": 2019, "socket": "AM4"},
    {"modelo": "AMD Ryzen 7 9800X3D", "tdp": 120, "ano": 2024, "socket": "AM5"},
    {"modelo": "AMD Ryzen 9 9950X3D", "tdp": 170, "ano": 2025, "socket": "AM5"},
    {"modelo": "Intel Core Ultra 5 245KF", "tdp": 125, "ano": 2024, "socket": "LGA1851"},
    {"modelo": "Intel Core Ultra 7 265K", "tdp": 125, "ano": 2024, "socket": "LGA1851"},
]

# Coolers: adicionei vários e incluí tdp_manufacturer + tdp_nominal (ajustado -15% agora)
COOLERS = [
    # manufacturer TDP listed (tdp_manufacturer) -> tdp_nominal = 0.85 * tdp_manufacturer
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
    # novos air coolers pedidos
    {"modelo": "Redragon TYR (Redragon Tyr)", "tipo": "Air", "tdp_manufacturer": 130, "ruido_db": 22, "durabilidade_anos": 4},
    {"modelo": "Thermalright Phantom Spirit 120", "tipo": "Air", "tdp_manufacturer": 234, "ruido_db": 26, "durabilidade_anos": 6},  # teste e review apontam ~234W em testes
    {"modelo": "SuperFrame SuperFlow 450", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 25, "durabilidade_anos": 4},
    {"modelo": "Gamdias Boreas E1-410", "tipo": "Air", "tdp_manufacturer": 95, "ruido_db": 28, "durabilidade_anos": 4},
    {"modelo": "Thermalright Assassin (Peerless/Assassin)", "tipo": "Air", "tdp_manufacturer": 225, "ruido_db": 26, "durabilidade_anos": 6},

    # AIO / Water coolers (manufacturer spec) - novos inclusive
    {"modelo": "Corsair H100i (AIO 240)", "tipo": "AIO", "tdp_manufacturer": 300, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "Corsair H150i (AIO 360)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "NZXT Kraken X63 (AIO 280)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 29, "durabilidade_anos": 7},
    {"modelo": "Arctic Liquid Freezer II 240", "tipo": "AIO", "tdp_manufacturer": 320, "ruido_db": 27, "durabilidade_anos": 7},
    {"modelo": "DeepCool LS720 (AIO 360)", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 30, "durabilidade_anos": 7},
    {"modelo": "Rise Mode Sentinel 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 300, "ruido_db": 32, "durabilidade_anos": 6},
    {"modelo": "Rise Mode Gamer Black 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 220, "ruido_db": 28, "durabilidade_anos": 6},
    {"modelo": "TGT 120mm AIO (TGT Spartel / TGT 120)", "tipo": "AIO", "tdp_manufacturer": 200, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "TGT Storm 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 280, "ruido_db": 33, "durabilidade_anos": 5},
    {"modelo": "Pichau AIO 240", "tipo": "AIO", "tdp_manufacturer": 270, "ruido_db": 34, "durabilidade_anos": 5},
    {"modelo": "DeepCool Castle 360EX", "tipo": "AIO", "tdp_manufacturer": 350, "ruido_db": 31, "durabilidade_anos": 7},
    {"modelo": "Husky Hunter 240 (AIO)", "tipo": "AIO", "tdp_manufacturer": 260, "ruido_db": 33, "durabilidade_anos": 5},
]

# aplicar ajuste de eficiência: criar campo tdp_nominal = 0.85 * tdp_manufacturer
for c in COOLERS:
    if "tdp_manufacturer" in c and c.get("tdp_manufacturer") is not None:
        c["tdp_nominal"] = round(0.85 * c["tdp_manufacturer"], 1)
    else:
        # fallback para compatibilidade com o código anterior
        c["tdp_nominal"] = c.get("tdp_nominal", 0)

# Safety configuration (base safety reduction applied to all coolers)
BASE_SAFETY_PCT = 0.10  # alterado para 10% conforme solicitado

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
       dinâmica = min(0
