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

DEEP_THEORY = {
    "Software Engineer": {
        "goals": "Setelah membaca, pembaca memahami siklus hidup software, pemisahan tanggung jawab, dan alasan engineering practices diperlukan.",
        "prereq": "Bisa membaca kode dasar dan memahami variabel, fungsi, serta input-output.",
        "theory": "Software engineering bukan sekadar menulis kode yang bisa berjalan. Ia adalah disiplin untuk mengubah kebutuhan pengguna menjadi sistem yang dapat diandalkan, diuji, dipantau, dan dipelihara. Kode akan dibaca jauh lebih sering daripada ditulis, sehingga struktur dan keputusan desain sama pentingnya dengan hasil akhirnya.\n\nDalam proyek nyata, kebutuhan berubah, anggota tim berganti, dan jumlah pengguna bertambah. Karena itu engineer memakai version control, code review, automated testing, dokumentasi, logging, dan arsitektur yang memisahkan aturan bisnis dari detail teknis. Tujuannya bukan membuat kode paling rumit, melainkan mengurangi biaya perubahan dan risiko kerusakan.",
        "walkthrough": "Fungsi calculate_total menerima daftar item, menghitung harga dikali jumlah untuk setiap item, lalu menjumlahkan seluruh hasil. Aturan bisnis ini sebaiknya tidak bergantung pada database atau tampilan agar dapat diuji secara mandiri. Setelah itu tambahkan test untuk daftar kosong, satu item, diskon, dan jumlah yang tidak valid.",
    },
    "Hardware Engineer": {
        "goals": "Memahami hubungan sensor, pemrosesan, dan actuator serta batasan listrik dasar.",
        "prereq": "Memahami konsep tegangan, arus, ground, dan logika 0/1.",
        "theory": "Hardware engineering menghubungkan dunia fisik dengan sistem komputasi. Sensor mengubah kondisi fisik menjadi sinyal, microcontroller memproses sinyal berdasarkan program, lalu actuator melakukan aksi. Setiap komponen memiliki batas tegangan, arus, suhu, dan timing yang harus dihormati.\n\nBerbeda dari software, bug hardware dapat merusak komponen secara permanen. Engineer membaca datasheet, membuat skematik, menguji dengan multimeter atau oscilloscope, dan merancang kondisi aman ketika sensor gagal atau listrik terputus.",
        "walkthrough": "Pada contoh LED, sensorPin adalah input dan ledPin adalah output. Program membaca level logika sensor lalu menyalin nilainya ke LED. Dalam perangkat nyata, tambahkan resistor, debounce untuk tombol, dan validasi agar sinyal noise tidak menyalakan actuator secara salah.",
    },
    "Automation Engineer": {
        "goals": "Memahami control loop, state machine, sensor, actuator, dan fail-safe.",
        "prereq": "Memahami diagram alur dan konsep input-output.",
        "theory": "Automation engineering merancang sistem yang mengamati kondisi melalui sensor, mengambil keputusan melalui controller, dan mengubah dunia fisik melalui actuator. Control loop membandingkan nilai aktual dengan target; selisihnya disebut error dan dipakai untuk menentukan aksi berikutnya.\n\nSistem industri harus tetap aman ketika sensor rusak, jaringan putus, atau operator melakukan kesalahan. Karena itu desain automation membutuhkan interlock, alarm, emergency stop, manual override, logging, dan prosedur recovery yang jelas.",
        "walkthrough": "Pada thermostat sederhana, heater menyala ketika suhu berada di bawah target dikurangi tolerance dan mati ketika melewati target ditambah tolerance. Tolerance mencegah heater hidup-mati terlalu cepat. Sistem produksi biasanya memakai PID, state machine, dan sensor redundancy untuk hasil yang lebih stabil.",
    },
    "AI Engineer": {
        "goals": "Memahami alur data, training, evaluasi, deployment, dan risiko model machine learning.",
        "prereq": "Memahami Python dasar, tabel data, dan konsep train-test split.",
        "theory": "AI engineering mencakup lebih dari memilih model. Pekerjaan dimulai dari mendefinisikan masalah dan target, mengumpulkan data yang representatif, membersihkan data, membuat baseline, melatih model, mengevaluasi error, lalu mengintegrasikannya ke produk.\n\nModel dapat terlihat akurat tetapi gagal pada data dunia nyata karena data leakage, bias, distribution shift, atau metrik yang salah. Engineer harus menyimpan versi dataset dan model, memantau performa setelah deployment, serta menyediakan fallback ketika prediksi tidak yakin.",
        "walkthrough": "Data dibagi menjadi train dan test agar evaluasi dilakukan pada contoh yang belum pernah dilihat model. Model belajar dari train, kemudian prediksinya dibandingkan dengan label pada test. Jangan mengubah test set untuk tuning berulang karena hasilnya tidak lagi merepresentasikan performa nyata.",
    },
    "Designer": {
        "goals": "Memahami bagaimana hierarki visual, typography, layout, dan warna menyampaikan informasi.",
        "prereq": "Bisa mengamati interface dan menjelaskan tujuan sebuah elemen visual.",
        "theory": "Designer memecahkan masalah komunikasi melalui bentuk, ruang, warna, tipografi, dan komposisi. Sebelum memilih gaya visual, designer perlu memahami tujuan bisnis, informasi yang harus disampaikan, konteks penggunaan, dan keterbatasan media.\n\nVisual hierarchy menentukan urutan perhatian pengguna. Ukuran, kontras, whitespace, alignment, dan posisi membuat pembaca tahu mana judul, informasi utama, dan tindakan berikutnya. Sistem desain membantu keputusan ini konsisten di banyak halaman dan perangkat.",
        "walkthrough": "Pada .card-title, ukuran dan weight membuat judul lebih menonjol. Dalam praktik, cek juga line-height, panjang teks, kontras warna, dan perilakunya pada layar kecil. Style yang bagus harus tetap terbaca ketika konten berubah.",
    },
    "UI/UX Designer": {
        "goals": "Memahami perbedaan UI dan UX serta cara memvalidasi desain dengan riset dan usability testing.",
        "prereq": "Bisa menjelaskan siapa pengguna dan tujuan utama sebuah produk.",
        "theory": "UX berfokus pada keseluruhan pengalaman pengguna: masalah apa yang ingin diselesaikan, langkah yang harus ditempuh, dan apakah hasilnya memuaskan. UI adalah bagian visual dan interaktif yang memungkinkan pengalaman itu terjadi. UI yang indah tidak otomatis berarti UX yang baik.\n\nProses yang sehat dimulai dari riset, perumusan problem, user flow, wireframe, prototype, usability test, lalu iterasi. Pengujian bukan meminta pengguna memuji desain, tetapi mengamati apakah mereka dapat menyelesaikan task, di mana mereka ragu, dan kesalahan apa yang muncul.",
        "walkthrough": "Task 'cari produk dan tambahkan ke keranjang' memiliki tujuan dan kriteria sukses yang jelas. Catat waktu penyelesaian, jumlah error, dan pertanyaan pengguna. Data ini lebih berguna daripada sekadar bertanya apakah mereka menyukai warna tombol.",
    },
}

PRACTICE = {
    "Software Engineer": {
        "analogy": "Bayangkan aplikasi seperti restoran: UI adalah pelayan, service adalah dapur, dan database adalah gudang. Memisahkan tanggung jawab membuat perubahan menu tidak merusak gudang.",
        "steps": "1. Buat file fungsi dan definisikan input yang dibutuhkan.\n2. Tulis satu aturan bisnis paling kecil.\n3. Jalankan dengan data normal.\n4. Tambahkan test untuk data kosong dan data salah.\n5. Refactor jika satu fungsi mulai mengerjakan terlalu banyak hal.",
        "result": "Program harus menghasilkan total yang benar untuk data valid dan menolak input yang tidak masuk akal dengan error yang jelas.",
        "check": "Jelaskan bagian mana yang merupakan aturan bisnis dan mengapa bagian itu bisa dites tanpa database atau halaman web.",
    },
    "Hardware Engineer": {
        "analogy": "Sensor seperti mata, microcontroller seperti otak, dan actuator seperti tangan. Ketiganya harus memakai tegangan dan bahasa sinyal yang kompatibel.",
        "steps": "1. Baca datasheet setiap komponen.\n2. Gambar jalur VCC, GND, input, dan output.\n3. Uji sensor tanpa actuator.\n4. Tampilkan nilai sensor lewat serial monitor.\n5. Aktifkan actuator hanya setelah nilai tervalidasi.",
        "result": "LED atau motor hanya aktif ketika kondisi sensor benar dan tetap aman ketika kabel sensor dilepas.",
        "check": "Sebutkan apa yang terjadi jika ground terputus atau sensor mengirim nilai di luar rentang.",
    },
    "Automation Engineer": {
        "analogy": "Thermostat seperti seseorang yang terus melihat termometer, membandingkan suhu dengan target, lalu menyalakan atau mematikan pemanas.",
        "steps": "1. Tentukan target dan batas aman.\n2. Baca sensor secara berkala.\n3. Hitung selisih nilai aktual dengan target.\n4. Pilih aksi berdasarkan state sistem.\n5. Tambahkan alarm dan mode manual ketika sensor gagal.",
        "result": "Sistem bergerak menuju target tanpa hidup-mati terlalu cepat dan masuk ke kondisi aman saat input tidak valid.",
        "check": "Jelaskan mengapa tolerance atau hysteresis diperlukan pada control loop sederhana.",
    },
    "AI Engineer": {
        "analogy": "Training model seperti mengajar siswa dengan contoh. Data train adalah materi latihan, validation membantu memilih cara belajar, dan test adalah ujian terakhir.",
        "steps": "1. Tulis definisi masalah dan target.\n2. Bersihkan dan periksa kualitas data.\n3. Pisahkan train dan test sebelum tuning.\n4. Latih baseline sederhana.\n5. Analisis contoh yang salah, bukan hanya angka akurasi.",
        "result": "Kamu dapat menjelaskan data yang dipakai, alasan memilih metrik, contoh prediksi salah, dan batasan model.",
        "check": "Jelaskan apa itu data leakage dan beri satu contoh bagaimana hal itu bisa terjadi.",
    },
    "Designer": {
        "analogy": "Mendesain halaman seperti menyusun papan pengumuman: judul harus terlihat dulu, informasi penting berikutnya, lalu instruksi tindakan.",
        "steps": "1. Tulis tujuan halaman dalam satu kalimat.\n2. Kelompokkan konten berdasarkan kepentingan.\n3. Susun grid dan alignment.\n4. Pilih ukuran dan weight typography.\n5. Uji desain dengan orang yang belum melihatnya.",
        "result": "Orang lain dapat menyebutkan informasi utama dan tindakan berikutnya tanpa penjelasan dari designer.",
        "check": "Tunjukkan elemen dengan prioritas tertinggi, sedang, dan rendah pada desainmu.",
    },
    "UI/UX Designer": {
        "analogy": "UX seperti merancang rute perjalanan: pengguna harus tahu tujuan, jalan berikutnya, dan cara kembali ketika salah arah.",
        "steps": "1. Tentukan siapa pengguna dan task-nya.\n2. Tulis langkah ideal dari awal sampai selesai.\n3. Buat wireframe tanpa dekorasi.\n4. Uji task dengan pengguna.\n5. Catat kebingungan, error, dan waktu lalu iterasi.",
        "result": "Mayoritas pengguna menyelesaikan task tanpa bantuan dan kamu memiliki bukti bagian mana yang perlu diperbaiki.",
        "check": "Bedakan opini pengguna tentang warna dengan bukti bahwa alur task memang sulit digunakan.",
    },
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
        summary_node = values.get("description")
        if summary_node is None:
            summary_node = values.get("summary")
        if summary_node is None:
            summary_node = values.get("content")
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

    today = date.today().isoformat()
    LESSONS.mkdir(exist_ok=True)
    output = LESSONS / f"{today}.md"

    fresh = next((item for item in candidates if item["link"] not in seen), None)
    if fresh is None:
        # Keep a daily activity even when feeds are temporarily unavailable.
        if output.exists():
            print("No new RSS item found; today's lesson already exists.")
            return
        fresh = {
            "category": "Software Engineer",
            "title": "Daily study checkpoint",
            "link": "https://github.com/pittkajull/daily-study",
            "summary": "Tidak ada artikel RSS baru yang tersedia hari ini. Gunakan checkpoint ini untuk mengulang konsep, membaca dokumentasi resmi, atau mengerjakan latihan kecil.",
        }
        print("No fresh RSS item found; publishing a fallback study checkpoint.")
    guide = GUIDES.get(fresh["category"], GUIDES["Software Engineer"])
    deep = DEEP_THEORY.get(fresh["category"], DEEP_THEORY["Software Engineer"])
    practice = PRACTICE.get(fresh["category"], PRACTICE["Software Engineer"])
    output.write_text(
        f"# {fresh['title']}\n\n**Kategori:** {fresh['category']}  \n**Difficulty:** {guide['level']}  \n**Date:** {today}\n\n"
        f"## Tujuan Belajar\n\n{deep['goals']}\n\n## Prasyarat\n\n{deep['prereq']}\n\n"
        f"## Teori: Apa yang Dipelajari?\n\n{deep['theory']}\n\n"
        f"## Kenapa Ini Penting?\n\n{guide['why']}\n\n"
        f"## Gambaran Sederhana\n\n{practice['analogy']}\n\n"
        f"## Ringkasan Bacaan Terbaru\n\n{fresh['summary'] or 'Baca sumber asli untuk konteks terbaru.'}\n\n"
        f"## Contoh Praktik\n\n```text\n{guide['code']}\n```\n\n**Cara membacanya:** {deep['walkthrough']}\n\n"
        f"## Praktik Langkah demi Langkah\n\n{practice['steps']}\n\n"
        f"### Hasil yang Diharapkan\n\n{practice['result']}\n\n"
        f"## Best Practices\n\n{guide['best']}\n\n## Kesalahan Umum\n\n{guide['pitfalls']}\n\n"
        f"## Latihan Mandiri\n\n{guide['exercise']}\n\n### Cek Pemahaman\n\n{practice['check']}\n\n## Sumber Belajar\n\n- [Bacaan terbaru dari sumber asli]({fresh['link']})\n",
        encoding="utf-8",
    )
    seen.add(fresh["link"])
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(sorted(seen), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
