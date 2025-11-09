# app.py
import io
import csv
import streamlit as st

st.set_page_config(page_title="Fujifilm Recipes", page_icon="🎞️", layout="centered")
st.title("Fujifilm Recipes")

# ========= DICCIONARIOS (tus datos) =========

film = {
    "Film Simulation": {
        1: "Provia", 2: "Velvia", 3: "Astia", 4: "Classic Chrome",
        5: "Pro Neg Hi", 6: "Pro Neg Std", 7: "Classic Neg",
        8: "Nostalgic Neg", 9: "Eterna", 10: "Eterna Bleach Bypass",
        11: "Reala Ace", 12: "Monochrome",
        13: "Monochrome + Y Filter", 14: "Monochrome + R Filter",
        15: "Monochrome + G Filter", 16: "Acros",
        17: "Acros + Y Filter", 18: "Acros + R Filter", 19: "Acros + G Filter",
    }
}

grain = {
    "Grain Level": {
        1: "Off", 2: "Weak - Small", 3: "Weak - Large",
        4: "Strong - Small", 5: "Strong - Large"
    }
}

chrome = {
    "Color Chrome": {1: "Off", 2: "Weak", 3: "Strong"}
}

blue = {
    "Blue Chrome": {1: "Off", 2: "Weak", 3: "Strong"}
}

white = {
    "White Balance": {
        1: "White Priority", 2: "Auto", 3: "Ambience Priority",
        4: "Kelvin", 5: "Daylight", 6: "Tungsten"
    }
}

dynamic = {"Dynamic Range": {1: "DR 100", 2: "DR 200", 3: "DR 400"}}

# lista -4 ... +4 con pasos de 0.5
high = {
    "Highlight": {i: v for i, v in enumerate(
        ["-4", "-3.5", "-3", "-2.5", "-2", "-1.5", "-1", "-0.5",
         "0", "+0.5", "+1", "+1.5", "+2", "+2.5", "+3", "+3.5", "+4"], 1)}
}
shadow = {"Shadow": high["Highlight"]}

sharp = {"Sharpness": {1: "+4", 2: "+3", 3: "+2", 4: "+1", 5: "0", 6: "-1", 7: "-2", 8: "-3", 9: "-4"}}
iso_nr = {"High ISO NR": {1: "+4", 2: "+3", 3: "+2", 4: "+1", 5: "0", 6: "-1", 7: "-2", 8: "-3", 9: "-4"}}
clarity = {"Clarity": {1: "+4", 2: "+3", 3: "+2", 4: "+1", 5: "0", 6: "-1", 7: "-2", 8: "-3", 9: "-4"}}
iso = {"ISO": {1: "Manual", 2: "Auto"}}

# ========= HELPERS =========

def opciones(d: dict, key: str):
    """Devuelve (indices, etiquetas, inverso) para usar en selectbox."""
    inner = d[key]
    idxs = list(inner.keys())
    labels = [inner[i] for i in idxs]
    inv = {v: k for k, v in inner.items()}
    return idxs, labels, inv

def csv_de_receta(dic):
    """Devuelve un CSV (str) con una sola fila (la receta)."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(dic.keys()))
    writer.writeheader()
    writer.writerow(dic)
    return buffer.getvalue()

st.write("---")

# ========= NOMBRE DEL PRESET =========
st.subheader("Preset Name")
preset_name = st.text_input("Escribe el nombre de tu preset", value="Mi receta")
st.write("---")

# ========= FILM SIMULATION =========
st.header("Film Simulation")
_, film_labels, _ = opciones(film, "Film Simulation")
fs_elegido = st.selectbox("Film Simulation", film_labels, index=0)
st.write("---")

# ========= COLOR CHROME (PESTAÑAS) =========
st.header("Color Chrome")
tab_cc, tab_ccb = st.tabs(["Color Chrome", "Color Chrome Blue"])
with tab_cc:
    _, cc_labels, _ = opciones(chrome, "Color Chrome")
    cc_elegido = st.selectbox("Color Chrome FX", cc_labels, index=0, key="cc_sel")
with tab_ccb:
    _, cb_labels, _ = opciones(blue, "Blue Chrome")
    cb_elegido = st.selectbox("Color Chrome Blue", cb_labels, index=0, key="ccb_sel")
st.write("---")

# ========= WHITE BALANCE =========
st.header("White Balance")
_, wb_labels, _ = opciones(white, "White Balance")
wb_elegido = st.selectbox("White Balance", wb_labels, index=1)

wb_texto = wb_elegido
if wb_elegido == "Kelvin":
    kelvin = st.number_input("Kelvin (2500–10000)", min_value=2500, max_value=10000, step=100, value=5600)
    col_wb1, col_wb2 = st.columns(2)
    with col_wb1:
        red_offset = st.number_input("Red offset (-4 a +4)", min_value=-4, max_value=4, value=0, step=1)
    with col_wb2:
        blue_offset = st.number_input("Blue offset (-4 a +4)", min_value=-4, max_value=4, value=0, step=1)
    wb_texto = f"{kelvin}K, {red_offset:+} Red, {blue_offset:+} Blue"
st.write("---")

# ========= DETAIL =========
st.header("Detail")
col_d1, col_d2 = st.columns(2)
with col_d1:
    _, sh_labels, _ = opciones(sharp, "Sharpness")
    sh_elegido = st.selectbox("Sharpness", sh_labels, index=4)
    _, cl_labels, _ = opciones(clarity, "Clarity")
    cl_elegido = st.selectbox("Clarity", cl_labels, index=4)
    _, gl_labels, _ = opciones(grain, "Grain Level")
    gl_elegido = st.selectbox("Grain Level", gl_labels, index=0)
with col_d2:
    _, hl_labels, _ = opciones(high, "Highlight")
    hl_elegido = st.selectbox("Highlight", hl_labels, index=9)
    _, sd_labels, _ = opciones(shadow, "Shadow")
    sd_elegido = st.selectbox("Shadow", sd_labels, index=9)
st.write("---")

# ========= ISO + DR + HIGH ISO NR =========
st.header("ISO Settings")
col_iso1, col_iso2, col_iso3 = st.columns(3)
with col_iso1:
    _, iso_labels, _ = opciones(iso, "ISO")
    iso_elegido = st.selectbox("ISO Type", iso_labels, index=1)
with col_iso2:
    _, dr_labels, _ = opciones(dynamic, "Dynamic Range")
    dr_elegido = st.selectbox("Dynamic Range", dr_labels, index=0)
with col_iso3:
    _, nr_labels, _ = opciones(iso_nr, "High ISO NR")
    iso_nr_elegido = st.selectbox("High ISO NR", nr_labels, index=4)
st.write("---")

# ========= RESUMEN =========
st.header("Summary")
resumen = {
    "Preset Name": preset_name,
    "Film Simulation": fs_elegido,
    "Color Chrome": cc_elegido,
    "Color Chrome Blue": cb_elegido,
    "White Balance": wb_texto,
    "Grain Level": gl_elegido,
    "Highlight": hl_elegido,
    "Shadow": sd_elegido,
    "Sharpness": sh_elegido,
    "Clarity": cl_elegido,
    "ISO": iso_elegido,
    "Dynamic Range": dr_elegido,
    "High ISO NR": iso_nr_elegido,
}

st.table({"Ajuste": list(resumen.keys()), "Valor": list(resumen.values())})

st.subheader("Download Preset")

# CSV
csv_data = csv_de_receta(resumen)
st.download_button(
    label="📄 Download as CSV",
    data=csv_data.encode("utf-8"),
    file_name=f"{preset_name.replace(' ', '_')}.csv",
    mime="text/csv",
)

# TXT
def resumen_a_txt(res):
    return "\n".join(f"{k}: {v}" for k, v in res.items())

txt_bytes = io.BytesIO(resumen_a_txt(resumen).encode("utf-8"))
st.download_button(
    label="🗒️ Download as TXT",
    data=txt_bytes,
    file_name=f"{preset_name.replace(' ', '_')}.txt",
    mime="text/plain",
)
