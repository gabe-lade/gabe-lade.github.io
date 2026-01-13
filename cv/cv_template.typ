// CV Template - Typst
// This file defines the styling; content comes from generate_cv.py

#let cv(
  name: "",
  email: "",
  department: "",
  institution: "",
  address: "",
  body
) = {
  // Page setup
  set page(
    paper: "us-letter",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  )
  
  // Font setup
  set text(
    font: "Linux Libertine",
    size: 12pt,
  )
  
  // Paragraph setup
  set par(
    justify: false,
    leading: 0.65em,
  )
  
  // Link styling
  show link: it => text(fill: rgb(0, 0, 128), it)
  
  // Header
  align(center)[
    #text(size: 18pt, weight: "bold", smallcaps(name))
  ]
  
  align(center)[
    #department \
    #institution \
    #address \
    Email: #link("mailto:" + email)[#email]
  ]
  
  v(-0.2em)
  line(length: 100%, stroke: 0.5pt)
  v(0.2em)

  body
}

// Section heading
#let section(title) = {
  v(0.5em)
  text(size: 13pt, weight: "bold", smallcaps(title))
  v(0.2em)
}

// Subsection (e.g., "Refereed articles")
#let subsection(title) = {
  v(0.3em)
  text(weight: "bold", title)
  v(0.15em)
}

// Position entry
#let position(institution, department: none, roles) = {
  text(weight: "regular", institution)
  linebreak()
  if department != none {
    h(1em)
    department
    linebreak()
  }
  for role in roles {
    if department != none { h(2em) } else { h(1em) }
    role.title
    h(1fr)
    role.years
    linebreak()
  }
  v(0.15em)
}

// Education entry
#let education-entry(degree, field, institution, year) = {
  [#degree, #field, #institution, #year]
  linebreak()
}

// Publication entry
#let pub(authors, year, title, journal, details: none, notes: none) = {
  [#authors. #year. #title. #emph[*#journal.*]]
  if details != none [ #details]
  linebreak()
  if notes != none {
    for note in notes {
      h(1em)
      [— #note]
      linebreak()
    }
  }
  v(0.15em)
}

// Working paper
#let working-paper(title, coauthors: none, note: none) = {
  title
  if coauthors != none [ (with #coauthors)]
  if note != none [. #note]
  linebreak()
  v(0.15em)
}

// Grant entry
#let grant(title, project, role, amount: none, year, coauthors: none) = {
  [#title. #project (#role]
  if coauthors != none [. Co-Investigators: #coauthors]
  [)]
  if amount != none [. #amount]
  [. #year.]
  linebreak()
  v(0.15em)
}

// Teaching entry
#let teaching(institution, courses) = {
  text(weight: "regular", institution)
  linebreak()
  for course in courses {
    h(1em)
    course.name
    h(1fr)
    course.years
    linebreak()
  }
  v(0.15em)
}

// Advising entry
#let advisee(name, degree, placement, years) = {
  [#name (#degree, #placement) #h(1fr) #years]
  linebreak()
}

// Conference year
#let conf-year(year, items) = {
  [#year: #items]
  linebreak()
  v(0.1em)
}
