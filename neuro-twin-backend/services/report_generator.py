from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os


# ============================================================
# CONFIGURATION
# ============================================================

PAGE_WIDTH, PAGE_HEIGHT = A4


# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontSize=22,
    leading=28,
    alignment=TA_CENTER,
    spaceAfter=15,
)

SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=12,
    leading=18,
    alignment=TA_CENTER,
    spaceAfter=20,
)

H1 = ParagraphStyle(
    "Heading1Custom",
    parent=styles["Heading1"],
    fontSize=16,
    leading=20,
    spaceBefore=10,
    spaceAfter=10,
)

H2 = ParagraphStyle(
    "Heading2Custom",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    spaceBefore=8,
    spaceAfter=6,
)

BODY = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
)

SMALL = ParagraphStyle(
    "Small",
    parent=styles["BodyText"],
    fontSize=8,
    leading=11,
)

CENTER = ParagraphStyle(
    "Center",
    parent=BODY,
    alignment=TA_CENTER,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def P(text, style=BODY):
    """Create a paragraph safely."""
    if text is None:
        text = "N/A"

    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    return Paragraph(text, style)


def make_table(data, widths=None, header=True):

    table = Table(
        data,
        colWidths=widths,
        repeatRows=1 if header else 0,
    )

    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]

    if header:
        style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])

    table.setStyle(TableStyle(style))

    return table


def add_image(path, width=160 * mm):

    if not path or not os.path.exists(path):
        return P("Image not available.")

    img = Image(path)

    ratio = img.imageHeight / float(img.imageWidth)

    img.drawWidth = width
    img.drawHeight = width * ratio

    return img


# ============================================================
# SEVERITY LOGIC
# ============================================================

def get_severity(defect):

    """
    Project screening logic.

    This does NOT claim structural failure.
    It provides a screening level that can be reviewed
    by an engineer.
    """

    severity = defect.get("severity")

    if severity:
        return severity

    defect_type = defect.get("type", "").lower()

    width = defect.get("max_width_mm")

    if width is not None:

        try:
            width = float(width)

            if width > 1.0:
                return "L4"

            if width > 0.50:
                return "L3"

            if width > 0.30:
                return "L2"

            return "L1"

        except (ValueError, TypeError):
            pass

    if defect_type in ["corrosion", "exposed_rebar"]:
        return "L3"

    if defect_type == "spalling":
        return "L2"

    return "L1"


# ============================================================
# RECOMMENDATIONS
# ============================================================

def get_recommendation(defect):

    defect_type = defect.get("type", "").lower()
    severity = get_severity(defect)

    if severity == "L4":
        return (
            "Engineer assessment recommended. "
            "Restrict access/load where necessary and assess "
            "stabilization or repair requirements."
        )

    if defect_type == "crack":
        return (
            "Measure and map the crack, assess whether movement "
            "is suspected, determine likely cause, and select "
            "repair based on crack activity and site condition."
        )

    if defect_type == "spalling":
        return (
            "Inspect deteriorated concrete and reinforcement. "
            "Determine extent and cause before selecting patch "
            "repair and protection."
        )

    if defect_type == "corrosion":
        return (
            "Inspect reinforcement condition, determine corrosion "
            "cause and extent, and assess concrete/reinforcement "
            "repair and protection requirements."
        )

    if defect_type == "exposed_rebar":
        return (
            "Inspect exposed reinforcement and surrounding "
            "concrete. Assess corrosion and provide appropriate "
            "repair/protection after engineering review."
        )

    return "Detailed inspection and engineering review recommended."


# ============================================================
# MAIN PDF FUNCTION
# ============================================================

def generate_inspection_report(
    output_path,
    project_info,
    detections,
    original_image=None,
    annotated_image=None,
):
    """
    Generate Neuro Twin Mesh Structural Inspection Report.

    Parameters
    ----------
    output_path:
        Destination PDF path.

    project_info:
        Dictionary containing project/site information.

    detections:
        List of AI detection dictionaries.

    original_image:
        Path to original image.

    annotated_image:
        Path to AI annotated image.
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Neuro Twin Mesh Structural Inspection Report",
    )

    story = []

    # ========================================================
    # COVER PAGE
    # ========================================================

    story.append(Spacer(1, 35 * mm))

    story.append(
        P(
            "NEURO TWIN MESH",
            TITLE,
        )
    )

    story.append(
        P(
            "AI-Assisted Structural Defect Inspection Report",
            SUBTITLE,
        )
    )

    story.append(Spacer(1, 15 * mm))

    cover_data = [
        [P("<b>Project</b>"), P(project_info.get("project", "N/A"))],
        [P("<b>Structure ID</b>"), P(project_info.get("structure_id", "N/A"))],
        [P("<b>Location</b>"), P(project_info.get("location", "N/A"))],
        [P("<b>Inspection Date</b>"), P(project_info.get("inspection_date", datetime.now().strftime("%d-%m-%Y")))],
        [P("<b>Inspection Team</b>"), P(project_info.get("inspector", "N/A"))],
    ]

    story.append(
        make_table(
            cover_data,
            widths=[55 * mm, 115 * mm],
            header=False,
        )
    )

    story.append(Spacer(1, 20 * mm))

    story.append(
        P(
            "AI model: YOLO-based structural defect segmentation",
            CENTER,
        )
    )

    story.append(
        P(
            "Defect classes: Crack, Spalling, Corrosion, Exposed Rebar",
            CENTER,
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 1. EXECUTIVE SUMMARY
    # ========================================================

    story.append(P("1. Executive Summary", H1))

    total = len(detections)

    counts = {}

    for d in detections:
        defect_type = d.get("type", "unknown")
        counts[defect_type] = counts.get(defect_type, 0) + 1

    summary_text = (
        f"The Neuro Twin Mesh inspection pipeline processed the supplied "
        f"inspection image and identified {total} AI detection(s). "
        f"The detected defect categories are summarized below. "
        f"AI detections are intended to support inspection and screening "
        f"and should be reviewed against field measurements and appropriate "
        f"engineering assessment."
    )

    story.append(P(summary_text))

    story.append(Spacer(1, 8))

    summary_table = [
        [P("<b>Defect Type</b>"), P("<b>Detected Count</b>")]
    ]

    for defect_type, count in counts.items():
        summary_table.append([
            P(defect_type.title()),
            P(str(count)),
        ])

    story.append(
        make_table(
            summary_table,
            widths=[100 * mm, 60 * mm],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 2. PROJECT INFORMATION
    # ========================================================

    story.append(P("2. Project & Inspection Information", H1))

    project_rows = [
        ["Project", project_info.get("project", "N/A")],
        ["Structure ID", project_info.get("structure_id", "N/A")],
        ["Location", project_info.get("location", "N/A")],
        ["Block", project_info.get("block", "N/A")],
        ["Floor", project_info.get("floor", "N/A")],
        ["Member Type", project_info.get("member_type", "N/A")],
        ["Member/Grid", project_info.get("member_grid", "N/A")],
        ["Inspector/Team", project_info.get("inspector", "N/A")],
        ["Weather", project_info.get("weather", "N/A")],
        ["Exposure", project_info.get("exposure", "N/A")],
    ]

    project_table = [
        [P("<b>Parameter</b>"), P("<b>Value</b>")]
    ]

    for key, value in project_rows:
        project_table.append([
            P(key),
            P(value),
        ])

    story.append(
        make_table(
            project_table,
            widths=[60 * mm, 100 * mm],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 3. ORIGINAL IMAGE
    # ========================================================

    story.append(P("3. Inspection Image", H1))

    if original_image:
        story.append(add_image(original_image, 160 * mm))
        story.append(Spacer(1, 5 * mm))

    story.append(
        P(
            "Original inspection image supplied to the Neuro Twin Mesh "
            "inspection pipeline."
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 4. AI DETECTION RESULT
    # ========================================================

    story.append(P("4. AI Detection Results", H1))

    if annotated_image:
        story.append(add_image(annotated_image, 160 * mm))
        story.append(Spacer(1, 5 * mm))

    story.append(
        P(
            "Annotated output generated by the AI inspection pipeline."
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 5. DEFECT REGISTER
    # ========================================================

    story.append(P("5. Defect Register", H1))

    defect_table = [[
        P("<b>ID</b>"),
        P("<b>Type</b>"),
        P("<b>Confidence</b>"),
        P("<b>Location / Box</b>"),
        P("<b>Severity</b>"),
        P("<b>Recommended Action</b>"),
    ]]

    for index, defect in enumerate(detections, start=1):

        confidence = defect.get("confidence")

        if confidence is not None:
            confidence_text = f"{float(confidence) * 100:.2f}%"
        else:
            confidence_text = "N/A"

        box = defect.get("box", "N/A")

        severity = get_severity(defect)

        recommendation = defect.get(
            "recommendation",
            get_recommendation(defect)
        )

        defect_table.append([
            P(f"D-{index:02d}"),
            P(defect.get("type", "N/A").title()),
            P(confidence_text),
            P(str(box)),
            P(severity),
            P(recommendation),
        ])

    story.append(
        make_table(
            defect_table,
            widths=[
                12 * mm,
                25 * mm,
                22 * mm,
                35 * mm,
                18 * mm,
                48 * mm,
            ],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 6. MEASUREMENT REGISTER
    # ========================================================

    story.append(P("6. Defect Measurement Register", H1))

    story.append(
        P(
            "Where available, field measurements should be entered for "
            "crack length, minimum/typical/maximum width, depth, movement, "
            "spalling dimensions, corrosion/exposed reinforcement and leakage."
        )
    )

    measurement_table = [[
        P("<b>ID</b>"),
        P("<b>Length</b>"),
        P("<b>Min Width</b>"),
        P("<b>Typical Width</b>"),
        P("<b>Max Width</b>"),
        P("<b>Depth</b>"),
        P("<b>Movement</b>"),
    ]]

    for index, defect in enumerate(detections, start=1):

        measurement_table.append([
            P(f"D-{index:02d}"),
            P(defect.get("length", "N/A")),
            P(defect.get("min_width_mm", "N/A")),
            P(defect.get("typical_width_mm", "N/A")),
            P(defect.get("max_width_mm", "N/A")),
            P(defect.get("depth_mm", "N/A")),
            P(defect.get("movement_mm", "N/A")),
        ])

    story.append(
        make_table(
            measurement_table,
            widths=[
                15 * mm,
                22 * mm,
                22 * mm,
                25 * mm,
                22 * mm,
                22 * mm,
                22 * mm,
            ],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 7. SEVERITY ASSESSMENT
    # ========================================================

    story.append(P("7. Severity Screening", H1))

    story.append(
        P(
            "The following levels are used as project screening categories. "
            "The screening result should not by itself be interpreted as "
            "a structural capacity or structural failure determination."
        )
    )

    severity_data = [
        [
            P("<b>Level</b>"),
            P("<b>Screening Description</b>"),
            P("<b>Suggested Action</b>"),
        ],
        [
            P("L0"),
            P("No significant distress / stable condition"),
            P("Photograph, map, measure and monitor."),
        ],
        [
            P("L1"),
            P("Low severity / generally stable superficial condition"),
            P("Seal/protect where required and monitor."),
        ],
        [
            P("L2"),
            P("Moderate condition or project limit exceeded"),
            P("Detailed inspection and determine cause."),
        ],
        [
            P("L3"),
            P("High severity or significant distress indicators"),
            P("Engineer assessment and appropriate repair/protection."),
        ],
        [
            P("L4"),
            P("Critical distress indicators"),
            P("Restrict access/load where necessary and obtain immediate engineering assessment."),
        ],
    ]

    story.append(
        make_table(
            severity_data,
            widths=[
                18 * mm,
                75 * mm,
                67 * mm,
            ],
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        P(
            "Final severity should consider the highest credible risk condition "
            "rather than relying only on crack width."
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 8. ROOT CAUSE
    # ========================================================

    story.append(P("8. Root-Cause Assessment", H1))

    cause_data = [
        [P("<b>Possible Cause</b>"), P("<b>Assessment</b>")],
        [P("Shrinkage"), P("To be assessed during field inspection.")],
        [P("Thermal movement"), P("To be assessed during field inspection.")],
        [P("Flexure"), P("To be assessed based on member/location and crack pattern.")],
        [P("Shear"), P("To be assessed based on crack direction and structural location.")],
        [P("Settlement"), P("To be assessed based on movement and structural context.")],
        [P("Corrosion"), P("Consider where rust staining or exposed reinforcement is observed.")],
        [P("Leakage"), P("Consider where dampness or water ingress is observed.")],
        [P("Construction joint"), P("Assess location and construction history.")],
        [P("Overload"), P("Requires engineering assessment and structural context.")],
    ]

    story.append(
        make_table(
            cause_data,
            widths=[55 * mm, 105 * mm],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 9. REPAIR RECOMMENDATION
    # ========================================================

    story.append(P("9. Recommended Action / Repair", H1))

    for index, defect in enumerate(detections, start=1):

        severity = get_severity(defect)

        recommendation = defect.get(
            "recommendation",
            get_recommendation(defect)
        )

        block = [
            P(
                f"<b>D-{index:02d} — "
                f"{defect.get('type', 'Unknown').title()} "
                f"({severity})</b>",
                H2,
            ),
            P(recommendation),
            Spacer(1, 4),
        ]

        story.append(KeepTogether(block))

    story.append(PageBreak())

    # ========================================================
    # 10. MONITORING
    # ========================================================

    story.append(P("10. Monitoring Plan", H1))

    monitoring = [
        [P("<b>Parameter</b>"), P("<b>Record</b>")],
        [P("Baseline photograph"), P("Record before repair/monitoring.")],
        [P("Crack measurement"), P("Record minimum, typical and maximum width where applicable.")],
        [P("Movement"), P("Record measurement over the monitoring period.")],
        [P("Follow-up date"), P(project_info.get("follow_up_date", "To be scheduled."))],
        [P("After photograph"), P("Record after repair or follow-up inspection.")],
    ]

    story.append(
        make_table(
            monitoring,
            widths=[55 * mm, 105 * mm],
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 11. LIMITATIONS
    # ========================================================

    story.append(P("11. Limitations & Engineering Note", H1))

    limitations = [
        "AI detections are intended to support inspection and screening.",
        "AI confidence is not equivalent to structural severity.",
        "Field measurements should be used where measurements are required.",
        "Crack activity, depth, structural significance and root cause require appropriate inspection.",
        "The L0–L4 matrix is a project screening framework.",
        "Final structural acceptance, repair design and structural safety decisions require appropriate engineering verification.",
    ]

    for item in limitations:
        story.append(P("• " + item))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    story.append(
        P(
            "Generated by Neuro Twin Mesh — AI-Assisted Structural "
            "Inspection System",
            CENTER,
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(story)

    return output_path