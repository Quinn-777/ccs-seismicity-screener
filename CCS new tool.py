# Step 1: SCORING ENGINE
def d_value(level):
    if level == "high":
        return 1
    elif level == "moderate":
        return 0.5
    else:
        return 0

def risk_score(entries):
    numerator = 0
    denominator = 0
    for weight, level in entries:
        if level == "na":
            continue    #If I don't know, just skip it. Neither bucket will be moved
        numerator = numerator + weight * d_value(level)
        denominator = denominator + weight
    if denominator == 0:
        return None
    return numerator / denominator * 100

# Step 2: CLASSIFICATION FUNCTIONS

def classify_permeability(value):
    if value < 1:
        return "high"
    elif value > 100:
        return "low"
    else:
        return "moderate"

def classify_proximity(value):
    if value < 1:
        return "high"
    else:
        return "low"

def classify_pathways(answer):
    if answer == "yes":
        return "high"
    elif answer == "no":
        return "low"
    else:
        return "na"

def classify_roughness(answer):
    if answer == "smooth":
        return "low"
    elif answer == "rough":
        return "high"
    else:
        return "na"

def classify_size(value):
    if value < 200:
        return "low"
    elif 200 <= value < 1000:
        return "moderate"
    else:
        return "high"

def classify_continuity(value):
    if value == "continuous":
        return "high"
    elif value == "heterogeneous":
        return "low"
    else:
        return "na"

def classify_stress(value):
    if value >= 0.6:
        return "high"
    else:
        return "low"

def classify_caprock(value):
    if value < 50:
        return "high"
    else:
        return "low"

# STEP 3: INPUT LAYER

def ask_permeability():
    print("\n--- Fault permeability ---")
    print("1. I have a value (in mD)")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        value = float(input("Enter permeability in mD: "))
        return classify_permeability(value)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
         return "na"

def ask_proximity():
    print("\n--- proximity to basement ---")
    print("1. I have a value (in km)")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        value = float(input("Enter distance to basement in km: "))
        return classify_proximity(value)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

def ask_pathways():
    print("\n--- Fluid Pathways ---")
    print("1. I know whether a pathway is present ")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        answer = input("Fluid pathway present? (yes / no): ")
        return classify_pathways(answer)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

def ask_roughness():
    print("\n--- Fault Roughness ---")
    print("1. I know the fault surface type ")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        answer = input("Fault surfaces? (smooth / rough): ")
        return classify_roughness(answer)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

def ask_size():
    print("\n--- Fault Size/Length ---")
    print("1. I know a value (in m)  ")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        value = float(input("Enter fault size in m: "))
        return classify_size(value)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

def ask_continuity():
    print("\n--- Fault Continuity ---")
    print("1. I know whether a fault is continuous: ")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        answer = input("Fault continuity? (continuous / heterogeneous):")
        return classify_continuity(answer)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

def ask_stress():
    print("\n--- Stress State ---")
    print("1. I know a value (in µmob): ")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        value = float(input("Enter mobilized friction µmob (dimensionless):"))
        return classify_stress(value)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

def ask_caprock():
    print("\n--- Caprock Integrity---")
    print("1. I know a value (in m): ")
    print("2. I only know the risk level")
    print("3. I don't know")
    choice = input("choose: 1 / 2 / 3: ")

    if choice == "1":
        value = float(input("Enter caprock thickness in m: "))
        return classify_caprock(value)
    elif choice == "2":
        level = input("Enter high / moderate / low: ")
        if level in ("high", "moderate", "low"):
            return level
        else:
            print("Not recognized – recording as no data.")
            return "na"
    else:
        return "na"

# MAIN PROGRAM

def main():
    print("=" * 50)
    print("CO2 Storage – Induced Seismicity Risk Screener")
    print("=" * 50)

    entries = [
        ("Fault permeability", 2, ask_permeability()),
        ("Fluid pathways", 2, ask_pathways()),
        ("Fault roughness", 1, ask_roughness()),
        ("Fault size/length", 2, ask_size()),
        ("Fault continuity", 2, ask_continuity()),
        ("Stress state", 2, ask_stress()),
        ("Proximity to basement", 2, ask_proximity()),
        ("Caprock integrity", 1, ask_caprock()),
    ]
    print_report(entries)



def print_report(entries):
    print("\n" + "=" * 50)
    print("PARAMETER BREAKDOWN")
    print("=" * 50)

    for name, weight, level in entries:
        if level == "na":
            print(f"{name:<28} {'no data':>12}")
        else:
            contribution = weight * d_value(level)
            print(f"{name:<28} {level:>10}  {contribution}/{weight}")

    simple = []
    for name, weight, level in entries:
        simple.append((weight, level))
    score = risk_score(simple)

    print("\n" + "=" * 50)
    if score is None:
        print("No data entered – cannot calculate risk score.")
    else:
        print("RISK SCORE:", round(score,2), "%")

# ============================================
# TESTS
# ============================================

def run_tests():
    # --- threshold ---
    assert classify_permeability(0.5) == "high"
    assert classify_permeability(1) == "moderate"
    assert classify_permeability(100) == "moderate"
    assert classify_permeability(150) == "low"

    assert classify_size(199) == "low"
    assert classify_size(200) == "moderate"
    assert classify_size(999) == "moderate"
    assert classify_size(1000) == "high"

    assert classify_stress(0.59) == "low"
    assert classify_stress(0.6) == "high"
    assert classify_proximity(0.99) == "high"
    assert classify_proximity(1) == "low"
    assert classify_caprock(49) == "high"
    assert classify_caprock(50) == "low"

    #
    assert classify_roughness("rough") == "high"
    assert classify_roughness("smooth") == "low"
    assert classify_roughness("Rough") == "na"
    assert classify_pathways("yes") == "high"
    assert classify_pathways("no") == "low"
    assert classify_continuity("continuous") == "high"
    assert classify_continuity("heterogeneous") == "low"

    # --- engine ---
    assert d_value("high") == 1
    assert d_value("moderate") == 0.5
    assert d_value("low") == 0
    assert risk_score([(2, "high"), (1, "high")]) == 100
    assert risk_score([(2, "low"), (1, "low")]) == 0
    assert risk_score([(2, "na"), (1, "na")]) is None
    assert risk_score([(2, "high"), (2, "na")]) == 100

    # --- Case：Illinois Basin-Decatur → 8/13 = 61.54% ---
    illinois = [
        (2, classify_permeability(0.1013)),
        (2, classify_pathways("yes")),
        (1, "na"),
        (2, "low"),
        (2, classify_continuity("continuous")),
        (2, "high"),
        (2, classify_proximity(2.2)),
        (1, classify_caprock(125)),
    ]
    assert round(risk_score(illinois), 2) == 61.54

    # --- case: In Salah → 7/14 = 50.00% ---
    insalah = [
        (2, classify_permeability(4.75)),
        (2, classify_pathways("yes")),
        (1, classify_roughness("smooth")),
        (2, classify_size(4000)),
        (2, classify_continuity("continuous")),
        (2, classify_stress(0.4)),
        (2, classify_proximity(3.1)),
        (1, classify_caprock(950)),
    ]
    assert round(risk_score(insalah), 2) == 50.00

    # --- Case：Basel → 12/14 = 85.71% ---
    basel = [
        (2, classify_permeability(0.005877)),
        (2, classify_pathways("yes")),
        (1, classify_roughness("rough")),
        (2, classify_size(1000)),
        (2, classify_continuity("continuous")),
        (2, classify_stress(0.7)),
        (2, classify_proximity(2.12)),
        (1, "high"),
    ]
    assert round(risk_score(basel), 2) == 85.71

    print("All tests passed ✓")
# –––––––––– test ends ––––––––––


if __name__ == "__main__":
    run_tests()
    main()
