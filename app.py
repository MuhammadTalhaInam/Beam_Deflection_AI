
import os
import streamlit as st
import matplotlib.pyplot as plt

from groq import Groq

import workflow
import prompts


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Interactive Beam Calculator",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏗️ Interactive Beam Deflection & Stress Calculator")

st.markdown(
    """
    Analyze the behavior of a simply supported rectangular beam
    under different loading conditions.

    **Calculate:** Bending Moment • Bending Stress • Deflection • Factor of Safety
    """
)

st.info(
    "🔧 Python performs the engineering calculations. "
    "🤖 Groq AI provides an educational explanation of the calculated results."
)


# ============================================================
# SIDEBAR — INPUTS
# ============================================================

st.sidebar.header("Beam Inputs")

material_name = st.sidebar.selectbox(
    "Material",
    list(workflow.MATERIALS.keys())
)

load_type = st.sidebar.selectbox(
    "Load Type",
    [
        "Center Point Load",
        "Full-Span UDL"
    ]
)

st.sidebar.subheader("Beam Dimensions")

L = st.sidebar.number_input(
    "Beam Length (m)",
    min_value=0.01,
    value=2.0,
    step=0.1
)

width = st.sidebar.number_input(
    "Beam Width (m)",
    min_value=0.001,
    value=0.05,
    step=0.01
)

height = st.sidebar.number_input(
    "Beam Height (m)",
    min_value=0.001,
    value=0.10,
    step=0.01
)


# ============================================================
# LOAD INPUT
# ============================================================

st.sidebar.subheader("Loading")

if load_type == "Center Point Load":

    load = st.sidebar.number_input(
        "Point Load (N)",
        min_value=0.01,
        value=1000.0,
        step=100.0
    )

else:

    load = st.sidebar.number_input(
        "UDL (N/m)",
        min_value=0.01,
        value=1000.0,
        step=100.0
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.sidebar.button(
    "🔍 Analyze Beam",
    type="primary"
)


# ============================================================
# MAIN ANALYSIS
# ============================================================

if analyze:

    try:

        # ----------------------------------------------------
        # Run engineering calculations
        # ----------------------------------------------------

        results = workflow.run_beam_analysis(
            material_name=material_name,
            load_type=load_type,
            L=L,
            width=width,
            height=height,
            load=load
        )


        # ----------------------------------------------------
        # Display success message
        # ----------------------------------------------------

        st.success("Beam analysis completed successfully!")


        # ====================================================
        # RESULTS
        # ====================================================

       st.header("📊 Engineering Results")

# ====================================================
# STRUCTURAL RESULTS
# ====================================================

st.subheader("⚙️ Structural Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Maximum Moment",
        f"{results['maximum_moment']:.2f} N·m"
    )

with col2:
    st.metric(
        "Maximum Stress",
        f"{results['maximum_stress'] / 1e6:.2f} MPa"
    )

with col3:
    st.metric(
        "Maximum Deflection",
        f"{results['maximum_deflection'] * 1000:.4f} mm"
    )


# ====================================================
# SAFETY RESULTS
# ====================================================

st.subheader("🛡️ Safety")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Yield Strength",
        f"{results['yield_strength'] / 1e6:.2f} MPa"
    )

with col2:
    st.metric(
        "Factor of Safety",
        f"{results['factor_of_safety']:.2f}"
    )


        # ====================================================
        # ADDITIONAL INFORMATION
        # ====================================================

        st.subheader("Beam Information")

        info_col1, info_col2 = st.columns(2)

        with info_col1:

            st.write(f"**Material:** {material_name}")
            st.write(f"**Load Type:** {load_type}")
            st.write(f"**Beam Length:** {L:.3f} m")


        with info_col2:

            st.write(f"**Width:** {width:.3f} m")
            st.write(f"**Height:** {height:.3f} m")

            if load_type == "Center Point Load":
                st.write(f"**Point Load:** {load:.2f} N")
            else:
                st.write(f"**UDL:** {load:.2f} N/m")


        # ====================================================
        # DIAGRAMS
        # ====================================================

        st.header("📈 Beam Diagrams")


        x = results["x"]

        shear_force = results["shear_force"]

        bending_moment = results["bending_moment"]

        deflection = results["deflection"]


        # ----------------------------------------------------
        # SFD
        # ----------------------------------------------------

        st.subheader("Shear Force Diagram (SFD)")

        fig_sfd, ax_sfd = plt.subplots()

        ax_sfd.plot(
            x,
            shear_force,
            linewidth=2
        )

        ax_sfd.axhline(
            0,
            linewidth=1
        )

        ax_sfd.set_xlabel("Beam Position (m)")

        ax_sfd.set_ylabel("Shear Force (N)")

        ax_sfd.set_title("Shear Force Diagram")

        ax_sfd.grid(True)

        st.pyplot(fig_sfd)

        plt.close(fig_sfd)


        # ----------------------------------------------------
        # BMD
        # ----------------------------------------------------

        st.subheader("Bending Moment Diagram (BMD)")

        fig_bmd, ax_bmd = plt.subplots()

        ax_bmd.plot(
            x,
            bending_moment,
            linewidth=2
        )

        ax_bmd.axhline(
            0,
            linewidth=1
        )

        ax_bmd.set_xlabel("Beam Position (m)")

        ax_bmd.set_ylabel("Bending Moment (N·m)")

        ax_bmd.set_title("Bending Moment Diagram")

        ax_bmd.grid(True)

        st.pyplot(fig_bmd)

        plt.close(fig_bmd)


        # ----------------------------------------------------
        # DEFLECTION
        # ----------------------------------------------------

        st.subheader("Deflection Curve")

        fig_def, ax_def = plt.subplots()

        ax_def.plot(
            x,
            deflection * 1000,
            linewidth=2
        )

        ax_def.axhline(
            0,
            linewidth=1
        )

        ax_def.set_xlabel("Beam Position (m)")

        ax_def.set_ylabel("Deflection (mm)")

        ax_def.set_title("Beam Deflection Curve")

        ax_def.grid(True)

        st.pyplot(fig_def)

        plt.close(fig_def)


        # ====================================================
        # AI EXPLANATION
        # ====================================================

        st.header("🤖 AI Engineering Explanation")


        api_key = os.environ.get("GROQ_API_KEY")


        if not api_key:

            st.warning(
                "Groq API key was not found. "
                "The engineering calculations are still available."
            )

        else:

            try:

                client = Groq(
                    api_key=api_key
                )


                engineering_prompt = (
                    prompts.build_engineering_prompt(results)
                )


                response = client.chat.completions.create(

                    messages=[

                        {
                            "role": "system",
                            "content": prompts.SYSTEM_PROMPT
                        },

                        {
                            "role": "user",
                            "content": engineering_prompt
                        }

                    ],

                    model="openai/gpt-oss-120b"
                )


                ai_explanation = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                st.markdown(ai_explanation)


            except Exception as e:

                st.error(
                    f"Groq AI error: {e}"
                )


    except Exception as e:

        st.error(
            f"Beam analysis error: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Interactive Beam Deflection & Stress Calculator | "
    "Python + Streamlit + Groq AI"
)
