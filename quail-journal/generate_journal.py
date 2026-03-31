from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from datetime import datetime

# Journal specs
PAGE_WIDTH = 6 * inch
PAGE_HEIGHT = 9 * inch
MARGIN = 0.5 * inch

class QuailJournal:
    def __init__(self, filename="Quail_Journal_Interior.pdf"):
        self.c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT
        
    def add_page_number(self, page_num):
        self.c.setFont("Helvetica", 9)
        self.c.drawRightString(self.width - MARGIN, 0.3 * inch, str(page_num))
        
    def title_page(self):
        """Page 1: Title Page"""
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawCentredString(self.width/2, self.height - 2*inch, "THE QUAIL")
        self.c.drawCentredString(self.width/2, self.height - 2.5*inch, "KEEPER'S JOURNAL")
        
        self.c.setFont("Helvetica", 12)
        self.c.drawCentredString(self.width/2, self.height - 3.5*inch, 
                                  "A Comprehensive Record Book for")
        self.c.drawCentredString(self.width/2, self.height - 3.8*inch, 
                                  "Coturnix Quail Breeding")
        
        # Decorative line
        self.c.setStrokeColor(colors.HexColor("#667eea"))
        self.c.setLineWidth(2)
        self.c.line(MARGIN, self.height - 4.5*inch, self.width - MARGIN, self.height - 4.5*inch)
        
        self.c.setFont("Helvetica", 10)
        self.c.drawCentredString(self.width/2, 1.5*inch, "M4Quick Quail Farm")
        self.c.showPage()
        
    def introduction_page(self):
        """Page 2: Introduction"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawString(MARGIN, self.height - MARGIN - 0.3*inch, "Welcome!")
        
        self.c.setFont("Helvetica", 10)
        y = self.height - MARGIN - 0.8*inch
        intro_text = [
            "This journal will help you track every aspect of your",
            "quail breeding operation, from daily egg production to",
            "hatch rates and health records.",
            "",
            "How to Use This Journal:",
            "",
            "• Daily Egg Log - Record eggs laid each day",
            "• Hatch Records - Track incubation success",
            "• Health Notes - Monitor treatments and issues",  
            "• Breeding Pairs - Follow bloodlines",
            "• Expenses - Calculate your true costs",
            "",
            "Happy hatching! 🐣",
        ]
        
        for line in intro_text:
            self.c.drawString(MARGIN, y, line)
            y -= 0.25*inch
            
        self.c.showPage()
        
    def quick_reference(self):
        """Page 3-4: Quick Reference"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, "Quick Reference Guide")
        
        self.c.setFont("Helvetica-Bold", 11)
        y = self.height - MARGIN - 0.8*inch
        
        refs = [
            ("Incubation Period:", "17-18 days"),
            ("Temperature:", "99.5°F (forced air)"),
            ("Humidity Days 1-14:", "45-50%"),
            ("Humidity Lockdown:", "70%+"),
            ("Brooder Week 1:", "95°F"),
            ("Brooder Week 2:", "90°F"),
            ("Brooder Week 3:", "85°F"),
            ("Starter Feed:", "20-24% protein"),
            ("Grower Feed:", "18-20% protein"),
            ("Layer Feed:", "16-18% protein + calcium"),
        ]
        
        for label, value in refs:
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(MARGIN, y, label)
            self.c.setFont("Helvetica", 10)
            self.c.drawString(MARGIN + 1.8*inch, y, value)
            y -= 0.35*inch
            
        self.c.setFont("Helvetica-Oblique", 9)
        self.c.drawString(MARGIN, 1*inch, "Note: Reduce brooder temp by 5°F each week until 70°F")
        
        self.c.showPage()
        
    def flock_overview(self):
        """Page 5-6: Flock Overview"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, "My Flock")
        
        fields = [
            ("Flock Start Date:", ""),
            ("Number of Birds:", ""),
            ("Breeds:", ""),
            ("Coop/Setup:", ""),
            ("Feed Brand:", ""),
            ("Notes:", ""),
        ]
        
        y = self.height - MARGIN - 1*inch
        for label, _ in fields:
            self.c.setFont("Helvetica-Bold", 11)
            self.c.drawString(MARGIN, y, label)
            
            # Draw line for writing
            self.c.setStrokeColor(colors.grey)
            self.c.line(MARGIN + 1.5*inch, y, self.width - MARGIN, y)
            
            y -= 0.6*inch
            
        self.c.showPage()
        
    def daily_egg_log(self, month_num):
        """Daily egg production log page"""
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, f"Egg Production - Month {month_num}")
        
        self.c.setFont("Helvetica", 9)
        self.c.drawString(MARGIN, self.height - MARGIN - 0.6*inch, "Week of: _______________")
        
        # Table header
        headers = ["Day", "Bird/Group", "Eggs", "Notes"]
        col_widths = [0.6*inch, 1.2*inch, 0.6*inch, 2.6*inch]
        
        y_start = self.height - MARGIN - 1*inch
        y = y_start
        
        # Draw table
        self.c.setFont("Helvetica-Bold", 9)
        x = MARGIN
        for i, h in enumerate(headers):
            self.c.drawString(x + 0.1*inch, y, h)
            x += col_widths[i]
        
        y -= 0.25*inch
        
        # Draw rows for each day
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.c.setFont("Helvetica", 9)
        
        for day in days:
            x = MARGIN
            # Day column
            self.c.drawString(x + 0.1*inch, y, day)
            x += col_widths[0]
            
            # Draw lines for other columns
            for i in range(3):
                self.c.setStrokeColor(colors.lightgrey)
                self.c.line(x, y - 0.15*inch, x + col_widths[i+1] - 0.1*inch, y - 0.15*inch)
                x += col_widths[i+1]
            
            y -= 0.35*inch
        
        # Weekly total
        y -= 0.1*inch
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(MARGIN, y, "Weekly Total: _______ eggs")
        y -= 0.3*inch
        self.c.drawString(MARGIN, y, "Monthly Total: _______ eggs")
        
        self.c.showPage()
        
    def hatch_record(self, hatch_num):
        """Hatch record page"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, f"Hatch Record #{hatch_num}")
        
        fields = [
            ("Incubator:", ""),
            ("Start Date:", ""),
            ("Lockdown:", ""),
            ("Hatch Date:", ""),
        ]
        
        y = self.height - MARGIN - 0.8*inch
        for label, _ in fields:
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(MARGIN, y, label)
            self.c.setStrokeColor(colors.lightgrey)
            self.c.line(MARGIN + 1.2*inch, y, self.width - MARGIN, y)
            y -= 0.4*inch
        
        # Stats boxes
        y -= 0.1*inch
        stats = [
            ("Eggs Set:", "Fertile:", "Hatched:", "Rate:")
        ]
        
        x = MARGIN
        for stat in stats[0]:
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(x, y, stat)
            self.c.setStrokeColor(colors.lightgrey)
            self.c.line(x, y - 0.1*inch, x + 0.7*inch, y - 0.1*inch)
            x += 1.1*inch
        
        # Egg tracking table
        y -= 0.6*inch
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(MARGIN, y, "Egg Tracking:")
        y -= 0.25*inch
        
        headers = ["#", "Breed", "Dam", "Sire", "Result"]
        col_widths = [0.4*inch, 1.2*inch, 1*inch, 1*inch, 1.4*inch]
        
        x = MARGIN
        for h in headers:
            self.c.drawString(x + 0.05*inch, y, h)
            x += 1
        
        # Lines for 12 eggs
        y -= 0.2*inch
        for i in range(12):
            x = MARGIN
            self.c.drawString(x + 0.05*inch, y, str(i+1))
            x += col_widths[0]
            
            for j in range(4):
                self.c.setStrokeColor(colors.lightgrey)
                self.c.line(x, y - 0.05*inch, x + col_widths[j+1] - 0.1*inch, y - 0.05*inch)
                x += col_widths[j+1]
            
            y -= 0.25*inch
        
        # Notes
        y -= 0.1*inch
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(MARGIN, y, "Notes:")
        y -= 0.15*inch
        for _ in range(3):
            self.c.setStrokeColor(colors.lightgrey)
            self.c.line(MARGIN, y, self.width - MARGIN, y)
            y -= 0.25*inch
        
        self.c.showPage()
        
    def health_log(self):
        """Health tracking page"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, "Health & Treatment Log")
        
        headers = ["Date", "Bird ID", "Symptoms", "Treatment", "Result"]
        col_widths = [0.8*inch, 0.8*inch, 1.3*inch, 1.3*inch, 0.8*inch]
        
        y = self.height - MARGIN - 0.8*inch
        
        # Header row
        x = MARGIN
        self.c.setFont("Helvetica-Bold", 8)
        for h in headers:
            self.c.drawString(x + 0.05*inch, y, h)
            x += col_widths[0]
        
        y -= 0.25*inch
        
        # Data rows
        self.c.setFont("Helvetica", 8)
        for _ in range(8):
            x = MARGIN
            for i in range(5):
                self.c.setStrokeColor(colors.lightgrey)
                self.c.line(x, y - 0.15*inch, x + col_widths[0] - 0.05*inch, y - 0.15*inch)
                x += col_widths[0]
            y -= 0.35*inch
        
        self.c.showPage()
        
    def breeding_tracker(self):
        """Breeding pair tracking"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, "Breeding Pair Tracker")
        
        fields = [
            ("Pair ID:", ""),
            ("Dam (Female):", ""),
            ("Sire (Male):", ""),
        ]
        
        y = self.height - MARGIN - 0.8*inch
        for label, _ in fields:
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(MARGIN, y, label)
            self.c.setStrokeColor(colors.lightgrey)
            self.c.line(MARGIN + 1.3*inch, y, self.width - MARGIN, y)
            y -= 0.4*inch
        
        # Offspring table
        y -= 0.2*inch
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(MARGIN, y, "Offspring Record:")
        y -= 0.3*inch
        
        headers = ["Hatch Date", "# Eggs", "# Chicks", "Notes"]
        col_widths = [1.1*inch, 0.7*inch, 0.7*inch, 2.2*inch]
        
        x = MARGIN
        for h in headers:
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawString(x + 0.05*inch, y, h)
            x += col_widths[0]
        
        y -= 0.25*inch
        
        # Data rows
        for _ in range(6):
            x = MARGIN
            for i in range(4):
                self.c.setStrokeColor(colors.lightgrey)
                self.c.line(x, y - 0.1*inch, x + col_widths[i] - 0.05*inch, y - 0.1*inch)
                x += col_widths[i]
            y -= 0.3*inch
        
        # Total
        y -= 0.1*inch
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(MARGIN, y, "Total Offspring: ______")
        
        self.c.showPage()
        
    def expense_tracker(self):
        """Expense tracking page"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, "Expense Tracker")
        
        headers = ["Date", "Item", "Qty", "Each", "Total"]
        col_widths = [0.7*inch, 1.8*inch, 0.5*inch, 0.7*inch, 0.7*inch]
        
        y = self.height - MARGIN - 0.8*inch
        
        # Header
        x = MARGIN
        self.c.setFont("Helvetica-Bold", 9)
        for h in headers:
            self.c.drawString(x + 0.05*inch, y, h)
            x += col_widths[0]
        
        y -= 0.25*inch
        
        # Data rows
        for _ in range(10):
            x = MARGIN
            for i in range(5):
                self.c.setStrokeColor(colors.lightgrey)
                self.c.line(x, y - 0.12*inch, x + col_widths[i] - 0.05*inch, y - 0.12*inch)
                x += col_widths[i]
            y -= 0.28*inch
        
        # Totals
        y -= 0.15*inch
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawRightString(self.width - MARGIN, y, "Total Expenses: $_______")
        y -= 0.3*inch
        self.c.drawRightString(self.width - MARGIN, y, "Total Revenue:  $_______")
        y -= 0.3*inch
        self.c.setStrokeColor(colors.HexColor("#667eea"))
        self.c.setLineWidth(1)
        self.c.line(self.width - 2.2*inch, y - 0.05*inch, self.width - MARGIN, y - 0.05*inch)
        y -= 0.15*inch
        self.c.drawRightString(self.width - MARGIN, y, "NET: $_______")
        
        self.c.showPage()
        
    def notes_page(self):
        """Blank notes page with lines"""
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(self.width/2, self.height - MARGIN - 0.3*inch, "Notes & Ideas")
        
        y = self.height - MARGIN - 0.8*inch
        
        # Draw lines
        self.c.setStrokeColor(colors.lightgrey)
        for _ in range(20):
            self.c.line(MARGIN, y, self.width - MARGIN, y)
            y -= 0.35*inch
        
        self.c.showPage()
        
    def generate(self):
        """Generate the full journal"""
        # Static pages
        self.title_page()
        self.introduction_page()
        self.quick_reference()
        self.flock_overview()
        
        # Monthly egg logs (12 months x 4 weeks = 48 pages, use 50 for buffer)
        for month in range(1, 13):
            for week in range(1, 5):
                self.daily_egg_log(f"{month}.{week}")
        
        # Hatch records (10 pages)
        for i in range(1, 11):
            self.hatch_record(i)
        
        # Health logs (5 pages)
        for _ in range(5):
            self.health_log()
        
        # Breeding trackers (5 pages)
        for _ in range(5):
            self.breeding_tracker()
        
        # Expense tracker (2 pages)
        for _ in range(2):
            self.expense_tracker()
        
        # Notes pages (3)
        for _ in range(3):
            self.notes_page()
        
        # Page numbers (add manually after)
        self.c.save()
        print(f"Journal generated: Quail_Journal_Interior.pdf")
        
if __name__ == "__main__":
    journal = QuailJournal()
    journal.generate()
