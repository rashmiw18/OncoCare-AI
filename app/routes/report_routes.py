from flask import (
    Blueprint,
    render_template,
    make_response
)

from flask_login import (
    login_required,
    current_user
)

from app.models.health_data import HealthData
from app.models.ai_insight import AIInsight

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from io import BytesIO


report_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports"
)


# =====================================================
# REPORT PAGE
# =====================================================

@report_bp.route("/")
@login_required
def report():

    health_records = (

        HealthData.query

        .filter_by(
            user_id=current_user.id
        )

        .order_by(
            HealthData.recorded_at.desc()
        )

        .all()

    )


    latest_record = (

        health_records[0]

        if health_records

        else None

    )


    latest_insight = (

        AIInsight.query

        .filter_by(
            user_id=current_user.id
        )

        .order_by(
            AIInsight.created_at.desc()
        )

        .first()

    )


    return render_template(

        "report.html",

        health_records=health_records,

        latest_record=latest_record,

        latest_insight=latest_insight

    )


# =====================================================
# DOWNLOAD PDF REPORT
# =====================================================

@report_bp.route("/download")
@login_required
def download_report():

    health_records = (

        HealthData.query

        .filter_by(
            user_id=current_user.id
        )

        .order_by(
            HealthData.recorded_at.desc()
        )

        .all()

    )


    latest_record = (

        health_records[0]

        if health_records

        else None

    )


    latest_insight = (

        AIInsight.query

        .filter_by(
            user_id=current_user.id
        )

        .order_by(
            AIInsight.created_at.desc()
        )

        .first()

    )


    buffer = BytesIO()


    pdf = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=40

    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "TitleStyle",

        parent=styles["Title"],

        fontSize=24,

        alignment=TA_CENTER,

        spaceAfter=20

    )


    heading_style = ParagraphStyle(

        "HeadingStyle",

        parent=styles["Heading2"],

        fontSize=16,

        spaceBefore=15,

        spaceAfter=10

    )


    normal_style = ParagraphStyle(

        "NormalStyle",

        parent=styles["Normal"],

        fontSize=10,

        leading=15

    )


    story = []


    # =================================================
    # TITLE
    # =================================================

    story.append(

        Paragraph(

            "OncoCare AI",

            title_style

        )

    )


    story.append(

        Paragraph(

            "Personal Health Monitoring Report",

            ParagraphStyle(

                "Subtitle",

                parent=styles["Normal"],

                alignment=TA_CENTER,

                fontSize=12

            )

        )

    )


    story.append(

        Spacer(

            1,

            20

        )

    )


    # =================================================
    # PATIENT INFORMATION
    # =================================================

    story.append(

        Paragraph(

            "Patient Information",

            heading_style

        )

    )


    patient_data = [

        [

            "Name",

            current_user.name

        ],

        [

            "Email",

            current_user.email

        ],

        [

            "Report Date",

            __import__(

                "datetime"

            ).datetime.now().strftime(

                "%d %B %Y"

            )

        ]

    ]


    patient_table = Table(

        patient_data,

        colWidths=[

            140,

            350

        ]

    )


    patient_table.setStyle(

        TableStyle([

            (

                "GRID",

                (

                    0,

                    0

                ),

                (

                    -1,

                    -1

                ),

                0.5,

                colors.grey

            ),

            (

                "BACKGROUND",

                (

                    0,

                    0

                ),

                (

                    0,

                    -1

                ),

                colors.lightgrey

            ),

            (

                "PADDING",

                (

                    0,

                    0

                ),

                (

                    -1,

                    -1

                ),

                8

            )

        ])

    )


    story.append(

        patient_table

    )


    # =================================================
    # LATEST HEALTH DATA
    # =================================================

    story.append(

        Paragraph(

            "Latest Health Measurements",

            heading_style

        )

    )


    if latest_record:


        latest_data = [

            [

                "Measurement",

                "Value"

            ],

            [

                "Heart Rate",

                f"{latest_record.heart_rate} BPM"

            ],

            [

                "Blood Oxygen",

                f"{latest_record.spo2}%"

            ],

            [

                "Temperature",

                f"{latest_record.temperature} °F"

            ],

            [

                "Sleep",

                f"{latest_record.sleep_hours} hours"

            ],

            [

                "Fatigue Level",

                f"{latest_record.fatigue_level}/10"

            ],

            [

                "Pain Level",

                f"{latest_record.pain_level}/10"

            ]

        ]


        latest_table = Table(

            latest_data,

            colWidths=[

                250,

                240

            ]

        )


        latest_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        -1

                    ),

                    0.5,

                    colors.grey

                ),

                (

                    "BACKGROUND",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        0

                    ),

                    colors.black

                ),

                (

                    "TEXTCOLOR",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        0

                    ),

                    colors.white

                ),

                (

                    "PADDING",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        -1

                    ),

                    8

                )

            ])

        )


        story.append(

            latest_table

        )


    else:


        story.append(

            Paragraph(

                "No health data available.",

                normal_style

            )

        )


    # =================================================
    # HEALTH HISTORY
    # =================================================

    story.append(

        Paragraph(

            "Health History",

            heading_style

        )

    )


    if health_records:


        history_data = [

            [

                "Date",

                "Heart Rate",

                "SpO₂",

                "Temp",

                "Sleep",

                "Fatigue"

            ]

        ]


        for record in health_records:


            history_data.append([

                record.recorded_at.strftime(

                    "%d %b %Y"

                ),

                f"{record.heart_rate}",

                f"{record.spo2}%",

                f"{record.temperature}°F",

                f"{record.sleep_hours} hrs",

                f"{record.fatigue_level}/10"

            ])


        history_table = Table(

            history_data,

            repeatRows=1,

            colWidths=[

                80,

                80,

                60,

                70,

                70,

                70

            ]

        )


        history_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        -1

                    ),

                    0.4,

                    colors.grey

                ),

                (

                    "BACKGROUND",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        0

                    ),

                    colors.black

                ),

                (

                    "TEXTCOLOR",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        0

                    ),

                    colors.white

                ),

                (

                    "FONTSIZE",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        -1

                    ),

                    8

                ),

                (

                    "PADDING",

                    (

                        0,

                        0

                    ),

                    (

                        -1,

                        -1

                    ),

                    6

                )

            ])

        )


        story.append(

            history_table

        )


    # =================================================
    # AI INSIGHT
    # =================================================

    story.append(

        Paragraph(

            "Latest AI Health Insight",

            heading_style

        )

    )


    if latest_insight:


        story.append(

            Paragraph(

                f"<b>Risk Level:</b> "

                f"{latest_insight.risk_level}",

                normal_style

            )

        )


        story.append(

            Paragraph(

                f"<b>Risk Score:</b> "

                f"{latest_insight.risk_score}",

                normal_style

            )

        )


        story.append(

            Spacer(

                1,

                8

            )

        )


        insight_text = (

            latest_insight.insight_text

            .replace(

                "\n",

                "<br/>"

            )

        )


        story.append(

            Paragraph(

                insight_text,

                normal_style

            )

        )


    else:


        story.append(

            Paragraph(

                "No AI analysis has been generated yet.",

                normal_style

            )

        )


    # =================================================
    # DISCLAIMER
    # =================================================

    story.append(

        Spacer(

            1,

            25

        )

    )


    story.append(

        Paragraph(

            "<b>Disclaimer:</b> This report is generated "

            "using AI-assisted health monitoring and is "

            "intended for informational purposes only. "

            "It does not replace professional medical advice, "

            "diagnosis, or treatment.",

            normal_style

        )

    )


    pdf.build(

        story

    )


    buffer.seek(

        0

    )


    response = make_response(

        buffer.getvalue()

    )


    response.headers["Content-Type"] = (

        "application/pdf"

    )


    response.headers["Content-Disposition"] = (

        "attachment; "

        'filename="OncoCare_Health_Report.pdf"'

    )


    return response