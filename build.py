"""
build.py — Portfolio static site generator
Run: python3 build.py
Output: output/index.html
"""
import json
import os

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR      = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR    = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load(filename):
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
        return json.load(f)

def read_template(filename):
    with open(os.path.join(TEMPLATES_DIR, filename), encoding="utf-8") as f:
        return f.read()

info     = load("info.json")
skills   = load("skills.json")
projects = load("projects.json")
training = load("training.json")


def build_hero():
    name_parts = info["name"].split()
    p1 = name_parts[0]
    p2 = " ".join(name_parts[1:-1])
    p3 = name_parts[-1]

    stats_html = ""
    for s in info["stats"]:
        stats_html += f'<div class="stat"><span class="stat-num">{s["num"]}</span><span class="stat-label">{s["label"]}</span></div>'

    tpl = read_template("hero.html")
    return (tpl
        .replace("{tagline}", info["tagline"])
        .replace("{name_parts[0]}", p1)
        .replace("{name_parts[1]}", p2)
        .replace("{name_parts[2]}", p3)
        .replace("{title}", info["title"])
        .replace("{about_short}", info["about"][0])
        .replace("{stats}", stats_html)
        .replace("{photo}", info["photo"])
        .replace("{name}", info["name"])
    )


def build_about():
    paras = "".join(f"<p>{p}</p>" for p in info["about"])

    rows = ""
    for card in info["info_cards"]:
        rows += f'''<div class="info-row">
          <span class="info-key">{card["label"]}</span>
          <span class="info-val">{card["value"]}</span>
        </div>'''

    tpl = read_template("about.html")
    return (tpl
        .replace("{about_paragraphs}", paras)
        .replace("{info_rows}", rows)
    )


def build_skills():
    groups_html = ""
    for group in skills:
        tags_html = "".join(f'<span class="skill-tag">{s["name"]}</span>' for s in group["items"])  
        groups_html += f'''<div class="skill-group reveal">
        <p class="skill-group-name">{group["group"]}</p>
        <div class="skill-tags">{tags_html}</div>
      </div>'''

    tpl = read_template("skills.html")
    return tpl.replace("{skill_groups}", groups_html)


def build_projects():
    cats_html = ""
    for cat in projects:
        cards_html = ""
        for p in cat["projects"]:
            if p["coming_soon"]:
                cards_html += f'''<div class="proj-card coming-soon">
            <p class="proj-name">{p["name"]}</p>
            <p class="proj-desc">{p["desc"]}</p>
            <span class="coming-label">Coming soon</span>
          </div>'''
            else:
                tags_html = "".join(f'<span class="proj-tag">{t}</span>' for t in p["tags"])
                cards_html += f'''<div class="proj-card">
            <p class="proj-name">{p["name"]}</p>
            <p class="proj-desc">{p["desc"]}</p>
            <div class="proj-tags">{tags_html}</div>
            <a class="proj-link" href="{p["repo"]}" target="_blank">View repo</a>
          </div>'''

        cats_html += f'''<div class="proj-category reveal">
        <p class="proj-category-label">{cat["category"]}</p>
        <div class="projects-grid">{cards_html}</div>
      </div>'''

    tpl = read_template("projects.html")
    return tpl.replace("{categories}", cats_html)


def build_contact():
    c = info["contact"]
    github_display   = c["github"].replace("https://", "")
    linkedin_display = c["linkedin"].split("/in/")[-1].strip("/")
    location = next((x["value"] for x in info["info_cards"] if x["label"] == "Location"), "Jordan")

    tpl = read_template("contact.html")
    return (tpl
        .replace("{email}", c["email"])
        .replace("{github}", c["github"])
        .replace("{github_display}", github_display)
        .replace("{linkedin}", c["linkedin"])
        .replace("{linkedin_display}", linkedin_display)
        .replace("{location}", location)
    )



def build_training():
    items_html = ""
    for t in training:
        badge = f'<span class="training-badge">{t["badge"]}</span>' if t["badge"] else ""
        url = t.get("url", "")
        tag_o = f'<a class="training-card-link" href="{url}" target="_blank">' if url else "<div>"
        tag_c = "</a>" if url else "</div>"
        items_html += (
            tag_o +
            '<div class="training-card reveal">' +
            '<div class="training-header">' +
            "<div>" +
            f'<p class="training-title">{t["title"]} {badge}</p>' +
            f'<p class="training-issuer">{t["issuer"]}</p>' +
            "</div>" +
            f'<span class="training-year">{t["year"]}</span>' +
            "</div>" +
            f'<p class="training-desc">{t["desc"]}</p>' +
            "</div>" +
            tag_c
        )
    tpl = read_template("training.html")
    return tpl.replace("{training_items}", items_html)

def build():
    content = (
        build_hero() +
        build_about() +
        build_skills() +
        build_projects() +
        build_training() +
        build_contact()
    )

    base = read_template("base.html")
    html = (base
        .replace("{content}", content)
        .replace("{name}", info["name"])
    )

    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ Built → {out_path}")

if __name__ == "__main__":
    build()
