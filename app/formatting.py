def get_betting_recommendation(value, avg, source_name, metric_type):
    """
    Determine betting recommendation based on comparison with average value
    Green = recommended bet, Red = not recommended
    """
    if value is None or avg is None:
        return ""
    
    # Difference between source value and average
    difference = value - avg
    
    # Thresholds for recommendations (configurable)
    strong_threshold = 1.0  # Strong recommendation
    weak_threshold = 0.5    # Weak recommendation
    
    if metric_type == "spread":
        # For spread: if source gives higher spread than average - green (bet on favorite)
        if difference > strong_threshold:
            return "cell-pos"  # Green - bet
        elif difference < -strong_threshold:
            return "cell-neg"  # Red - don't bet
        elif abs(difference) < weak_threshold:
            return "cell-neutral"  # Neutral - be careful
    
    elif metric_type == "total":
        # For total: if source gives higher total than average - green (bet on over)
        if difference > strong_threshold:
            return "cell-pos"  # Green - bet on over
        elif difference < -strong_threshold:
            return "cell-neg"  # Red - bet on under
        elif abs(difference) < weak_threshold:
            return "cell-neutral"  # Neutral
    
    elif metric_type == "winprob":
        # For win probability: if source gives higher probability than average - green
        if difference > 0.05:  # 5% difference
            return "cell-pos"  # Green - bet on home team
        elif difference < -0.05:
            return "cell-neg"  # Red - bet on away team
        else:
            return "cell-neutral"  # Neutral
    
    return ""

def get_spread_class(value, avg, source_name):
    """CSS class for spread with betting recommendation"""
    return get_betting_recommendation(value, avg, source_name, "spread")

def get_total_class(value, avg, source_name):
    """CSS class for total with betting recommendation"""
    return get_betting_recommendation(value, avg, source_name, "total")

def get_winprob_class(value, avg, source_name):
    """CSS class for win probability with betting recommendation"""
    return get_betting_recommendation(value, avg, source_name, "winprob")
