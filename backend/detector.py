import statistics


HARD_THRESHOLD = 500000      # Flag anything above this unconditionally
ROUND_NUMBER_FACTOR = 10000  # Flag suspiciously round numbers like 100000, 500000


def is_suspicious(amount: float, history: list, sender: str = "") -> dict:
    """
    Multi-rule suspicious transaction detector.
    
    Rules:
    1. Hard threshold — above ₹5,00,000
    2. Statistical anomaly — more than 2 standard deviations from history average
    3. Round number — suspiciously round (e.g., exactly 100000, 500000)
    4. Zero amount — possibly a test or error transaction
    
    Returns a dict with flagged (bool), reasons (list), risk_level (str)
    """
    flags = []

    # Rule 1: Hard threshold
    if amount > HARD_THRESHOLD:
        flags.append(f"Amount ₹{amount:,.0f} exceeds hard limit of ₹{HARD_THRESHOLD:,.0f}")

    # Rule 2: Statistical anomaly (only if we have enough history)
    if len(history) >= 5:
        mean = statistics.mean(history)
        stdev = statistics.stdev(history)
        if stdev > 0:
            z_score = (amount - mean) / stdev
            if abs(z_score) > 2:
                flags.append(
                    f"Statistical anomaly: {z_score:.1f} standard deviations from average "
                    f"(avg: ₹{mean:,.0f})"
                )

    # Rule 3: Suspiciously round number
    if amount > 10000 and amount % ROUND_NUMBER_FACTOR == 0:
        flags.append(f"Suspiciously round number: ₹{amount:,.0f}")

    # Rule 4: Zero or negative amount
    if amount <= 0:
        flags.append("Invalid amount: must be greater than zero")

    # Assign risk level
    if len(flags) == 0:
        risk_level = "low"
    elif len(flags) == 1:
        risk_level = "medium"
    else:
        risk_level = "high"

    return {
        "flagged": len(flags) > 0,
        "reasons": flags,
        "risk_level": risk_level
    }