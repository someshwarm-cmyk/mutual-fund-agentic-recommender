def generate_explanation(risk_profile):
    
    if risk_profile == "Conservative":
        return "You prefer stability with lower volatility. Recommended funds focus on stability and steady NAV growth."
    
    elif risk_profile == "Moderate":
        return "You balance risk and returns. These funds offer moderate growth with controlled volatility."
    
    elif risk_profile == "Aggressive":
        return "You seek high returns and accept higher volatility. Recommended funds emphasize growth potential."
    
    else:
        return "Default recommendation applied."