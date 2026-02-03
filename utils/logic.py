from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class PatientData:
    name: str = "N/A"
    reason: str = "N/A"
    severity: Optional[int] = None
    duration: str = "N/A"
    notes: str = "None provided"

def validate_severity(value: Any) -> Optional[int]:
    """Validate severity input (must be between 1 and 10)."""
    try:
        value = int(value)
        if 1 <= value <= 10:
            return value
    except:
        pass
    return None

def generate_summary(data: Dict[str, Any]) -> str:
    """
    Takes a dictionary of patient data and returns a professional medical-style report.
    """

    patient = PatientData(
        name=data.get("name", "N/A"),
        reason=data.get("reason", "N/A"),
        severity=validate_severity(data.get("severity")),
        duration=data.get("duration", "N/A"),
        notes=data.get("notes", "None provided"),
    )

    severity_display = (
        f"{patient.severity}/10"
        if patient.severity is not None
        else "Not specified"
    )

    summary = f"""
    ==========================================
            🏥 PATIENT PRE-VISIT REPORT
    ==========================================

    👤 Patient Name      : {patient.name}
    🩺 Primary Concern   : {patient.reason}
    ⚠️ Severity Level    : {severity_display}
    ⏳ Duration          : {patient.duration}
    📝 Additional Notes : {patient.notes}

    ------------------------------------------
    ⚠️ DISCLAIMER:
    This is a preliminary AI-generated summary 
    and does NOT replace a professional medical diagnosis.
    Please consult a licensed healthcare provider.
    ------------------------------------------
    """

    return summary.strip()

def get_questionnaire() -> Dict[int, str]:
    """
    Returns structured questionnaire — easy to modify or expand.
    """
    return {
        0: "Hello! I'm HealthAssist. To start, what is your **full name**?",
        1: "In a few words, what is the **primary reason** for your visit?",
        2: "On a scale of **1 to 10**, how severe is this discomfort?",
        3: "How many **days** has this been bothering you?",
        4: "Are there any **other symptoms or allergies** you'd like the doctor to know about?"
    }

def get_next_question(current_step: int) -> str:
    """
    Determines the next question based on conversation step.
    """
    questions = get_questionnaire()
    return questions.get(
        current_step,
        "Thank you! I have all the info. Would you like me to generate your report?"
    )
