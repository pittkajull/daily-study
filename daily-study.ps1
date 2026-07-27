$ErrorActionPreference = "Stop"

# Folder repo otomatis ditentukan dari lokasi script ini.
Set-Location $PSScriptRoot

$lessons = @(
    @{
        Topic = "Git dasar"
        Explanation = "Pelajari fungsi git status, git add, git commit, dan git push."
        Task = "Tulis dengan kata-katamu sendiri alur perubahan file sampai masuk GitHub."
    },
    @{
        Topic = "Python"
        Explanation = "Pelajari perbedaan string, integer, list, dan dictionary."
        Task = "Buat satu contoh data untuk setiap tipe dan jelaskan kegunaannya."
    },
    @{
        Topic = "JavaScript"
        Explanation = "Pelajari fungsi map, filter, dan reduce untuk mengolah array."
        Task = "Catat satu contoh kasus penggunaan masing-masing fungsi."
    },
    @{
        Topic = "Web"
        Explanation = "Pelajari perbedaan HTTP method GET, POST, PUT, PATCH, dan DELETE."
        Task = "Jelaskan method mana yang dipakai untuk membuat dan menghapus data."
    },
    @{
        Topic = "Database"
        Explanation = "Pelajari SELECT, WHERE, ORDER BY, dan LIMIT pada SQL."
        Task = "Tulis query untuk mengambil lima data terbaru dari sebuah tabel."
    },
    @{
        Topic = "Keamanan akun"
        Explanation = "Pelajari password manager, 2FA, dan bahaya membagikan token."
        Task = "Aktifkan 2FA di satu layanan yang kamu gunakan."
    },
    @{
        Topic = "Linux dan terminal"
        Explanation = "Pelajari pwd, ls, cd, mkdir, dan grep atau Select-String."
        Task = "Catat fungsi setiap perintah dan satu contoh penggunaannya."
    }
)

$date = Get-Date
$dateText = $date.ToString("yyyy-MM-dd")
$index = ($date.DayOfYear - 1) % $lessons.Count
$lesson = $lessons[$index]

$folder = Join-Path $PSScriptRoot "daily-study"
$file = Join-Path $folder "$dateText.md"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

if (!(Test-Path -LiteralPath $file)) {
    @"
# Daily Study - $dateText

## Materi: $($lesson.Topic)

$($lesson.Explanation)

## Tugas kecil

$($lesson.Task)

## Catatan pribadi

- Yang saya pahami:
- Yang masih membingungkan:
- Langkah berikutnya:
"@ | Set-Content -LiteralPath $file -Encoding UTF8
}

git add -- "$file"
if (git diff --cached --quiet) {
    Write-Host "Catatan untuk $dateText sudah ada; tidak ada perubahan."
    exit 0
}

git commit -m "study: $dateText"
git push origin main

