# Automated CV Workflow (Typst)

This system maintains your CV as structured YAML data and uses [Typst](https://typst.app/) to generate a professional PDF.

## Why Typst?

- **Simpler syntax** than LaTeX—no cryptic error messages
- **Fast compilation**—builds in milliseconds
- **Modern tooling**—native to GitHub Actions with no heavy TeX installation
- **Great typography**—output quality rivals LaTeX

## Directory Structure

```
your-website-repo/
├── cv/
│   ├── cv_data.yaml        # Your CV content (edit this!)
│   ├── cv_template.typ     # Typst formatting template
│   ├── generate_cv.py      # Converts YAML → Typst
│   └── Lade_CV.typ         # Auto-generated (don't edit directly)
├── docs/
│   └── Lade_CV.pdf         # Auto-generated PDF for website
└── .github/
    └── workflows/
        └── build-cv.yml    # GitHub Action
```

## How It Works

1. **Edit `cv_data.yaml`** — This is the single source of truth for your CV
2. **Push to GitHub** — The Action automatically:
   - Generates Typst markup from the YAML
   - Compiles to PDF
   - Commits the PDF to `docs/` for your website

## Using with Claude Code

The whole point of this setup is to make CV updates trivially easy. Examples:

### Add a new publication
```
"Add my new paper: 'Water Quality Impacts of Agricultural Subsidies' 
published in JAERE 2025, coauthored with Smith and Jones"
```

### Update a position
```
"Change my CARD affiliation end date from 'Present' to '2024'"
```

### Add a conference presentation
```
"Add that I presented at AERE 2025 in Seattle"
```

### Add a new grant
```
"Add my new NSF grant: $450,000 for 'Climate Adaptation in Rural Communities' 
with co-PIs Keiser and Rudik, starting 2025"
```

Claude Code edits the YAML, you push, PDF updates automatically.

## Local Development

### Prerequisites

```bash
pip install pyyaml typst
```

### Generate and compile locally

```bash
# Generate Typst from YAML
python cv/generate_cv.py cv/cv_data.yaml cv/Lade_CV.typ

# Compile to PDF (using Python bindings)
python -c "import typst; typst.compile('cv/Lade_CV.typ', output='cv/Lade_CV.pdf')"

# Or use the typst CLI if installed
typst compile cv/Lade_CV.typ cv/Lade_CV.pdf
```

## YAML Structure Reference

| Section | Description |
|---------|-------------|
| `positions` | Academic appointments |
| `education` | Degrees |
| `publications.refereed` | Peer-reviewed articles |
| `publications.working_papers` | Working papers |
| `publications.work_in_progress` | Ongoing work |
| `publications.nonrefereed` | Policy briefs, op-eds, etc. |
| `testimony` | Congressional testimony |
| `grants` | Funded projects |
| `honors` | Awards |
| `teaching` | Courses taught |
| `advising` | PhD students |
| `conferences` | Presentations by year |
| `service` | Referee work, committees |

### Adding a new publication

```yaml
publications:
  refereed:
    - authors: Lade, G.E. and J. Smith
      year: "2025"
      title: "Your Paper Title Here"
      journal: Journal Name
      details: "Vol(Issue): pages"
      notes:  # optional
        - "Award or distinction"
```

### Adding a grant

```yaml
grants:
  - title: Funding Agency Name
    project: Project Title
    role: PI  # or co-PI, Project Director
    coauthors: Collaborator Names  # optional
    amount: 100000  # no commas, just number
    year: "2025"
```

## Customizing the Template

Edit `cv_template.typ` to change:

- **Fonts**: Change `font: "Linux Libertine"` to any system font
- **Margins**: Adjust the `margin` settings in `set page()`
- **Section styling**: Modify the `#let section()` function
- **Colors**: Change `rgb(0, 0, 128)` in link styling

## Troubleshooting

### "Label does not exist" error
Special characters like `@` need escaping. The generator handles this automatically, but if you edit the `.typ` file directly, use `\@` for literal @ symbols.

### Missing fonts
Linux Libertine should be available on most systems. If not, change to a common font like "Times New Roman" or "Georgia" in the template.

### GitHub Action fails
Check that all three files (`cv_data.yaml`, `cv_template.typ`, `generate_cv.py`) are in the `cv/` directory.

## Advantages Over LaTeX

| Aspect | LaTeX | Typst |
|--------|-------|-------|
| Error messages | Cryptic | Clear |
| Compilation speed | Slow | Fast |
| GitHub Actions setup | Complex (texlive) | Simple |
| Syntax learning curve | Steep | Gentle |
| Output quality | Excellent | Excellent |
