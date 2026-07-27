# Technology Learning Hub

Materi pendek harian untuk mengenal dunia teknologi dan berbagai jalur karier di dalamnya. Setiap hari repository ini menerbitkan satu technology brief baru dari RSS resmi sumber teknologi.

## Topik yang Dicakup

| Jalur | Materi |
|---|---|
| Software Engineer | Architecture, Python, testing, maintainability |
| Hardware Engineer | Microcontroller, digital logic, input/output |
| Automation Engineer | Control loop, PLC, sensor, actuator |
| AI Engineer | Machine learning, PyTorch, prompt engineering |
| Designer | Visual hierarchy, typography, design principles |
| UI/UX Designer | User research, usability testing, interface thinking |

## Isi Setiap Lesson

- Penjelasan konsep
- Ringkasan pendek dari sumber asli
- Contoh atau konteks penerapan
- Latihan mandiri
- Link referensi lengkap

## Cara Menggunakan

1. Buka folder [`lessons/`](lessons/).
2. Pilih materi berdasarkan tanggal.
3. Baca ringkasan dan buka sumber aslinya.
4. Kerjakan latihan mandirinya.

## Auto Update

[`generate.py`](generate.py) membaca RSS resmi dari sumber teknologi, memilih link yang belum pernah digunakan, lalu membuat file Markdown baru. GitHub Actions menjalankannya setiap hari pukul 19:00 WIB melalui [workflow](.github/workflows/daily-lesson.yml).

```text
RSS resmi -> filter duplikat -> lesson Markdown -> commit -> push
```

### Menjalankan manual

```powershell
python .\generate.py
```

## Struktur Repository

```text
technology-learning-hub/
├── .github/workflows/daily-lesson.yml  # Automation harian
├── generate.py                          # RSS reader dan generator
├── lessons/                             # Materi dalam format Markdown
│   ├── 2026-07-27.md
│   └── ...
└── README.md                            # Dokumentasi repository
```

## Sumber dan Etika

Feed dibatasi ke sumber teknologi resmi dan publik. Script hanya menyimpan metadata RSS, ringkasan pendek, atribusi, dan link sumber asli—bukan menyalin artikel penuh. Rate limit, robots.txt, hak cipta, dan permintaan takedown harus selalu dihormati.

## Tujuan

Repository ini adalah perpustakaan belajar terbuka untuk siswa, pemula, dan siapa saja yang ingin memahami teknologi secara bertahap. Pull request untuk memperbaiki atau menambah materi sangat dipersilakan.

## License

Materi di repository ini dapat digunakan untuk belajar dengan tetap mencantumkan sumber aslinya.
