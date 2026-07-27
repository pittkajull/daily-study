# Technology Learning Hub

Materi pendek harian untuk mengenal dunia teknologi dan berbagai jalur karier di dalamnya. Setiap hari repository ini menerbitkan satu mini-lesson baru secara otomatis.

## Topik yang Dicakup

| Jalur | Materi |
|---|---|
| Software Engineer | Clean architecture, testing, maintainability |
| Hardware Engineer | Microcontroller, digital logic, input/output |
| Automation Engineer | Control loop, PLC, sensor, actuator |
| AI Engineer | Machine learning, prompt engineering, model workflow |
| Designer | Visual hierarchy, typography, design principles |
| UI/UX Designer | User research, usability testing, interface thinking |

## Isi Setiap Lesson

Setiap materi dibuat singkat agar mudah dipelajari dan dibagikan. Isinya mencakup:

- Penjelasan konsep
- Contoh sederhana
- Latihan mandiri
- Referensi dokumentasi atau sumber belajar

## Contoh Materi

Materi yang tersedia antara lain:

- **Software Engineer:** cara membagi aplikasi dengan clean architecture
- **Hardware Engineer:** cara kerja microcontroller dan gerbang logika
- **Automation Engineer:** control loop dan PLC
- **AI Engineer:** machine learning dan prompt engineering
- **Designer:** visual hierarchy dan typography
- **UI/UX Designer:** user research dan usability testing

## Cara Menggunakan

1. Buka folder [`lessons/`](lessons/).
2. Pilih materi berdasarkan tanggal.
3. Baca bagian penjelasan dan contoh.
4. Kerjakan latihan mandirinya.
5. Buka referensi untuk belajar lebih dalam.

## Auto Update

Materi baru dibuat oleh [`daily-study.ps1`](daily-study.ps1). Script ini:

1. Memilih mini-lesson teknologi berdasarkan tanggal.
2. Membuat file Markdown baru di folder `lessons/`.
3. Melakukan commit.
4. Melakukan push ke branch `main`.

Di Windows, jalankan otomatis menggunakan **Task Scheduler** dengan trigger `When I log on`.

### Menjalankan manual

```powershell
powershell -ExecutionPolicy Bypass -File .\daily-study.ps1
```

## Struktur Repository

```text
technology-learning-hub/
├── daily-study.ps1       # Generator dan auto-publisher lesson
├── lessons/              # Materi edukasi dalam format Markdown
│   ├── 2026-07-27.md
│   ├── 2026-07-28.md
│   └── ...
└── README.md             # Dokumentasi repository
```

## Tujuan

Repository ini dibuat sebagai perpustakaan belajar terbuka untuk siswa, pemula, dan siapa saja yang ingin memahami dasar berbagai bidang teknologi secara bertahap.

Materi di sini bersifat pengantar. Gunakan referensi yang tercantum untuk eksplorasi lebih lanjut dan jangan ragu membuka pull request untuk memperbaiki atau menambah materi.

## License

Materi di repository ini dapat digunakan untuk belajar dan dibagikan dengan tetap mencantumkan sumbernya.
