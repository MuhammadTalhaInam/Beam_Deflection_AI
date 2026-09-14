# 🏗️ Interactive Beam Deflection & Stress Calculator

An AI-powered web application for analyzing a simply supported rectangular beam under different loading conditions.

The application performs engineering calculations using Python and provides interactive Shear Force Diagram (SFD), Bending Moment Diagram (BMD), deflection results, bending stress, and Factor of Safety. Groq AI is used to provide an easy-to-understand engineering explanation of the calculated results.

## 🚀 Live Demo

https://beamdeflectionai-hbw3wnhw6wtjio28iwdkem.streamlit.app

## 📌 Project Features

- Simply supported rectangular beam analysis
- Center point load analysis
- Full-span Uniformly Distributed Load (UDL) analysis
- Maximum bending moment calculation
- Maximum bending stress calculation
- Maximum beam deflection calculation
- Factor of Safety calculation
- Shear Force Diagram (SFD)
- Bending Moment Diagram (BMD)
- Beam deflection curve
- Multiple material options
- AI-powered engineering explanation using Groq
- Interactive Streamlit interface

## 🛠️ Technologies Used

- Python
- NumPy
- Matplotlib
- Streamlit
- Groq AI
- GitHub

## ⚙️ Engineering Calculations

The application uses standard beam theory equations for a simply supported rectangular beam.

### Center Point Load

Maximum bending moment:

Mmax = P × L / 4

Maximum deflection:

δmax = P × L³ / (48 × E × I)

### Full-Span UDL

Maximum bending moment:

Mmax = w × L² / 8

Maximum deflection:

δmax = 5 × w × L⁴ / (384 × E × I)

### Bending Stress

σmax = Mmax × c / I

### Factor of Safety

FOS = Yield Strength / Maximum Bending Stress

## 📂 Project Structure

```text
Beam_Deflection_AI/
│
├── app.py
├── workflow.py
├── prompts.py
├── requirements.txt
└── README.md
