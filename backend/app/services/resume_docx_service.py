"""
DOCX Export Service for Elevate X AI Resume Generator.
Generates beautifully formatted, clean Word (.docx) documents from structured resume data.
"""

import io
from typing import Dict, Any
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from app.schemas.resume_generator import ResumeFullData


class ResumeDocxService:
    @classmethod
    def _add_section_heading(cls, doc: Document, title: str, color_rgb=(23, 35, 63)):
        """Adds a standardized section heading with a bottom border or underline."""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True

        run = p.add_run(title.upper())
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(*color_rgb)

        # Add thin horizontal rule below heading
        pBdr = parse_xml(r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                         r'<w:bottom w:val="single" w:sz="6" w:space="1" w:color="D6A84B"/>'
                         r'</w:pBdr>')
        p._p.get_or_add_pPr().append(pBdr)

    @classmethod
    def generate_docx(cls, resume_data: ResumeFullData) -> io.BytesIO:
        """
        Converts ResumeFullData into an ATS-compliant, beautifully styled Word document.
        Returns a BytesIO stream ready for streaming response.
        """
        doc = Document()

        # Set 0.6 inch margins for professional dense layout
        sections = doc.sections
        for s in sections:
            s.top_margin = Inches(0.6)
            s.bottom_margin = Inches(0.6)
            s.left_margin = Inches(0.65)
            s.right_margin = Inches(0.65)

        # Parse accent color
        hex_col = (resume_data.accentColor or "#17233F").lstrip("#")
        if len(hex_col) == 6:
            accent_rgb = (int(hex_col[0:2], 16), int(hex_col[2:4], 16), int(hex_col[4:6], 16))
        else:
            accent_rgb = (23, 35, 63)

        info = resume_data.personalInfo

        # 1. Header: Full Name
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(0)
        title_p.paragraph_format.space_after = Pt(2)
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        name_run = title_p.add_run(info.fullName or "Candidate Name")
        name_run.bold = True
        name_run.font.size = Pt(20)
        name_run.font.name = "Calibri"
        name_run.font.color.rgb = RGBColor(*accent_rgb)

        # Professional Title
        if info.professionalTitle:
            sub_p = doc.add_paragraph()
            sub_p.paragraph_format.space_before = Pt(0)
            sub_p.paragraph_format.space_after = Pt(4)
            sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            sub_run = sub_p.add_run(info.professionalTitle)
            sub_run.font.size = Pt(11)
            sub_run.font.name = "Calibri"
            sub_run.font.color.rgb = RGBColor(104, 113, 135)

        # Contact Info Line
        contact_parts = []
        if info.email:
            contact_parts.append(info.email)
        if info.phone:
            contact_parts.append(info.phone)
        if info.location:
            contact_parts.append(info.location)
        if info.linkedIn:
            contact_parts.append(f"LinkedIn: {info.linkedIn}")
        if info.gitHub:
            contact_parts.append(f"GitHub: {info.gitHub}")
        if info.portfolio:
            contact_parts.append(f"Portfolio: {info.portfolio}")

        if contact_parts:
            contact_p = doc.add_paragraph()
            contact_p.paragraph_format.space_before = Pt(0)
            contact_p.paragraph_format.space_after = Pt(8)
            contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            contact_run = contact_p.add_run("  •  ".join(contact_parts))
            contact_run.font.size = Pt(9)
            contact_run.font.name = "Calibri"
            contact_run.font.color.rgb = RGBColor(70, 75, 85)

        # 2. Professional Summary
        if info.summary and info.summary.strip():
            cls._add_section_heading(doc, "Professional Summary", accent_rgb)
            sum_p = doc.add_paragraph()
            sum_p.paragraph_format.space_before = Pt(2)
            sum_p.paragraph_format.space_after = Pt(6)
            sum_run = sum_p.add_run(info.summary.strip())
            sum_run.font.size = Pt(10)
            sum_run.font.name = "Calibri"

        # 3. Technical Skills
        skills = resume_data.skills
        has_skills = any([
            skills.programmingLanguages,
            skills.frameworks,
            skills.databases,
            skills.developerTools,
            skills.aiMlSkills,
            skills.otherSkills,
        ])
        if has_skills:
            cls._add_section_heading(doc, "Technical Skills", accent_rgb)
            categories = [
                ("Languages", skills.programmingLanguages),
                ("Frameworks & Libraries", skills.frameworks),
                ("Databases & Storage", skills.databases),
                ("Developer Tools & Cloud", skills.developerTools),
                ("AI & Machine Learning", skills.aiMlSkills),
                ("Other Competencies", skills.otherSkills),
            ]
            for cat_label, cat_items in categories:
                if cat_items:
                    sk_p = doc.add_paragraph()
                    sk_p.paragraph_format.space_before = Pt(1)
                    sk_p.paragraph_format.space_after = Pt(2)
                    lbl_run = sk_p.add_run(f"{cat_label}: ")
                    lbl_run.bold = True
                    lbl_run.font.size = Pt(9.5)
                    lbl_run.font.name = "Calibri"

                    items_run = sk_p.add_run(", ".join(cat_items))
                    items_run.font.size = Pt(9.5)
                    items_run.font.name = "Calibri"

        # 4. Work Experience
        if resume_data.experience:
            cls._add_section_heading(doc, "Work Experience", accent_rgb)
            for exp in resume_data.experience:
                p_head = doc.add_paragraph()
                p_head.paragraph_format.space_before = Pt(4)
                p_head.paragraph_format.space_after = Pt(1)
                p_head.paragraph_format.keep_with_next = True

                # Role and Company
                r_run = p_head.add_run(exp.role)
                r_run.bold = True
                r_run.font.size = Pt(10.5)
                r_run.font.name = "Calibri"

                comp_run = p_head.add_run(f" | {exp.company}")
                comp_run.bold = True
                comp_run.font.size = Pt(10.5)
                comp_run.font.color.rgb = RGBColor(104, 113, 135)
                comp_run.font.name = "Calibri"

                # Dates & Location
                date_str = f"{exp.startDate} – {exp.endDate or 'Present'}"
                if exp.location:
                    date_str += f" ({exp.location})"
                
                # Align dates right or as a subtitle
                sub_p = doc.add_paragraph()
                sub_p.paragraph_format.space_before = Pt(0)
                sub_p.paragraph_format.space_after = Pt(3)
                sub_run = sub_p.add_run(date_str)
                sub_run.font.size = Pt(9)
                sub_run.font.italic = True
                sub_run.font.color.rgb = RGBColor(120, 125, 135)

                for bullet in exp.responsibilities:
                    if bullet and bullet.strip():
                        b_p = doc.add_paragraph(style='List Bullet')
                        b_p.paragraph_format.space_before = Pt(0)
                        b_p.paragraph_format.space_after = Pt(2)
                        b_run = b_p.add_run(bullet.strip())
                        b_run.font.size = Pt(9.5)
                        b_run.font.name = "Calibri"

        # 5. Internships
        if resume_data.internships:
            cls._add_section_heading(doc, "Internships & Practical Training", accent_rgb)
            for intern in resume_data.internships:
                p_head = doc.add_paragraph()
                p_head.paragraph_format.space_before = Pt(4)
                p_head.paragraph_format.space_after = Pt(1)
                p_head.paragraph_format.keep_with_next = True

                r_run = p_head.add_run(intern.role)
                r_run.bold = True
                r_run.font.size = Pt(10.5)
                r_run.font.name = "Calibri"

                org_run = p_head.add_run(f" | {intern.organization}")
                org_run.bold = True
                org_run.font.size = Pt(10.5)
                org_run.font.color.rgb = RGBColor(104, 113, 135)
                org_run.font.name = "Calibri"

                if intern.duration:
                    sub_p = doc.add_paragraph()
                    sub_p.paragraph_format.space_before = Pt(0)
                    sub_p.paragraph_format.space_after = Pt(3)
                    sub_run = sub_p.add_run(intern.duration)
                    sub_run.font.size = Pt(9)
                    sub_run.font.italic = True
                    sub_run.font.color.rgb = RGBColor(120, 125, 135)

                for item in intern.workPerformed + intern.achievements:
                    if item and item.strip():
                        b_p = doc.add_paragraph(style='List Bullet')
                        b_p.paragraph_format.space_before = Pt(0)
                        b_p.paragraph_format.space_after = Pt(2)
                        b_run = b_p.add_run(item.strip())
                        b_run.font.size = Pt(9.5)
                        b_run.font.name = "Calibri"

        # 6. Projects
        if resume_data.projects:
            cls._add_section_heading(doc, "Technical Projects", accent_rgb)
            for proj in resume_data.projects:
                p_head = doc.add_paragraph()
                p_head.paragraph_format.space_before = Pt(4)
                p_head.paragraph_format.space_after = Pt(1)
                p_head.paragraph_format.keep_with_next = True

                p_run = p_head.add_run(proj.title)
                p_run.bold = True
                p_run.font.size = Pt(10.5)
                p_run.font.name = "Calibri"

                if proj.technologies:
                    tech_run = p_head.add_run(f" [{', '.join(proj.technologies)}]")
                    tech_run.font.size = Pt(9)
                    tech_run.font.color.rgb = RGBColor(115, 85, 217)

                urls = []
                if proj.githubUrl:
                    urls.append(f"GitHub: {proj.githubUrl}")
                if proj.projectUrl:
                    urls.append(f"Live: {proj.projectUrl}")
                if urls:
                    u_p = doc.add_paragraph()
                    u_p.paragraph_format.space_before = Pt(0)
                    u_p.paragraph_format.space_after = Pt(2)
                    u_run = u_p.add_run("  |  ".join(urls))
                    u_run.font.size = Pt(8.5)
                    u_run.font.color.rgb = RGBColor(100, 100, 110)

                if proj.description:
                    d_p = doc.add_paragraph()
                    d_p.paragraph_format.space_before = Pt(0)
                    d_p.paragraph_format.space_after = Pt(2)
                    d_run = d_p.add_run(proj.description)
                    d_run.font.size = Pt(9.5)
                    d_run.font.name = "Calibri"

                for bullet in proj.contributions:
                    if bullet and bullet.strip():
                        b_p = doc.add_paragraph(style='List Bullet')
                        b_p.paragraph_format.space_before = Pt(0)
                        b_p.paragraph_format.space_after = Pt(2)
                        b_run = b_p.add_run(bullet.strip())
                        b_run.font.size = Pt(9.5)
                        b_run.font.name = "Calibri"

        # 7. Education
        if resume_data.education:
            cls._add_section_heading(doc, "Education", accent_rgb)
            for edu in resume_data.education:
                p_head = doc.add_paragraph()
                p_head.paragraph_format.space_before = Pt(3)
                p_head.paragraph_format.space_after = Pt(1)
                p_head.paragraph_format.keep_with_next = True

                deg_run = p_head.add_run(f"{edu.degree} in {edu.fieldOfStudy}")
                deg_run.bold = True
                deg_run.font.size = Pt(10)
                deg_run.font.name = "Calibri"

                inst_run = p_head.add_run(f" | {edu.institution}")
                inst_run.font.size = Pt(10)
                inst_run.font.color.rgb = RGBColor(104, 113, 135)

                date_grade = f"{edu.startDate} – {edu.endDate}"
                if edu.grade:
                    date_grade += f"  •  Grade: {edu.grade}"
                
                sub_p = doc.add_paragraph()
                sub_p.paragraph_format.space_before = Pt(0)
                sub_p.paragraph_format.space_after = Pt(2)
                sub_run = sub_p.add_run(date_grade)
                sub_run.font.size = Pt(9)
                sub_run.font.italic = True
                sub_run.font.color.rgb = RGBColor(120, 125, 135)

                if edu.coursework:
                    cw_p = doc.add_paragraph()
                    cw_p.paragraph_format.space_before = Pt(0)
                    cw_p.paragraph_format.space_after = Pt(3)
                    cw_lbl = cw_p.add_run("Coursework: ")
                    cw_lbl.font.size = Pt(8.5)
                    cw_lbl.bold = True
                    cw_val = cw_p.add_run(", ".join(edu.coursework))
                    cw_val.font.size = Pt(8.5)

        # 8. Certifications
        if resume_data.certifications:
            cls._add_section_heading(doc, "Certifications", accent_rgb)
            for cert in resume_data.certifications:
                c_p = doc.add_paragraph(style='List Bullet')
                c_p.paragraph_format.space_before = Pt(1)
                c_p.paragraph_format.space_after = Pt(2)
                c_run = c_p.add_run(f"{cert.name} – {cert.issuingOrganization} ({cert.issueDate})")
                c_run.font.size = Pt(9.5)
                if cert.credentialUrl:
                    u_run = c_p.add_run(f" [{cert.credentialUrl}]")
                    u_run.font.size = Pt(8.5)
                    u_run.font.color.rgb = RGBColor(115, 85, 217)

        # 9. Additional Sections
        add = resume_data.additional
        if add.achievements:
            cls._add_section_heading(doc, "Honors & Achievements", accent_rgb)
            for ach in add.achievements:
                p = doc.add_paragraph(style='List Bullet')
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2)
                r = p.add_run(ach)
                r.font.size = Pt(9.5)

        if add.publications:
            cls._add_section_heading(doc, "Publications & Research", accent_rgb)
            for pub in add.publications:
                p = doc.add_paragraph(style='List Bullet')
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2)
                r = p.add_run(pub)
                r.font.size = Pt(9.5)

        if add.languages:
            cls._add_section_heading(doc, "Languages", accent_rgb)
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(", ".join(add.languages))
            r.font.size = Pt(9.5)

        # Save to memory stream
        stream = io.BytesIO()
        doc.save(stream)
        stream.seek(0)
        return stream
