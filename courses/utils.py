from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
import os
from datetime import datetime


def generate_certificate_pdf(certificate):
    """Generate a PDF certificate for the student.
    If a template file named 'PDF.pdf' exists at project root, overlay dynamic fields on it.
    Otherwise, fall back to the styled ReportLab document.
    """
    enrollment = certificate.enrollment
    user = enrollment.user
    course_level = enrollment.course_level
    language = course_level.language
    
    # Get student name
    student_name = f"{user.first_name} {user.last_name}".strip() or user.email
    
    # Output filename and path
    filename = f"certificate_{certificate.certificate_number}_{user.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # If template exists, overlay text on it
    template_path = os.path.join(settings.BASE_DIR, 'PDF.pdf')
    if os.path.exists(template_path):
        # Read template to get page size
        reader = PdfReader(template_path)
        first_page = reader.pages[0]
        media_box = first_page.mediabox
        page_width = float(media_box.width)
        page_height = float(media_box.height)

        # Create overlay PDF in memory
        overlay_buffer = BytesIO()
        c = rl_canvas.Canvas(overlay_buffer, pagesize=(page_width, page_height))

        # Try to register Montserrat fonts if present
        try:
            fonts_base = os.path.join(settings.BASE_DIR, 'static', 'fonts')
            montserrat_regular = os.path.join(fonts_base, 'Montserrat-Regular.ttf')
            montserrat_bold = os.path.join(fonts_base, 'Montserrat-Bold.ttf')
            if os.path.exists(montserrat_regular):
                pdfmetrics.registerFont(TTFont('Montserrat', montserrat_regular))
            if os.path.exists(montserrat_bold):
                pdfmetrics.registerFont(TTFont('Montserrat-Bold', montserrat_bold))
        except Exception:
            # Ignore font registration errors and fallback to Helvetica
            pass

        # Text values
        language_display = f"{language.flag_emoji if language.flag_emoji else ''} {language.name}"
        level_display = course_level.get_level_display()
        lang_level_line = f"{language_display}  •  {level_display}"
        date_str = certificate.issued_date.strftime("%B %d, %Y")

        # Choose positions (adjusted to match provided mockup)
        # Origin is bottom-left; tweak percentages as needed after preview.
        name_x, name_y = page_width * 0.50, page_height * 0.565   # slightly lower than before
        langlevel_x, langlevel_y = page_width * 0.45, page_height * 0.400  # one centered line
        date_x, date_y = page_width * 0.48, page_height * 0.350  # bottom-right label area

        # Draw centered strings
        c.setFillColorRGB(0.10, 0.10, 0.10)
        # Pick Montserrat if registered, else Helvetica
        try:
            c.setFont("Montserrat-Bold", 28)
        except Exception:
            c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(name_x, name_y, student_name)

        try:
            c.setFont("Montserrat", 16)
        except Exception:
            c.setFont("Helvetica", 16)
        c.drawCentredString(langlevel_x, langlevel_y, lang_level_line)

        try:
            c.setFont("Montserrat", 12)
        except Exception:
            c.setFont("Helvetica", 12)
        c.drawCentredString(date_x, date_y, date_str)

        c.showPage()
        c.save()

        # Merge overlay onto template
        overlay_buffer.seek(0)
        overlay_pdf = PdfReader(overlay_buffer)
        overlay_page = overlay_pdf.pages[0]

        writer = PdfWriter()
        base_page = reader.pages[0]
        base_page.merge_page(overlay_page)
        writer.add_page(base_page)

        with open(file_path, 'wb') as out_f:
            writer.write(out_f)

        return f'certificates/{filename}'

    # Fallback: build a styled certificate without background
    buffer = BytesIO()
    pdf_file = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
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
    
    # Write PDF bytes to file
    with open(file_path, 'wb') as f:
        f.write(pdf_bytes)
    
    # Return relative path for FileField
    return f'certificates/{filename}'

