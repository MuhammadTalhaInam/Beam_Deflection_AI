
import os
import streamlit as st
import matplotlib.pyplot as plt

from groq import Groq

import workflow
import prompts
# ====================================================
# GROQ AI CLIENT
# ====================================================

groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

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


# ====================================================
# SIDEBAR INPUTS
# ====================================================

st.sidebar.header("⚙️ Beam Inputs")

# ====================================================
# BEAM GEOMETRY
# ====================================================

st.sidebar.subheader("📐 Beam Geometry")

L = st.sidebar.number_input(
    "Beam Length (m)",
    min_value=0.1,
    value=2.0,
    step=0.1
)

width = st.sidebar.number_input(
    "Beam Width (m)",
    min_value=0.001,
    value=0.05,
    step=0.005
)

height = st.sidebar.number_input(
    "Beam Height (m)",
    min_value=0.001,
    value=0.10,
    step=0.005
)

# ====================================================
# MATERIAL
# ====================================================

st.sidebar.subheader("🔩 Material")

material_name = st.sidebar.selectbox(
    "Select Material",
    [
        "Structural Steel",
        "Aluminum 6061-T6",
        "Stainless Steel 304"
    ]
)

# ====================================================
# LOADING
# ====================================================

st.sidebar.subheader("⚖️ Loading")

load_type = st.sidebar.selectbox(
    "Select Load Type",
    [
        "Center Point Load",
        "Full-Span UDL"
    ]
)

if load_type == "Center Point Load":

    load = st.sidebar.number_input(
        "Point Load (N)",
        min_value=1.0,
        value=1000.0,
        step=100.0
    )

else:

    load = st.sidebar.number_input(
        "Uniform Load (N/m)",
        min_value=1.0,
        value=1000.0,
        step=100.0
    )

# ====================================================
# ANALYZE BUTTON
# ====================================================

st.sidebar.divider()

analyze = st.sidebar.button(
    "🔍 Analyze Beam",
    use_container_width=True
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
        # BEAM INFORMATION
        # ====================================================

        st.subheader("📐 Beam Information")

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.write(f"**Material**")
            st.write(material_name)

        with info_col2:
            st.write(f"**Load Type**")
            st.write(load_type)

        with info_col3:
            st.write(f"**Beam Length**")
            st.write(f"{L:.3f} m")

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.write(f"**Width**")
            st.write(f"{width:.3f} m")

        with info_col2:
            st.write(f"**Height**")
            st.write(f"{height:.3f} m")

        with info_col3:
            if load_type == "Center Point Load":
                st.write("**Point Load**")
                st.write(f"{load:.2f} N")
            else:
                st.write("**UDL**")
                st.write(f"{load:.2f} N/m")


              # ====================================================
        # DIAGRAMS
        # ====================================================

        st.header("📈 Beam Diagrams")

        x = results["x"]
        shear_force = results["shear_force"]
        bending_moment = results["bending_moment"]
        deflection = results["deflection"]

        # ====================================================
        # SHEAR FORCE DIAGRAM
        # ====================================================

        st.subheader("Shear Force Diagram (SFD)")

        fig_sfd, ax_sfd = plt.subplots(figsize=(9, 4))

        ax_sfd.plot(
            x,
            shear_force,
            linewidth=2.5
        )

        ax_sfd.axhline(
            0,
            linewidth=1
        )

        ax_sfd.set_xlabel("Beam Position (m)")
        ax_sfd.set_ylabel("Shear Force (N)")
        ax_sfd.set_title("Shear Force Diagram (SFD)")
        ax_sfd.set_xlim(0, L)
        ax_sfd.grid(True, alpha=0.3)

        fig_sfd.tight_layout()

        st.pyplot(fig_sfd)

        plt.close(fig_sfd)

        # ====================================================
        # BENDING MOMENT DIAGRAM
        # ====================================================

        st.subheader("Bending Moment Diagram (BMD)")

        fig_bmd, ax_bmd = plt.subplots(figsize=(9, 4))

        ax_bmd.plot(
            x,
            bending_moment,
            linewidth=2.5
        )

        ax_bmd.axhline(
            0,
            linewidth=1
        )

        ax_bmd.set_xlabel("Beam Position (m)")
        ax_bmd.set_ylabel("Bending Moment (N·m)")
        ax_bmd.set_title("Bending Moment Diagram (BMD)")
        ax_bmd.set_xlim(0, L)
        ax_bmd.grid(True, alpha=0.3)

        fig_bmd.tight_layout()

        st.pyplot(fig_bmd)

        plt.close(fig_bmd)

        # ====================================================
        # DEFLECTION CURVE
        # ====================================================

        st.subheader("Beam Deflection Curve")

        fig_def, ax_def = plt.subplots(figsize=(9, 4))

        ax_def.plot(
            x,
            deflection * 1000,
            linewidth=2.5
        )

        ax_def.axhline(
            0,
            linewidth=1
        )

        ax_def.set_xlabel("Beam Position (m)")
        ax_def.set_ylabel("Deflection (mm)")
        ax_def.set_title("Beam Deflection Curve")
        ax_def.set_xlim(0, L)
        ax_def.grid(True, alpha=0.3)

        fig_def.tight_layout()

        st.pyplot(fig_def)

        plt.close(fig_def)

     
                        # ====================================================
        # AI EXPLANATION
        # ====================================================

        st.header("🤖 AI Engineering Explanation")

        engineering_prompt = prompts.build_engineering_prompt(results)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
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
            temperature=0.2
        )

        ai_explanation = response.choices[0].message.content

        st.markdown(ai_explanation)

    except Exception as e:

        st.error(f"Analysis error: {e}")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Interactive Beam Deflection & Stress Calculator | "
    "Python + Streamlit + Groq AI"
)
