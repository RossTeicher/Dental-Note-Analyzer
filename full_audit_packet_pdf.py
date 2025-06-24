
from fpdf import FPDF

def generate_audit_packet_pdf(soap, consent, scary, education, compliance):
    class FullAuditPDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Dental Note Analyzer - Full Audit Packet", ln=True, align="C")

        def add_section(self, title, content):
            self.set_font("Arial", "B", 12)
            self.ln(10)
            self.cell(0, 10, title, ln=True)
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 10, content)
            self.ln()

    pdf = FullAuditPDF()
    pdf.add_page()
    pdf.add_section("SOAP Note", soap)
    pdf.add_section("Consent Text", consent)
    pdf.add_section("Patient Education Summary", education)
    pdf.add_section("Scary Note - What Happens If You Do Nothing", scary)
    pdf.add_section("Compliance Audit Summary", compliance)

    pdf_path = "/mnt/data/Full_Audit_Packet.pdf"
    pdf.output(pdf_path)
    return pdf_path
