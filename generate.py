"""Generate one attributed technology lesson from official RSS feeds.

Only RSS metadata and a short summary are stored. The original article remains
at the source URL, which keeps this workflow respectful of copyright and rate
limits.
"""

from __future__ import annotations

import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
LESSONS = ROOT / "lessons"
STATE = ROOT / ".cache" / "seen_links.json"

FEEDS = [
    ("Software Engineer", "https://github.blog/feed/"),
    ("AI Engineer", "https://pytorch.org/blog/feed.xml"),
    ("Software Engineer - Python", "https://feeds.feedburner.com/PythonInsider"),
    ("Hardware Engineer", "https://blog.arduino.cc/feed/"),
    ("Automation Engineer", "https://nodered.org/blog/rss.xml"),
]


def clean(value: str, limit: int = 600) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit].rstrip() + ("…" if len(value) > limit else "")


def read_feed(category: str, url: str) -> list[dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": "TechnologyLearningHub/1.0 RSS reader"})
    with urllib.request.urlopen(request, timeout=20) as response:
        root = ET.fromstring(response.read())

    entries = []
    for item in root.iter():
        tag = item.tag.rsplit("}", 1)[-1]
        if tag not in {"item", "entry"}:
            continue
        values = {child.tag.rsplit("}", 1)[-1]: child for child in item}
        title = clean(values.get("title").text if values.get("title") is not None else "", 160)
        link_node = values.get("link")
        link = (link_node.attrib.get("href") if link_node is not None else None) or (link_node.text if link_node is not None else "")
        summary_node = values.get("description") or values.get("summary") or values.get("content")
        summary = clean(summary_node.text if summary_node is not None else "")
        if title and link:
            entries.append({"category": category, "title": title, "link": link.strip(), "summary": summary})
    return entries


def main() -> None:
    seen = set(json.loads(STATE.read_text(encoding="utf-8"))) if STATE.exists() else set()
    candidates: list[dict[str, str]] = []
    for category, url in FEEDS:
        try:
            candidates.extend(read_feed(category, url))
        except Exception as exc:
            print(f"Skipping {url}: {exc}")

    fresh = next((item for item in candidates if item["link"] not in seen), None)
    if fresh is None:
        print("No new RSS item found; nothing to publish.")
        return

    today = date.today().isoformat()
    LESSONS.mkdir(exist_ok=True)
    output = LESSONS / f"{today}.md"
    output.write_text(
        f"# Technology Brief — {today}\n\n"
        f"## {fresh['title']}\n\n"
        f"**Track:** {fresh['category']}\n\n"
        f"### Ringkasan\n{fresh['summary'] or 'Baca sumber asli untuk ringkasan lengkap.'}\n\n"
        f"### Latihan\nTuliskan tiga hal yang kamu pelajari dari sumber ini dan satu cara menerapkannya pada proyek kecil.\n\n"
        f"### Sumber asli\n[{fresh['link']}]({fresh['link']})\n\n"
        "> Materi ini merangkum metadata RSS dan mengarahkan pembaca ke sumber asli.\n",
        encoding="utf-8",
    )
    seen.add(fresh["link"])
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(sorted(seen), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
