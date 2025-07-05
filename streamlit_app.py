import streamlit as st

# define dark vs light mode settings
dark_mode_css = """
<style>
body, .stApp {
    background-color: #0E1117 !important;
    color: #FAFAFA !important;
}
input, textarea, select, button {
    background-color: #222 !important;
    color: #FAFAFA !important;
    border-color: #555 !important;
}
input::placeholder, textarea::placeholder {
    color: #AAA !important;
}
label, .css-1v3fvcr {
    color: #FAFAFA !important;
}

/* Dark mode checkbox label */
label[for="dark_mode_toggle"] {
  color: #FAFAFA !important;
}
</style>
"""

light_mode_css = """
<style>
body, .stApp {
    background-color: white !important;
    color: black !important;
}
input, textarea, select, button {
    background-color: white !important;
    color: black !important;
    border-color: #DDD !important;
}
input::placeholder, textarea::placeholder {
    color: #555 !important;
}
label, .css-1v3fvcr {
    color: black !important;
}

/* Light mode checkbox label */
label[for="dark_mode_toggle"] {
  color: black !important;
}
</style>
"""

# header
st.title("🦠 Infection Dilution Calculator")

# define functions
def calculate_cfu(od):
    return od * 1.5e9

def calculate_required_volume(cfu_start, cfu_target, total_volume_ml=50):
    return (cfu_target * total_volume_ml) / cfu_start  # in mL

# prompt user to enter OD reading
od = st.number_input(
    "To calculate appropriate volumes to use for dilutions, enter OD reading:",
    min_value=0.0,
    step=0.0001,
    format="%.5f" # 5f = more decimal places for OD reading
    value=None   
)

if od > 0:
    # calculate CFU/mL in initial culture
    cfu_start = calculate_cfu(od)
    st.write(f"Your initial culture contains approximately **{cfu_start:.2e} CFU/mL** *V. fischeri*.")

    # calculate aliquot range to reach 3e6–5e6 CFU/mL in 50 mL
    min_cfu = 3e6
    max_cfu = 5e6
    total_volume_ml = 50

    min_vol_ul = calculate_required_volume(cfu_start, min_cfu) * 1000  # convert to uL
    max_vol_ul = calculate_required_volume(cfu_start, max_cfu) * 1000  # convert to uL

    st.write(f"To make an intermediate dilution of 3.0e6 to 5.0e6 CFU/mL in 50 mL, you can use **between {min_vol_ul:.1f} µL and {max_vol_ul:.1f} µL** of culture.")

    # prompt user to enter aliquot volume they chose
    aliquot_ul = st.number_input(
        "Enter the actual aliquot volume used (in µL):",
        min_value=0.0,
        step=1.0,
        format="%.0f" # 0f format to allow only whole integers w/o decimals
        value=None
    )
    aliquot_ml = aliquot_ul / 1000  # convert to ml

    if aliquot_ul > 0:
        # calculate the amount of FSSW to use based on aliquot amount
        fssw_intermediate = 50000 - aliquot_ul

         # calculate expected CFU/mL in intermediate dilution
        cfu_intermediate = (cfu_start * aliquot_ml) / total_volume_ml

        st.write(f"If you are using {aliquot_ul:.0f} µL culture, you should add **{fssw_intermediate:.0f} µL FSSW**. The intermediate dilution is expected to have a concentration of **{cfu_intermediate:.2e} CFU/mL**.")  # 0f = integer notation; 2e = scientific notation

        # calculate CFU/mL after aliquoting 50 µL of intermediate dilution into 49.95 mL FSSW
        cfu_final = cfu_intermediate / 1000
        st.write(f"Dilute **50 µL** of the intermediate into **49950 µL FSSW** to obtain 50 mL of a final dilution with a concentration of **{cfu_final:.2e} CFU/mL**.")

        # calculate expected colony count if plated 50 µL
        colonies_expected = cfu_final * 50 / 1000  # convert 50 µL to mL
        st.write(f"If you plate **50 µL** of the final dilution, there should be an expected **{colonies_expected:.0f} colonies**.")

        # save info on how much user used for aliquot to use again later in cell 2
        st.session_state["stored_aliquot_ul"] = aliquot_ul

# prompt user for actual colony count
observed_colonies = st.number_input(
    "To backcalculate dilution concentrations, enter the actual number of colonies you observed on the plate:",
    min_value=0.0,
    step=1.0,
    format="%.0f"
    value=None    
)

# get aliquot volume from earlier section if available
aliquot_ul = st.session_state.get("stored_aliquot_ul", None)

if observed_colonies > 0:
    if aliquot_ul is None:
        # Prompt user to manually enter aliquot if it wasn't stored
        aliquot_ul = st.number_input(
            "Enter the volume of initial culture you used to create the 50 mL intermediate dilution (in µL):",
            min_value=0.0,
            step=1.0,
            format="%.0f"
            value=None            
            key="manual_aliquot_input"
        )

    if aliquot_ul > 0:
        total_volume_ml = 50  # same as earlier

        actual_initial_culture = (1e9 * observed_colonies) / aliquot_ul
        actual_final_dilution = (1e3 * observed_colonies) / total_volume_ml

        st.write(f"Based on the colony count, the initial culture had a concentration of approximately **{actual_initial_culture:.2e} CFU/mL**.")
        st.write(f"Based on the colony count, the final dilution had a concentration of approximately **{actual_final_dilution:.2e} CFU/mL**.")
    
# dark mode toggle
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-top:10px;">', unsafe_allow_html=True)

dark_mode = st.checkbox("🌙", value=False, key="dark_mode_toggle")

if dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
