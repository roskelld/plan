import json
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

DATA_FILE = Path("plan_log.json")
RSS_FILE = Path("feed.xml")
SITE_URL = "https://roskelld.github.io/plan"
TITLE = "roskelld .plan"
DESCRIPTION = "Latest .plan entries"
LANG = "en-us"

entries = json.loads(DATA_FILE.read_text(encoding="utf-8"))
entries.sort(key=lambda e: e['timestamp'], reverse=True)

rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = TITLE
ET.SubElement(channel, 'link').text = SITE_URL
ET.SubElement(channel, 'description').text = DESCRIPTION
ET.SubElement(channel, 'language').text = LANG
ET.SubElement(channel, 'lastBuildDate').text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")

for e in entries:
    dt = datetime.fromtimestamp(e['timestamp'], tz=timezone.utc)
    item = ET.SubElement(channel, 'item')
    link = f"{SITE_URL}/#entry-{e['commit'][:7]}"
    ET.SubElement(item, 'title').text = dt.strftime("%Y-%m-%d %H:%M UTC")
    ET.SubElement(item, 'link').text = link
    ET.SubElement(item, 'guid').text = link
    ET.SubElement(item, 'pubDate').text = dt.strftime("%a, %d %b %Y %H:%M:%S %z")
    ET.SubElement(item, 'description').text = e['body']

ET.ElementTree(rss).write(RSS_FILE, encoding='utf-8', xml_declaration=True)
print(f"Generated {RSS_FILE}")