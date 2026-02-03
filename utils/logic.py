from dataclasses import dataclass
from typing import Optional, Dict, Any
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

@dataclass
class PatientData:
    name: str = "N/A"
    reason: str = "N/A"
    severity: Optional[int] = None
    duration: str = "N/A"
    notes: str = "None provided"

def load_symptom_faq():
    """Load symptom database from CSV"""
    try:
        return pd.read_csv("data/symptoms_faq.csv")
    except:
        return None

def get_symptom_info(symptom: str):
    """Fetch symptom info and recommendation from CSV"""
    df = load_symptom_faq()
    if df is None:
        return None, None

    symptom = symptom.lower().strip()

    match = df[df["symptom"].str.contains(symptom, case=False, na=False)]
    if not match.empty:
        info = match.iloc[0]["info"]
        recommendation = match.iloc[0]["recommendation"]
        return info, recommendation

    return None, None

def validate_severity(value: Any) -> Optional[int]:
    try:
        value = int(value)
        if 1 <= value <= 10:
            return value
    except:
        pass
    return None

def generate_summary(data: Dict[str, Any]) -> str:
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

    info, recommendation = get_symptom_info(patient.reason)

    info_text = info if info else "Not available in database."
    reco_text = recommendation if recommendation else "Consult a doctor if symptoms persist."

    summary = f"""
    🏥 **PATIENT PRE-VISIT REPORT**
    --------------------------------
    👤 Patient Name      : {patient.name}
    🩺 Primary Concern   : {patient.reason}
    ℹ️ Symptom Info      : {info_text}
    ⚠️ Severity Level    : {severity_display}
    ⏳ Duration          : {patient.duration}
    📝 Additional Notes : {patient.notes}

    ✅ Basic Recommendation:
    {reco_text}

    ⚠️ DISCLAIMER:
    This is a preliminary AI-generated summary and does NOT replace a professional medical diagnosis.
    """

    return summary.strip()

def get_questionnaire():
    return {
        0: "Hello! I'm HealthAssist. What is your **full name**?",
        1: "What is your **primary symptom or reason** for visiting?",
        2: "On a scale of **1 to 10**, how severe is this discomfort?",
        3: "How many **days** has this been bothering you?",
        4: "Any **other symptoms or allergies**?"
    }

def get_next_question(current_step: int) -> str:
    questions = get_questionnaire()
    return questions.get(
        current_step,
        "Thanks! Click **Generate Report** when you're ready."
    )

def get_dynamic_question(symptom):
    symptom = symptom.lower()

    if "body ache" in symptom:
        return "Is the pain in your whole body or a specific area?"
    elif "fever" in symptom:
        return "What is your current body temperature?"
    elif "headache" in symptom:
        return "Is it mild, moderate, or severe?"
    else:
        return "Can you describe this symptom in more detail?"

# ---------- PDF FUNCTION (LAZY IMPORT — SAFE) ----------

def generate_pdf_report(data):
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

    # ✅ Save inside your project folder instead of /mnt/data/
    file_path = os.path.join(os.getcwd(), "healthassist_report.pdf")

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    story = []

    content = f"""
    PATIENT PRE-VISIT REPORT

    Patient Name: {data.get('name','N/A')}
    Primary Concern: {data.get('reason','N/A')}
    Severity Level: {data.get('severity','N/A')}/10
    Duration: {data.get('duration','N/A')}
    Additional Notes: {data.get('notes','None')}

    Disclaimer:
    This is a preliminary AI-generated report and does not replace professional medical advice.
    """

    for line in content.strip().split("\n"):
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    return file_path
