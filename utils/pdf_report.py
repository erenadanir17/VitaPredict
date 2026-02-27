"""PDF report generator for VitaPredict"""
from fpdf import FPDF
from datetime import datetime
import io


class VitaPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(139, 92, 246)
        self.cell(0, 12, "VitaPredict Rapor", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, datetime.now().strftime("%d.%m.%Y %H:%M"), align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_draw_color(139, 92, 246)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, "Bu rapor bilgilendirme amaclidir, tibbi tavsiye yerine gecmez.", align="C")


def generate_pdf(report, profile=None):
    pdf = VitaPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Profile
    if profile and (profile.get("age") or profile.get("gender") != "Secilmedi"):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(139, 92, 246)
        pdf.cell(0, 8, "Kisisel Profil", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        parts = []
        if profile.get("age"):
            parts.append(f"Yas: {profile['age']}")
        if profile.get("gender") and profile["gender"] != "Secilmedi":
            parts.append(f"Cinsiyet: {profile['gender']}")
        if profile.get("lifestyle"):
            parts.append(f"Faktorler: {', '.join(profile['lifestyle'])}")
        pdf.cell(0, 6, "  |  ".join(parts), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # Summary
    n_def = report["count_deficient"]
    n_norm = report["count_normal"]
    n_total = report["count_total"]

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(139, 92, 246)
    pdf.cell(0, 8, "Ozet", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, report.get("summary", f"{n_total} vitamin girildi, {n_def} eksik, {n_norm} normal."))
    pdf.ln(3)

    # Deficient vitamins
    if report["deficient"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(220, 50, 50)
        pdf.cell(0, 8, "Eksik / Sinirda Vitaminler", new_x="LMARGIN", new_y="NEXT")

        for v in sorted(report["deficient"], key=lambda x: -x["severity_score"]):
            pdf.set_font("Helvetica", "B", 9)
            sc = v["status_label"]
            if v["status"] == "urgent":
                pdf.set_text_color(220, 50, 50)
            elif v["status"] == "critical":
                pdf.set_text_color(200, 130, 0)
            elif v["status"] == "borderline":
                pdf.set_text_color(59, 130, 246)
            else:
                pdf.set_text_color(180, 140, 0)
            pdf.cell(0, 6, f"{v['letter']} | {v['name']}: {v['value']} {v['unit']}  [{sc}]", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 4, f"   Normal aralik: {v['min_normal']} - {v['max_normal']} {v['unit']}", new_x="LMARGIN", new_y="NEXT")

            # Supplement recommendation
            supp = v.get("supplement")
            if supp:
                pdf.set_text_color(45, 140, 120)
                pdf.cell(0, 4, f"   Takviye: {supp['dose']} | {supp['form']} | {supp['timing']}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)

    # Normal vitamins
    if report["normal"]:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(34, 197, 94)
        pdf.cell(0, 8, "Normal Vitaminler", new_x="LMARGIN", new_y="NEXT")

        for v in report["normal"]:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 5, f"{v['letter']} | {v['name']}: {v['value']} {v['unit']}  [NORMAL]", new_x="LMARGIN", new_y="NEXT")

    # Affected systems
    if report["affected_systems"]:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(139, 92, 246)
        pdf.cell(0, 8, "Etkilenen Sistemler", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 5, ", ".join(report["affected_systems"]), new_x="LMARGIN", new_y="NEXT")

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()
