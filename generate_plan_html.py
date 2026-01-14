import json
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

# Paths
DATA_FILE = Path("plan_log.json")
OUT_FILE = Path("index.html")
SITE_URL = "https://roskelld.github.io/plan"

def load_entries():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def build_structure(entries):
    # Organize entries by year, then month, then day
    structure = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for e in entries:
        dt = datetime.fromtimestamp(e["timestamp"], timezone.utc)
        y = dt.strftime("%Y")
        m = dt.strftime("%Y-%m")
        d = dt.strftime("%Y-%m-%d")
        structure[y][m][d].append(e)
    return structure


def html_escape(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def generate_html(structure):
    # Determine latest entry for OG description
    flat = [e for year in structure.values() for month in year.values() for day in month.values() for e in day]
    latest_desc = ""
    if flat:
        flat.sort(key=lambda e: e["timestamp"], reverse=True)
        raw = html_escape(flat[0]["body"]).replace("\n", " ")
        latest_desc = (raw[:200] + '...') if len(raw) > 200 else raw
        
    html = ["<!DOCTYPE html>", "<html lang='en'>", "<head>",
            "<meta charset='UTF-8'>",
            f"<title>roskelld .plan</title>",
            # OpenGraph tags
            f"<meta property='og:title' content='.plan Archive' />",
            f"<meta property='og:description' content='{latest_desc}' />",
            "<meta property='og:type' content='website' />",
            f"<meta property='og:url' content='{SITE_URL}/' />",
            # RSS link & CSS
            f"<link rel='alternate' type='application/rss+xml' href='{SITE_URL}/feed.xml' />",
            "<link rel='stylesheet' type='text/css' href='color_expanded.css'>",
            "<link rel='stylesheet' type='text/css' href='styles.css'>",
            "</head><body>",
            "<h1>roskelld .plan</h1>",
            "<a href='https://roskelld.github.io/plan/feed.xml'><img src='images/pic_rss.gif' alt='RSS'></a>",
            # Table of Contents
            "<details>",
            "<summary>Jump to…</summary>",
            "<nav><ul>"]

    # TOC: years→months→days
    for year in sorted(structure.keys(), reverse=True):
        html.append(f"<li><a href='#{year}'>{year}</a><ul>")
        for month in sorted(structure[year].keys(), reverse=True):
            label = datetime.strptime(month, "%Y-%m").strftime("%B")
            html.append(f"<li><a href='#{month}'>{label}</a>")
            html.append("</li>")
        html.append("</ul></li>")
    html.append("</ul></nav>")
    html.append("</details>")

    # Entries
    for year in sorted(structure.keys(), reverse=True):
        html.append(f"<label id='{year}'></label>")
        for month in sorted(structure[year].keys(), reverse=True):
            html.append(f"<label id='{month}'></label>")
            for day in sorted(structure[year][month].keys(), reverse=True):
                full_label = datetime.strptime(day, "%Y-%m-%d").strftime("%B %d, %Y")
                html.append(f"<h4 id='{day}'>{full_label}</h4>")
                for e in reversed(structure[year][month][day]):
                    body = html_escape(e["body"]).replace("\n", "<br>")
                    code_spans = []
                    def stash_code(match):
                        code_spans.append(match.group(1))
                        return f"__CODE_SPAN_{len(code_spans) - 1}__"

                    body = re.sub(r"`([^`]+)`", stash_code, body)
                    # link tags
                    body = re.sub(r"#(\w+)", r"<a class='tag' href='#\1'>#\1</a>", body)
                    # Auto-link web addresses
                    def linkify(match):
                        url = match.group("url")
                        trail = ""
                        while url and url[-1] in ".,);:!?]}>":
                            trail = url[-1] + trail
                            url = url[:-1]
                        href = url if url.startswith("http") else f"http://{url}"
                        return f"<a class='weblink' href='{href}' rel='noopener noreferrer' target='_blank'>{url}</a>{trail}"

                    body = re.sub(r"(?P<url>(https?://|www\.)[^\s<]+)", linkify, body)
                    # Restore inline code spans
                    for idx, code in enumerate(code_spans):
                        body = body.replace(f"__CODE_SPAN_{idx}__", f"<code class='inline-code'>{code}</code>")
                    cid = e["commit"][:7]
                    html.append(
                        f"<div id='entry-{cid}' class='entry'>{body}"
                        f"<div class='tags'>Commit {cid}</div></div>"
                    )
    html.append("</body></html>")
    return "\n".join(html)


def main():
    entries = load_entries()
    struct = build_structure(entries)
    content = generate_html(struct)
    OUT_FILE.write_text(content, encoding="utf-8")
    print(f"Generated {OUT_FILE}")

if __name__ == '__main__':
    main()
