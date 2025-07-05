import streamlit as st

# header
st.title("🦠 Infection Dilution Calculator")

# define functions
def calculate_cfu(od):
    return od * 1.5e9

def calculate_required_volume(cfu_start, cfu_target, total_volume_ml=50):
    return (cfu_target * total_volume_ml) / cfu_start  # in mL

# prompt user to enter OD reading
od = st.number_input("To calculate appropriate volumes to use for dilutions, enter OD reading:", min_value=0.0, step=0.01, format="%.2f")

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
    aliquot_ul = st.number_input("Enter the actual aliquot volume used (in µL):", min_value=0.0, step=1.0)
    aliquot_ml = aliquot_ul / 1000  # convert to ml

    if aliquot_ul > 0:
        # calculate the amount of FSSW to use based on aliquot amount
        fssw_intermediate = 50000 - aliquot_ul

         # calculate expected CFU/mL in intermediate dilution
        cfu_intermediate = (cfu_start * aliquot_ml) / total_volume_ml

        st.write(f"If you are using {aliquot_ul:.0f} µL culture, you should add **{fssw_intermediate:.0f} µL FSSW**. The intermediate dilution is expected to have a concentration of **{cfu_intermediate:.2e} CFU/mL**.")  # 0f means integer notation; 2e means scientific notation

        # calculate CFU/mL after aliquoting 50 µL of intermediate dilution into 49.95 mL FSSW
        cfu_final = cfu_intermediate / 1000
        st.write(f"Dilute **50 µL** of the intermediate into **49950 µL FSSW** to obtain 50 mL of a final dilution with a concentration of **{cfu_final:.2e} CFU/mL**.")

        # calculate expected colony count if plated 50 µL
        colonies_expected = cfu_final * 50 / 1000  # convert 50 µL to mL
        st.write(f"If you plate **50 µL** of the final dilution, there should be an expected **{colonies_expected:.0f} colonies**.")

        # save info on how much user used for aliquot to use again later in cell 2
        st.session_state["stored_aliquot_ul"] = aliquot_ul

# prompt user for actual colony count
observed_colonies = st.number_input("To backcalculate dilution concentrations, enter the actual number of colonies you observed on the plate:", min_value=0.0, step=1.0)

# make sure the aliquot from earlier exists
if "stored_aliquot_ul" in st.session_state and observed_colonies > 0:

    stored_aliquot_ul = st.session_state["stored_aliquot_ul"]
    total_volume_ml = 50  # same as in cell 1

    actual_initial_culture = (1e9 * observed_colonies) / stored_aliquot_ul
    actual_final_dilution = (1e3 * observed_colonies) / total_volume_ml

    st.write(f"Based on the colony count, the initial culture had a concentration of approximately **{actual_initial_culture:.2e} CFU/mL**.")
    st.write(f"Based on the colony count, the final dilution had a concentration of approximately **{actual_final_dilution:.2e} CFU/mL**.")

elif observed_colonies > 0:
    st.warning("Enter the aliquot volume you used.")
