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

GUIDES = {
    "Software Engineer": {"level": "Beginner to Intermediate", "theory": "Software engineering adalah proses merancang, membangun, menguji, dan memelihara software secara sistematis.", "why": "Agar kode mudah dipahami, diuji, dan dikembangkan oleh tim.", "code": "def calculate_total(items):\n    return sum(item['price'] * item['qty'] for item in items)", "best": "Gunakan nama jelas, fungsi kecil, version control, code review, dan automated tests.", "pitfalls": "Fungsi terlalu besar, duplikasi kode, dan tidak menangani edge case.", "exercise": "Buat fungsi kecil dan tambahkan tiga unit test."},
    "Hardware Engineer": {"level": "Beginner to Intermediate", "theory": "Hardware engineering menggabungkan elektronika, rangkaian digital, microcontroller, sensor, dan actuator.", "why": "Memahami input-proses-output membantu membuat perangkat yang aman dan mudah di-debug.", "code": "const int sensorPin = 2;\nconst int ledPin = 13;\ndigitalWrite(ledPin, digitalRead(sensorPin));", "best": "Mulai dari datasheet dan perhatikan tegangan, arus, serta ground.", "pitfalls": "Salah tegangan, pin floating, dan mengabaikan batas arus komponen.", "exercise": "Rancang lampu otomatis dan tentukan sensor, controller, actuator, serta fail-safe."},
    "Automation Engineer": {"level": "Beginner to Intermediate", "theory": "Automation engineering memakai sensor, controller, dan actuator untuk menjalankan proses secara konsisten.", "why": "Control loop, PLC, dan interlock penting untuk keselamatan dan produktivitas.", "code": "if temperature < target - tolerance:\n    heater = ON\nelif temperature > target + tolerance:\n    heater = OFF", "best": "Definisikan alarm, logging, manual override, dan emergency stop.", "pitfalls": "Tidak menangani sensor rusak dan membuat loop terlalu agresif.", "exercise": "Buat state diagram pintu otomatis: OPEN, CLOSED, MOVING, dan ERROR."},
    "AI Engineer": {"level": "Beginner to Intermediate", "theory": "AI engineering mencakup data, training model, evaluasi, deployment, dan monitoring.", "why": "Model akurat di notebook belum tentu aman atau berguna di produk.", "code": "X_train, X_test, y_train, y_test = train_test_split(X, y)\nmodel.fit(X_train, y_train)", "best": "Pisahkan train dan test, ukur baseline, cek bias, dan dokumentasikan model.", "pitfalls": "Data leakage, overfitting, dan menganggap output model selalu benar.", "exercise": "Buat eksperimen klasifikasi kecil dan jelaskan error model."},
    "Designer": {"level": "Beginner", "theory": "Design menerjemahkan kebutuhan menjadi visual dengan hierarki, konsistensi, dan tujuan jelas.", "why": "Visual hierarchy dan typography membantu orang memahami informasi.", "code": ".card-title {\n  font-size: 1.5rem;\n  font-weight: 700;\n}", "best": "Gunakan grid, batasi font, dan uji desain pada ukuran layar nyata.", "pitfalls": "Terlalu banyak warna, kontras rendah, dan alignment tidak konsisten.", "exercise": "Redesign kartu produk dengan hierarki judul, informasi, dan aksi."},
    "UI/UX Designer": {"level": "Beginner to Intermediate", "theory": "UI/UX menggabungkan interface dengan riset, kebutuhan pengguna, alur tugas, dan usability testing.", "why": "Interface cantik belum tentu mudah digunakan; keputusan perlu divalidasi dengan perilaku pengguna.", "code": "User task: Cari produk dan tambahkan ke keranjang\nSuccess: selesai tanpa bantuan\nMeasure: waktu, error, dan pertanyaan", "best": "Riset, buat prototype murah, uji dengan pengguna, lalu iterasi.", "pitfalls": "Mengandalkan asumsi dan menguji hanya dengan sesama designer.", "exercise": "Buat tiga task usability untuk aplikasi pencatat keuangan."},
}


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
    guide = GUIDES.get(fresh["category"], GUIDES["Software Engineer"])
    output.write_text(
        f"# {fresh['title']}\n\n**Kategori:** {fresh['category']}  \n**Difficulty:** {guide['level']}  \n**Date:** {today}\n\n"
        f"## Teori: Apa yang Dipelajari?\n\n{guide['theory']}\n\n"
        f"## Kenapa Ini Penting?\n\n{guide['why']}\n\n"
        f"## Ringkasan Bacaan Terbaru\n\n{fresh['summary'] or 'Baca sumber asli untuk konteks terbaru.'}\n\n"
        f"## Contoh Praktik\n\n```text\n{guide['code']}\n```\n\n"
        f"## Best Practices\n\n{guide['best']}\n\n## Kesalahan Umum\n\n{guide['pitfalls']}\n\n"
        f"## Latihan Mandiri\n\n{guide['exercise']}\n\n## Sumber Belajar\n\n- [Bacaan terbaru dari sumber asli]({fresh['link']})\n",
        encoding="utf-8",
    )
    seen.add(fresh["link"])
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(sorted(seen), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
