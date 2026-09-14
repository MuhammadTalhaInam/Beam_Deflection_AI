# prompts.py

SYSTEM_PROMPT = """
You are a mechanical engineering teaching assistant.

Explain the supplied beam analysis results in simple,
clear, and professional engineering language.

IMPORTANT RULES:

1. Use only the numerical results supplied by Python.
2. Do not invent or change numerical values.
3. Keep units correct.
4. Explain what the results mean physically.
5. Do not say the beam is completely safe just because
   the factor of safety is greater than 1.
6. Mention that the analysis is based on ideal beam theory
   and does not include every real-world effect.
7. Keep the explanation suitable for a university
   mechanical engineering student.
8. Do not provide unnecessary mathematical derivations.

Use these headings:

### Engineering Interpretation

### Stress & Safety

### Deflection

### Key Takeaway
"""


def build_engineering_prompt(results):

    # Get values safely from the results dictionary
    material = results.get("material", "Selected material")
    load_type = results.get("load_type", "Selected loading condition")

    prompt = f"""
Analyze the following beam analysis results.

The beam is a simply supported rectangular beam.

Load type:
{load_type}

Material:
{material}

Beam length:
{results.get('L', 0):.3f} m

Beam width:
{results.get('width', 0):.3f} m

Beam height:
{results.get('height', 0):.3f} m

Maximum bending moment:
{results['maximum_moment']:.3f} N·m

Maximum bending stress:
{results['maximum_stress']:.3e} Pa

Yield strength:
{results['yield_strength']:.3e} Pa

Maximum deflection:
{results['maximum_deflection']:.6e} m

Factor of safety:
{results['factor_of_safety']:.2f}

Explain the engineering meaning of these results.

Convert:
- Stress from Pa to MPa
- Deflection from m to mm

Use the following headings:

### Engineering Interpretation
Explain the loading condition and maximum bending moment.

### Stress & Safety
Explain the maximum bending stress, yield strength,
and factor of safety.

### Deflection
Explain the maximum deflection and where it occurs.

### Key Takeaway
Give a short overall engineering conclusion.

Do not recalculate or change the supplied numerical results.
"""

    return prompt
