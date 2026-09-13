
"""
Prompts for the Generative AI part of the Beam Deflection app.

The engineering calculations are performed by Python.
Groq is used only to explain the calculated results in simple,
educational engineering language.
"""

SYSTEM_PROMPT = """
You are a helpful mechanical engineering teaching assistant.

You explain beam-analysis results to beginner mechanical engineering
students in simple and clear English.

Important rules:
1. Do not invent or recalculate numerical results.
2. Treat the supplied Python-calculated values as authoritative.
3. Explain what the results mean physically.
4. Mention important assumptions when relevant.
5. Keep the explanation educational and concise.
6. Explain the factor of safety clearly.
7. Never claim that the result guarantees real-world structural safety.
8. If a result is unusual, point it out without changing it.
9. Use the exact units supplied in the user data.
10. Do not provide design certification or professional approval.

Use these headings:

### Engineering Interpretation
Explain the main beam behavior.

### Stress & Safety
Explain maximum bending stress, yield strength, and factor of safety.

### Deflection
Explain the maximum deflection and where it occurs.

### Key Takeaway
Give 2-3 short sentences summarizing the result.
"""


def build_engineering_prompt(results):
    """Build the main prompt from Python-calculated results."""

    prompt = f"""
Explain the following beam-analysis results for a beginner
mechanical engineering student.

BEAM INFORMATION
Material: {results.get("material", "Unknown")}
Load type: {results.get("load_type", "Unknown")}
Beam length: {results.get("beam_length")} m
Beam width: {results.get("width")} m
Beam height: {results.get("height")} m

CALCULATED RESULTS
Maximum bending moment: {results.get("maximum_moment")} N.m
Maximum bending stress: {results.get("maximum_stress")} Pa
Material yield strength: {results.get("yield_strength")} Pa
Maximum deflection: {results.get("maximum_deflection")} m
Factor of safety: {results.get("factor_of_safety")}

The values above were calculated by a Python engineering calculation
engine. Do not change, replace, or invent any numerical value.

Explain:
- the main bending behavior for this load case,
- what maximum bending stress means,
- how stress compares with yield strength,
- what the factor of safety means,
- what maximum deflection means,
- and the overall engineering takeaway.

Use simple English suitable for a university mechanical engineering
student learning beam analysis.
"""

    return prompt


def build_short_summary_prompt(results):
    """Build an optional short AI summary prompt."""

    return f"""
Give a short engineering interpretation of these calculated beam results.

Material: {results.get("material")}
Load type: {results.get("load_type")}
Maximum bending moment: {results.get("maximum_moment")} N.m
Maximum bending stress: {results.get("maximum_stress")} Pa
Yield strength: {results.get("yield_strength")} Pa
Maximum deflection: {results.get("maximum_deflection")} m
Factor of safety: {results.get("factor_of_safety")}

Do not recalculate or modify the numerical values.
Explain the meaning in simple mechanical-engineering language.
Keep the answer below 150 words.
"""
