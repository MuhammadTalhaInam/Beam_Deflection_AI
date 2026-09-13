"""
Beam Deflection & Stress Calculator
Engineering calculation workflow.

Version 1 supports:
1. Simply supported beam + center point load
2. Simply supported beam + full-span uniformly distributed load (UDL)

All internal calculations use SI units:
- Length: m
- Force: N
- Distributed load: N/m
- Young's modulus: Pa
- Stress: Pa
- Moment: N.m
- Deflection: m
"""

import numpy as np


# ============================================================
# MATERIAL DATABASE
# ============================================================

MATERIALS = {
    "Structural Steel": {
        "youngs_modulus": 200e9,       # Pa
        "yield_strength": 250e6,       # Pa
        "youngs_modulus_gpa": 200,     # GPa
        "yield_strength_mpa": 250      # MPa
    },

    "Aluminum 6061-T6": {
        "youngs_modulus": 69e9,
        "yield_strength": 276e6,
        "youngs_modulus_gpa": 69,
        "yield_strength_mpa": 276
    },

    "Stainless Steel 304": {
        "youngs_modulus": 193e9,
        "yield_strength": 215e6,
        "youngs_modulus_gpa": 193,
        "yield_strength_mpa": 215
    }
}


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_positive(value, name):
    """Make sure a numerical input is positive."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number.")

    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")

    return value


def validate_material(material_name):
    """Make sure the selected material exists."""
    if material_name not in MATERIALS:
        raise ValueError(
            f"Unknown material: {material_name}. "
            f"Choose one of: {', '.join(MATERIALS.keys())}"
        )


# ============================================================
# SECTION PROPERTIES
# ============================================================

def calculate_rectangular_properties(width, height):
    """
    Calculate properties of a rectangular beam cross-section.

    width  : m
    height : m
    """

    width = validate_positive(width, "Width")
    height = validate_positive(height, "Height")

    area = width * height
    moment_of_inertia = (width * height**3) / 12
    c = height / 2

    return {
        "area": area,
        "moment_of_inertia": moment_of_inertia,
        "c": c
    }


# ============================================================
# MATERIAL PROPERTIES
# ============================================================

def get_material_properties(material_name):
    """Return the properties of a selected material."""
    validate_material(material_name)
    return MATERIALS[material_name].copy()


# ============================================================
# POINT LOAD CALCULATIONS
# ============================================================

def calculate_point_load_beam(
    L,
    width,
    height,
    P,
    E,
    yield_strength
):
    """
    Simply supported beam with a center point load.

    L              : beam length (m)
    width          : beam width (m)
    height         : beam height (m)
    P              : point load (N)
    E              : Young's modulus (Pa)
    yield_strength : yield strength (Pa)
    """

    L = validate_positive(L, "Beam length")
    P = validate_positive(P, "Point load")
    E = validate_positive(E, "Young's modulus")
    yield_strength = validate_positive(yield_strength, "Yield strength")

    properties = calculate_rectangular_properties(width, height)

    I = properties["moment_of_inertia"]
    c = properties["c"]

    # Symmetric center point load
    RA = P / 2
    RB = P / 2

    # Maximum bending moment
    M_max = (P * L) / 4

    # Maximum bending stress
    sigma_max = (M_max * c) / I

    # Maximum deflection
    delta_max = (P * L**3) / (48 * E * I)

    # Factor of safety
    factor_of_safety = yield_strength / sigma_max

    return {
        "load_type": "Center Point Load",
        "beam_length": L,
        "width": width,
        "height": height,
        "point_load": P,
        "youngs_modulus": E,
        "yield_strength": yield_strength,
        "area": properties["area"],
        "moment_of_inertia": I,
        "c": c,
        "reaction_A": RA,
        "reaction_B": RB,
        "maximum_shear": P / 2,
        "maximum_moment": M_max,
        "maximum_stress": sigma_max,
        "maximum_deflection": delta_max,
        "factor_of_safety": factor_of_safety
    }


# ============================================================
# UDL CALCULATIONS
# ============================================================

def calculate_udl_beam(
    L,
    width,
    height,
    w,
    E,
    yield_strength
):
    """
    Simply supported beam with a full-span UDL.

    L              : beam length (m)
    width          : beam width (m)
    height         : beam height (m)
    w              : UDL (N/m)
    E              : Young's modulus (Pa)
    yield_strength : yield strength (Pa)
    """

    L = validate_positive(L, "Beam length")
    w = validate_positive(w, "UDL")
    E = validate_positive(E, "Young's modulus")
    yield_strength = validate_positive(yield_strength, "Yield strength")

    properties = calculate_rectangular_properties(width, height)

    I = properties["moment_of_inertia"]
    c = properties["c"]

    # Total load
    total_load = w * L

    # Symmetric support reactions
    RA = total_load / 2
    RB = total_load / 2

    # Maximum bending moment
    M_max = (w * L**2) / 8

    # Maximum bending stress
    sigma_max = (M_max * c) / I

    # Maximum deflection
    delta_max = (5 * w * L**4) / (384 * E * I)

    # Factor of safety
    factor_of_safety = yield_strength / sigma_max

    return {
        "load_type": "Full-Span UDL",
        "beam_length": L,
        "width": width,
        "height": height,
        "udl": w,
        "total_load": total_load,
        "youngs_modulus": E,
        "yield_strength": yield_strength,
        "area": properties["area"],
        "moment_of_inertia": I,
        "c": c,
        "reaction_A": RA,
        "reaction_B": RB,
        "maximum_shear": total_load / 2,
        "maximum_moment": M_max,
        "maximum_stress": sigma_max,
        "maximum_deflection": delta_max,
        "factor_of_safety": factor_of_safety
    }


# ============================================================
# POINT LOAD SFD / BMD / DEFLECTION
# ============================================================

def generate_point_load_diagrams(L, P, E, I, num_points=201):
    """
    Generate x-position, shear force, bending moment,
    and deflection arrays for a center point load.
    """

    L = validate_positive(L, "Beam length")
    P = validate_positive(P, "Point load")
    E = validate_positive(E, "Young's modulus")
    I = validate_positive(I, "Moment of inertia")

    x = np.linspace(0, L, num_points)
    RA = P / 2

    # Use a tiny tolerance around the exact load point.
    left = x < L / 2
    right = x > L / 2
    center = np.isclose(x, L / 2)

    # Shear force
    V = np.zeros_like(x)
    V[left] = RA
    V[right] = RA - P

    # Leave the exact load point undefined so a plotting library
    # shows the physical jump in shear force rather than drawing
    # a diagonal line through the discontinuity.
    V[center] = np.nan

    # Bending moment
    M = np.where(
        x <= L / 2,
        RA * x,
        RA * x - P * (x - L / 2)
    )

    # Deflection: positive value represents downward deflection.
    delta = np.zeros_like(x)

    left_deflection = x <= L / 2
    right_deflection = x > L / 2

    delta[left_deflection] = (
        P
        * x[left_deflection]
        * (3 * L**2 - 4 * x[left_deflection]**2)
        / (48 * E * I)
    )

    distance_from_right = L - x[right_deflection]

    delta[right_deflection] = (
        P
        * distance_from_right
        * (
            3 * L**2
            - 4 * distance_from_right**2
        )
        / (48 * E * I)
    )

    return {
        "x": x,
        "shear_force": V,
        "bending_moment": M,
        "deflection": delta
    }


# ============================================================
# UDL SFD / BMD / DEFLECTION
# ============================================================

def generate_udl_diagrams(L, w, E, I, num_points=201):
    """
    Generate x-position, shear force, bending moment,
    and deflection arrays for a full-span UDL.
    """

    L = validate_positive(L, "Beam length")
    w = validate_positive(w, "UDL")
    E = validate_positive(E, "Young's modulus")
    I = validate_positive(I, "Moment of inertia")

    x = np.linspace(0, L, num_points)

    RA = (w * L) / 2

    # Shear force
    V = RA - w * x

    # Bending moment
    M = RA * x - (w * x**2) / 2

    # Deflection for full-span UDL.
    # Positive value represents downward deflection.
    #
    # δ(x) = w*x*(L^3 - 2L*x^2 + x^3) / (24EI)
    #
    # This equation is valid from the left support and
    # automatically gives zero deflection at x = 0 and x = L.
    delta = (
        w
        * x
        * (L**3 - 2 * L * x**2 + x**3)
        / (24 * E * I)
    )

    return {
        "x": x,
        "shear_force": V,
        "bending_moment": M,
        "deflection": delta
    }


# ============================================================
# COMPLETE WORKFLOW
# ============================================================

def run_beam_analysis(
    material_name,
    load_type,
    L,
    width,
    height,
    load
):
    """
    Main function used by the Streamlit application.

    material_name:
        Material name from MATERIALS.

    load_type:
        "Center Point Load" or "Full-Span UDL"

    L:
        Beam length in m

    width:
        Beam width in m

    height:
        Beam height in m

    load:
        N for point load
        N/m for UDL
    """

    validate_material(material_name)

    L = validate_positive(L, "Beam length")
    width = validate_positive(width, "Width")
    height = validate_positive(height, "Height")
    load = validate_positive(load, "Load")

    material = get_material_properties(material_name)

    E = material["youngs_modulus"]
    yield_strength = material["yield_strength"]

    properties = calculate_rectangular_properties(width, height)

    I = properties["moment_of_inertia"]

    if load_type == "Center Point Load":

        results = calculate_point_load_beam(
            L=L,
            width=width,
            height=height,
            P=load,
            E=E,
            yield_strength=yield_strength
        )

        diagrams = generate_point_load_diagrams(
            L=L,
            P=load,
            E=E,
            I=I
        )

    elif load_type == "Full-Span UDL":

        results = calculate_udl_beam(
            L=L,
            width=width,
            height=height,
            w=load,
            E=E,
            yield_strength=yield_strength
        )

        diagrams = generate_udl_diagrams(
            L=L,
            w=load,
            E=E,
            I=I
        )

    else:
        raise ValueError(
            "Unsupported load type. "
            "Choose 'Center Point Load' or 'Full-Span UDL'."
        )

    # Add material information
    results["material"] = material_name
    results["load_type"] = load_type

    # Add diagram arrays
    results["x"] = diagrams["x"]
    results["shear_force"] = diagrams["shear_force"]
    results["bending_moment"] = diagrams["bending_moment"]
    results["deflection"] = diagrams["deflection"]

    # Convenient maximum values from the generated arrays
    results["diagram_max_shear"] = float(
        np.max(np.abs(diagrams["shear_force"]))
    )

    results["diagram_max_moment"] = float(
        np.max(diagrams["bending_moment"])
    )

    results["diagram_max_deflection"] = float(
        np.max(diagrams["deflection"])
    )

    results["max_deflection_position"] = float(
        diagrams["x"][np.argmax(diagrams["deflection"])]
    )

    return results


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print("Testing Structural Steel + Center Point Load...")

    test = run_beam_analysis(
        material_name="Structural Steel",
        load_type="Center Point Load",
        L=2.0,
        width=0.05,
        height=0.10,
        load=1000
    )

    print(f"Maximum Moment: {test['maximum_moment']:.2f} N.m")
    print(
        f"Maximum Stress: "
        f"{test['maximum_stress'] / 1e6:.2f} MPa"
    )
    print(
        f"Maximum Deflection: "
        f"{test['maximum_deflection'] * 1000:.4f} mm"
    )
    print(
        f"Factor of Safety: "
        f"{test['factor_of_safety']:.2f}"
    )
