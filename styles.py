
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


# defining the styles to be used in the report
styles = getSampleStyleSheet()

titleStyle = ParagraphStyle(
    name="Title",
    fontName="Helvetica-Bold",
    fontSize=58,
    textColor=colors.HexColor('#9788EF'),
    alignment=2,
    spaceAfter=inch/2
)

sectionHeaderStyle = ParagraphStyle(
    name="SectionHeader",
    fontName="Helvetica-Bold",
    fontSize=20,
    textColor=colors.HexColor('#6D8E75'),
    spaceBefore=inch/2,
    spaceAfter=inch/4
)

subheaderStyle = ParagraphStyle(
    name="Subheader",
    fontName="Helvetica-Bold",
    fontSize=14,
    textColor=colors.HexColor('#6D8E75'),
    spaceBefore=inch/4,
    spaceAfter=inch/8
)

bodyStyle = ParagraphStyle(
    name="Body",
    fontName="Helvetica",
    fontSize=14,
    textColor=colors.HexColor('#1F1F1F'),
    spaceBefore=inch/8,
    spaceAfter=inch/8
)