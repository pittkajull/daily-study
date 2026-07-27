# Daily Technology Lessons

Script PowerShell ini membuat satu mini-lesson edukasi teknologi per hari, lalu commit dan push ke GitHub. Materinya mencakup Git, Python, JavaScript, Web, Database, Linux, Cybersecurity, Testing, dan DevOps.

## Setup pertama kali

```powershell
cd C:\path\ke\daily-study-bot
git init
git add .
git commit -m "chore: initial setup"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

Pastikan `git push` sudah bisa berjalan tanpa meminta login setiap kali, misalnya memakai GitHub Desktop atau SSH.

## Menjalankan otomatis saat login Windows

1. Buka **Task Scheduler** dan pilih **Create Basic Task**.
2. Nama task: `Daily GitHub Study`.
3. Trigger: **When I log on**.
4. Action: **Start a program**.
5. Program: `powershell.exe`.
6. Arguments:

```text
-ExecutionPolicy Bypass -File "C:\path\ke\daily-study-bot\daily-study.ps1"
```

Script memilih materi berdasarkan hari dalam tahun, jadi materi berganti otomatis tanpa perlu mengedit file setiap hari.
