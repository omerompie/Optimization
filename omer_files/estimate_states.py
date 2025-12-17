def calculate_prediction():
    # ==========================================
    # 1. TWEAK YOUR TARGET SETTINGS HERE
    # ==========================================

    # Grid Configuration (From main.py)
    TARGET_RINGS = 60  # Default: 29
    TARGET_ANGLES = 40  # Default: 21

    # Solver Configuration
    TARGET_PRUNE_TIME = 10.0  # Default: 100.0 (seconds)

    # ==========================================
    # 2. BASELINE DATA (DO NOT CHANGE)
    # Calibrated from your successful "53k states" run
    # ==========================================
    BASE_RINGS = 29
    BASE_ANGLES = 21
    BASE_TIME_BIN = 100.0
    BASE_STATES = 53159

    # Approximate processing speed (States per second)
    # Your PC did 53k very fast, so ~100k/sec is a safe estimate
    STATES_PER_SECOND = 100000

    # ==========================================
    # 3. CALCULATION LOGIC
    # ==========================================

    # Calculate Node Multiplier (Linear)
    # Complexity scales with Total Nodes ~= Rings * Angles
    base_node_count = BASE_RINGS * BASE_ANGLES
    target_node_count = TARGET_RINGS * TARGET_ANGLES
    node_multiplier = target_node_count / base_node_count

    # Calculate Time Multiplier (Inverse)
    # Halving the bin size doubles the number of buckets
    time_multiplier = BASE_TIME_BIN / TARGET_PRUNE_TIME

    # Total predicted states
    predicted_states = BASE_STATES * node_multiplier * time_multiplier

    # Estimated Runtime
    est_seconds = predicted_states / STATES_PER_SECOND

    # ==========================================
    # 4. REPORT
    # ==========================================
    print("-" * 50)
    print(f"COMPLEXITY PREDICTOR")
    print("-" * 50)
    print(f"BASELINE:   {BASE_RINGS}x{BASE_ANGLES} Grid, {BASE_TIME_BIN}s bins -> {BASE_STATES:,} states")
    print(f"TARGET:     {TARGET_RINGS}x{TARGET_ANGLES} Grid, {TARGET_PRUNE_TIME}s bins")
    print("-" * 50)
    print(f"PREDICTED STATES:   ~{int(predicted_states):,}")
    print(f"Likely Range:       {int(predicted_states * 0.9):,} to {int(predicted_states * 1.1):,}")
    print(f"Est. Runtime:       {est_seconds:.4f} seconds")
    print("-" * 50)

    # Risk Assessment
    if predicted_states > 2000000:
        print("⚠️ WARNING: >2 Million states. Expect 20-30s runtime.")
    elif predicted_states > 5000000:
        print("🛑 CRITICAL: >5 Million states. High risk of RAM crash.")
    else:
        print("✅ STATUS: Safe to run.")


if __name__ == "__main__":
    calculate_prediction()