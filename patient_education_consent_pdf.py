
from fpdf import FPDF

def generate_consent_pdf(education, scary_note):
    class PatientEducationPDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Your Treatment Options & What Happens If You Wait", ln=True, align="C")

        def chapter_title(self, title):
            self.set_font("Arial", "B", 12)
            self.ln(10)
            self.cell(0, 10, title, ln=True)

        def chapter_body(self, body):
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 10, body)
            self.ln()

        def add_section(self, title, body):
            self.chapter_title(title)
            self.chapter_body(body)

    pdf = PatientEducationPDF()
    pdf.add_page()
    pdf.add_section("Why This Treatment Was Recommended for You", education)
    pdf.add_section("What Could Happen If You Wait or Do Nothing", scary_note)

    pdf_path = "/mnt/data/Treatment_Options_And_Risks.pdf"
    pdf.output(pdf_path)
    return pdf_path
