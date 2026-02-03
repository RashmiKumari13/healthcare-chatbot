# utils/validator.py

def check_emergency(user_input):
    """
    Checks the user's input for high-risk medical keywords.
    Returns a tuple: (is_emergency, message)
    """
    red_flags = [
        "chest pain", "can't breathe", "difficulty breathing", 
        "stroke", "heavy bleeding", "suicide", "self harm", 
        "unconscious", "seizure"
    ]
    
    # Convert input to lowercase to catch "CHEST PAIN" or "Chest Pain"
    user_input_clean = user_input.lower()
    
    for flag in red_flags:
        if flag in user_input_clean:
            return True, "🚨 **EMERGENCY:** Your symptoms may require immediate medical attention. Please call 911 or go to the nearest emergency room."
            
    return False, "YOU are fine!"

def validate_severity(user_input):
    """
    Checks if the user's severity input is a valid number between 1 and 10.
    """
    try:
        score = int(user_input)
        if 1 <= score <= 10:
            return True, score
        return False, "Please enter a number between 1 and 10."
    except ValueError:
        return False, "That doesn't look like a number. Please enter a value from 1 to 10."