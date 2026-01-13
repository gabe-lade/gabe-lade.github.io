#!/usr/bin/env python3
"""
Generate a Typst CV from YAML data.
Usage: python generate_cv.py cv_data.yaml output.typ
"""

import yaml
import sys
from pathlib import Path


def escape_typst(text: str) -> str:
    """Escape special Typst characters."""
    if text is None:
        return ""
    # Typst special chars need escaping with backslash
    # Order matters: escape backslash first to avoid double-escaping
    text = text.replace('\\', '\\\\')  # Must be first
    text = text.replace('#', '\\#')
    text = text.replace('*', '\\*')
    text = text.replace('_', '\\_')
    text = text.replace('`', '\\`')
    text = text.replace('$', '\\$')
    text = text.replace('@', '\\@')
    text = text.replace('<', '\\<')
    text = text.replace('>', '\\>')
    return text


def format_amount(amount: int) -> str:
    """Format dollar amount with commas."""
    return f"${amount:,}"


def generate_header(data: dict) -> str:
    """Generate the document header."""
    return f'''#import "cv_template.typ": *

#show: cv.with(
  name: "{escape_typst(data['name'])}",
  email: "{data['email']}",
  department: "{escape_typst(data['department'])}",
  institution: "{escape_typst(data['institution'])}",
  address: "{escape_typst(data['address'])}",
)
'''


def generate_positions(positions: list) -> str:
    """Generate the positions section."""
    lines = ['#section("Academic Positions and Affiliations")', '']
    
    for pos in positions:
        dept = f'department: "{escape_typst(pos["department"])}",' if 'department' in pos else ''
        
        roles_str = ", ".join([
            f'(title: "{escape_typst(role["title"])}", years: "{role["years"]}")'
            for role in pos['roles']
        ])
        
        lines.append(f'''#position(
  "{escape_typst(pos['institution'])}",
  {dept}
  ({roles_str},)
)''')
    
    return "\n".join(lines)


def generate_education(education: list) -> str:
    """Generate the education section."""
    lines = ['#section("Education")', '']
    
    for edu in education:
        lines.append(
            f'#education-entry("{edu["degree"]}", '
            f'"{escape_typst(edu["field"])}", '
            f'"{escape_typst(edu["institution"])}", '
            f'"{edu["year"]}")'
        )
    
    return "\n".join(lines)


def generate_publications(pubs: dict) -> str:
    """Generate the publications section."""
    lines = ['#section("Publications")', '', '#subsection("Refereed articles")', '']
    
    for pub in pubs.get('refereed', []):
        title = escape_typst(pub['title'])
        authors = escape_typst(pub['authors'])
        journal = escape_typst(pub['journal'])
        details = pub.get('details', '')
        notes = pub.get('notes', [])
        
        details_str = f'details: "{escape_typst(details)}",' if details else ''
        
        if notes:
            notes_escaped = [f'"{escape_typst(n)}"' for n in notes]
            notes_str = f'notes: ({", ".join(notes_escaped)},),'
        else:
            notes_str = ''
        
        lines.append(f'''#pub(
  "{authors}",
  "{pub['year']}",
  "{title}",
  "{journal}",
  {details_str}
  {notes_str}
)''')
    
    # Working papers
    if pubs.get('working_papers'):
        lines.extend(['', '#subsection("Working papers")', ''])
        for wp in pubs['working_papers']:
            title = escape_typst(wp['title'])
            coauthors = f'coauthors: "{escape_typst(wp["authors"])}",' if wp.get('authors') else ''
            note = f'note: "{escape_typst(wp["note"])}",' if wp.get('note') else ''
            lines.append(f'#working-paper("{title}", {coauthors} {note})')
    
    # Work in progress
    if pubs.get('work_in_progress'):
        lines.extend(['', '#subsection("Work in progress")', ''])
        for wip in pubs['work_in_progress']:
            title = escape_typst(wip['title'])
            coauthors = f'coauthors: "{escape_typst(wip["coauthors"])}",' if wip.get('coauthors') else ''
            lines.append(f'#working-paper("{title}", {coauthors})')
    
    return "\n".join(lines)


def generate_nonrefereed(pubs: list) -> str:
    """Generate non-refereed publications section."""
    if not pubs:
        return ""
    
    lines = ['', '#subsection("Non-peer reviewed publications and commentaries")', '']
    
    for pub in pubs:
        title = escape_typst(pub['title'])
        venue = escape_typst(pub.get('venue', ''))
        date = pub.get('date', '')
        coauthors = f" with {escape_typst(pub['coauthors'])}" if pub.get('coauthors') else ''
        
        if venue:
            lines.append(f'[{title}{coauthors}. _{venue}._ {date}]')
        else:
            lines.append(f'[{title}{coauthors}. {date}]')
        lines.append('#linebreak()')
        lines.append('#v(0.2em)')
    
    return "\n".join(lines)


def generate_grants(grants: list) -> str:
    """Generate the grants section."""
    lines = ['#section("Grants and Fellowships")', '']
    
    for grant in grants:
        title = escape_typst(grant['title'])
        project = escape_typst(grant['project'])
        role = grant.get('role', '')
        amount = f'amount: "{format_amount(grant["amount"])}",' if grant.get('amount') else ''
        coauthors = f'coauthors: "{escape_typst(grant["coauthors"])}",' if grant.get('coauthors') else ''
        
        lines.append(f'''#grant(
  "{title}",
  "{project}",
  "{role}",
  {amount}
  "{grant['year']}",
  {coauthors}
)''')
    
    return "\n".join(lines)


def generate_honors(honors: list) -> str:
    """Generate honors and awards section."""
    if not honors:
        return ""
    
    lines = ['#section("Honors and Awards")', '']
    
    for honor in honors:
        lines.append(f'[{escape_typst(honor["title"])}, {honor["year"]}.]')
        lines.append('#linebreak()')
        lines.append('#v(0.2em)')
    
    return "\n".join(lines)


def generate_teaching(teaching: list) -> str:
    """Generate the teaching section."""
    lines = ['#section("Teaching")', '']
    
    for inst in teaching:
        courses_str = ", ".join([
            f'(name: "{escape_typst(c["name"])}", years: "{c["years"]}")'
            for c in inst['courses']
        ])
        lines.append(f'#teaching("{escape_typst(inst["institution"])}", ({courses_str},))')
    
    return "\n".join(lines)


def generate_advising(advising: list) -> str:
    """Generate the advising section."""
    lines = ['#section("Advising (ISU, Chair or co-Chair, Current Placement)")', '']
    
    for adv in advising:
        lines.append(
            f'#advisee("{escape_typst(adv["name"])}", '
            f'"{adv["degree"]}", '
            f'"{escape_typst(adv["placement"])}", '
            f'"{adv["years"]}")'
        )
    
    return "\n".join(lines)


def generate_conferences(conferences: list) -> str:
    """Generate conferences section."""
    if not conferences:
        return ""
    
    lines = ['#section("Conferences and Seminars")', '']
    
    for conf in conferences:
        lines.append(f'#conf-year("{conf["year"]}", "{escape_typst(conf["items"])}")')
    
    return "\n".join(lines)


def generate_service(service: dict) -> str:
    """Generate the service section."""
    lines = ['#section("Service")', '']
    
    # Referee
    if service.get('referee'):
        journals = ", ".join(service['referee'])
        lines.append(f'*Referee:* {escape_typst(journals)}')
        lines.append('')
        lines.append('#v(0.5em)')
    
    # Professional
    if service.get('professional'):
        roles = ", ".join([f"{p['role']} ({p['years']})" for p in service['professional']])
        lines.append(f'*Professional:* {escape_typst(roles)}')
        lines.append('')
        lines.append('#v(0.5em)')
    
    # Grant panels
    if service.get('grant_panels'):
        panels = ", ".join(service['grant_panels'])
        lines.append(f'*Grant Review Panels:* {escape_typst(panels)}')
        lines.append('')
        lines.append('#v(0.5em)')
    
    # Department service
    for dept_key in ['department_macalester', 'department_isu']:
        if service.get(dept_key):
            dept_name = "Macalester" if "macalester" in dept_key else "Iowa State"
            items = ", ".join(service[dept_key])
            lines.append(f'*Department ({dept_name}):* {escape_typst(items)}')
            lines.append('')
            lines.append('#v(0.5em)')
    
    return "\n".join(lines)


def generate_cv(yaml_path: str, output_path: str):
    """Generate complete CV from YAML data."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    sections = [
        generate_header(data),
        generate_positions(data['positions']),
        generate_education(data['education']),
        generate_publications(data['publications']),
    ]
    
    # Optional sections
    if data.get('publications', {}).get('nonrefereed'):
        sections.append(generate_nonrefereed(data['publications']['nonrefereed']))
    
    # Congressional testimony (special case)
    if data.get('testimony'):
        sections.append('#section("Congressional Testimony")')
        for t in data['testimony']:
            sections.append(f'[{escape_typst(t["committee"])}. {escape_typst(t["title"])}. {t["date"]}.]')
            sections.append('#linebreak()')
    
    sections.append(generate_grants(data['grants']))
    
    if data.get('honors'):
        sections.append(generate_honors(data['honors']))
    
    sections.append(generate_teaching(data['teaching']))
    sections.append(generate_advising(data['advising']))
    
    if data.get('conferences'):
        sections.append(generate_conferences(data['conferences']))
    
    sections.append(generate_service(data['service']))
    
    typst_content = "\n\n".join(sections)
    
    with open(output_path, 'w') as f:
        f.write(typst_content)
    
    print(f"Generated {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_cv.py cv_data.yaml output.typ")
        sys.exit(1)
    
    generate_cv(sys.argv[1], sys.argv[2])
