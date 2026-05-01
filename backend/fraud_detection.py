def analyze_risk(amount, history):
    """
    Determines risk level based on transaction patterns.
    """
    # Rule 1: Extremely high amount
    if amount > 500000:
        return "HIGH"
    
    # Rule 2: Round numbers often indicate lack of specific invoicing
    if amount > 0 and amount % 100000 == 0:
        return "MEDIUM"
    
    # Rule 3: Sudden spike compared to average of last 3 transactions
    if len(history) >= 3:
        last_three = [b.amount for b in history[-3:]]
        avg = sum(last_three) / 3
        if amount > avg * 3:
            return "MEDIUM"
            
    return "LOW"
