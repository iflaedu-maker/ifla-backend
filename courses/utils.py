from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from django.conf import settings
from io import BytesIO
import os
from datetime import datetime


def generate_certificate_pdf(certificate):
    """Generate a PDF certificate for the student"""
    enrollment = certificate.enrollment
    user = enrollment.user
    course_level = enrollment.course_level
    language = course_level.language
    
    # Get student name
    student_name = f"{user.first_name} {user.last_name}".strip() or user.email
    
    # Create buffer for PDF
    buffer = BytesIO()
    
    # Create the PDF object
    pdf_file = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define custom styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Name style
    name_style = ParagraphStyle(
        'CustomName',
        parent=styles['Normal'],
        fontSize=28,
        textColor=colors.HexColor('#5856D6'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Body style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Certificate number style
    cert_num_style = ParagraphStyle(
        'CustomCertNum',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#95a5a6'),
        spaceAfter=0,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    # Add content
    elements.append(Spacer(1, 1.5*inch))
    
    # Certificate Title
    elements.append(Paragraph("CERTIFICATE OF COMPLETION", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Subtitle
    elements.append(Paragraph("This is to certify that", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Student Name
    elements.append(Paragraph(student_name, name_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Certificate Text
    language_display = f"{language.flag_emoji if language.flag_emoji else ''} {language.name} - {course_level.get_level_display()}"
    cert_text = f"""
    has successfully completed the course<br/>
    <b>{language_display}</b><br/>
    offered by International Foreign Language Academy (IFLA)
    """
    elements.append(Paragraph(cert_text, body_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Date
    date_str = certificate.issued_date.strftime("%B %d, %Y")
    elements.append(Paragraph(f"Dated: {date_str}", body_style))
    elements.append(Spacer(1, 0.6*inch))
    
    # Certificate Number
    elements.append(Paragraph(f"Certificate Number: {certificate.certificate_number}", cert_num_style))
    
    # Build PDF
    pdf_file.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Save to file
    filename = f"certificate_{certificate.certificate_number}_{user.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write PDF bytes to file
    with open(file_path, 'wb') as f:
        f.write(pdf_bytes)
    
    # Return relative path for FileField
    return f'certificates/{filename}'

