# Technology Learning Hub

Repository ini berisi materi edukasi teknologi yang dibuat otomatis satu lesson per hari.

Tujuannya adalah menyediakan bacaan singkat dan praktis untuk orang yang ingin mengenal berbagai jalur karier teknologi:

- Software Engineer
- Hardware Engineer
- Automation Engineer
- AI Engineer
- Designer
- UI/UX Designer

Setiap lesson berisi penjelasan konsep, contoh sederhana, latihan, dan tautan referensi agar pembaca bisa melanjutkan belajar.

## Struktur

- `lessons/` — kumpulan materi dalam format Markdown.
- `daily-study.ps1` — generator yang memilih dan menerbitkan satu materi baru setiap hari.

## Cara menjalankan

```powershell
powershell -ExecutionPolicy Bypass -File .\daily-study.ps1
```

Script membuat file baru berdasarkan tanggal, lalu melakukan commit dan push ke branch `main`. Materi tidak memakai API berbayar; daftar lesson tersimpan di dalam script.

## Otomatis setiap hari

Gunakan Windows Task Scheduler dengan action berikut:

- Program: `powershell.exe`
- Arguments: `-ExecutionPolicy Bypass -File "C:\path\ke\daily-study-bot\daily-study.ps1"`
- Trigger: `When I log on`

Repo ini dimaksudkan sebagai perpustakaan belajar terbuka yang bisa dibaca, dikembangkan, dan dikoreksi bersama.
