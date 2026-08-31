
import streamlit as st
from seismic_score import (
    classify_permeability, classify_pathways, classify_roughness,
    classify_size, classify_continuity, classify_stress,
    classify_proximity, classify_caprock,
    risk_score, d_value
)

st.title("CO₂ Storage – Induced Seismicity Risk Screener")
st.caption("Pre-injection geological screening · 8 parameters · literature-derived thresholds")

def parameter_input(name, weight, key, classifier, unit=None, options=None):
    """Render one parameter block. Pass `unit` for numeric inputs,
        `options` for categorical ones."""
    st.subheader(name)
    mode = st.radio(
        "Input mode",
        ["Enter data","Choose risk level","Unknown"]
    )

    if mode == "Eneter data":
        if unit:
            value = st.number_input(f"{name} ({unit})", key=key + "_val")
            level = classifier(value)
        else:
            answer = st.selectbox("Select", options, key=key + "_ans")
            level = classifier(answer)
    elif mode == "Choose risk level":
        level = st.selectbox("Risk level", ["high", "moderate", "low"], key=key + "_lvl")
    else:
        level = "na"

    st.caption(f"→ {level}")
    return (name,weight,level)

entries = [
    parameter_input("Fault permeability", 2, "perm", classify_permeability, unit="mD"),
    parameter_input("Fluid pathways", 2, "path", classify_pathways, options=["yes", "no"]),
    parameter_input("Fault roughness", 1, "rough", classify_roughness, options=["rough", "smooth"]),
    parameter_input("Fault size / length", 2, "size", classify_size, unit="m"),
    parameter_input("Fault continuity", 2, "cont", classify_continuity, options=["continuous", "heterogeneous"]),
    parameter_input("Stress state", 2, "stress", classify_stress, unit="µmob"),
    parameter_input("Proximity to basement", 2, "prox", classify_proximity, unit="km"),
    parameter_input("Caprock integrity", 1, "cap", classify_caprock, unit="m"),
]

st.divider()
st.header("Result")

simple = []
for name, weight, level in entries:
    simple.append((weight, level))
score = risk_score(simple)

if score is None:
    st.warning("No data entered _ cannot calculate a risk score.")
else:
    st.metric("Risk Score", f"{round(score, 2)} %")

    st.subheader("Parameter breakdown")
    for name, weight, level in entries:
        if level == "na":
            st.write(f"**{name}** – no data")
        else:
            contribution = weight * d_value(level)
            st.write(f"**{name}** –{level} · {contribution}/{weight}")
