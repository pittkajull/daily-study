$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$lessons = @(
    @{ Topic = "Git: commit dan history"; What = "Commit adalah snapshot perubahan yang diberi pesan agar perkembangan proyek mudah dilacak."; Example = "git add .; git commit -m 'feat: tambah halaman login'; git log --oneline"; Task = "Jelaskan kenapa pesan commit yang jelas penting bagi tim."; Ref = "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository" },
    @{ Topic = "Python: tipe data"; What = "String menyimpan teks, integer menyimpan bilangan, list menyimpan kumpulan berurutan, dan dictionary menyimpan pasangan key-value."; Example = "user = {'name': 'Ari', 'age': 20}; print(user['name'])"; Task = "Buat contoh data profil pengguna menggunakan dictionary."; Ref = "https://docs.python.org/3/tutorial/introduction.html" },
    @{ Topic = "JavaScript: map, filter, reduce"; What = "map mengubah setiap item, filter memilih item tertentu, dan reduce menggabungkan banyak item menjadi satu hasil."; Example = "const prices = [10, 20, 30]; const total = prices.reduce((sum, price) => sum + price, 0);"; Task = "Jelaskan perbedaan ketiga method tersebut dengan contoh sederhana."; Ref = "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array" },
    @{ Topic = "Web: HTTP method"; What = "GET membaca data, POST membuat data, PUT atau PATCH mengubah data, dan DELETE menghapus data."; Example = "GET /users membaca daftar pengguna, sedangkan POST /users membuat pengguna baru."; Task = "Tentukan method HTTP yang tepat untuk lima operasi CRUD."; Ref = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods" },
    @{ Topic = "Database: SELECT dan WHERE"; What = "SELECT mengambil kolom dari tabel, sedangkan WHERE menyaring baris berdasarkan kondisi."; Example = "SELECT name, email FROM users WHERE active = true;"; Task = "Tulis query untuk mengambil produk dengan harga di bawah 100000."; Ref = "https://www.postgresql.org/docs/current/tutorial-select.html" },
    @{ Topic = "Linux: pipe dan redirect"; What = "Pipe meneruskan output satu perintah menjadi input perintah lain; redirect menyimpan output ke file."; Example = "Get-Process | Select-Object -First 5"; Task = "Cari contoh pipeline untuk memfilter daftar proses."; Ref = "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines" },
    @{ Topic = "Cybersecurity: password dan 2FA"; What = "Password unik dan autentikasi dua faktor mengurangi risiko akun diambil alih."; Example = "Gunakan password manager dan aktifkan authenticator app, bukan password yang sama di semua layanan."; Task = "Buat checklist keamanan akun untuk pemula."; Ref = "https://www.cisa.gov/secure-our-world" },
    @{ Topic = "Software engineering: clean code"; What = "Clean code memakai nama yang jelas, fungsi kecil, dan struktur sederhana agar mudah dipelihara."; Example = "Ganti fungsi processData() menjadi calculateCartTotal() jika memang tugasnya menghitung total keranjang."; Task = "Temukan satu nama fungsi yang ambigu lalu usulkan nama yang lebih jelas."; Ref = "https://martinfowler.com/books/refactoring.html" },
    @{ Topic = "Testing: unit test"; What = "Unit test memeriksa bagian kecil program secara terisolasi sehingga bug ditemukan lebih cepat."; Example = "Uji fungsi calculateTotal() dengan input kosong, satu item, dan banyak item."; Task = "Sebutkan tiga edge case untuk fungsi login."; Ref = "https://docs.pytest.org/en/stable/getting-started.html" },
    @{ Topic = "DevOps: continuous integration"; What = "CI menjalankan build dan test otomatis setiap kali ada perubahan kode."; Example = "Pull request dapat menjalankan test sebelum kode digabung ke main."; Task = "Jelaskan dua manfaat CI untuk tim kecil."; Ref = "https://docs.github.com/en/actions" }
)

$date = Get-Date
$dateText = $date.ToString("yyyy-MM-dd")
$lesson = $lessons[($date.DayOfYear - 1) % $lessons.Count]
$folder = Join-Path $PSScriptRoot "daily-study"
$file = Join-Path $folder "$dateText.md"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

if (!(Test-Path -LiteralPath $file)) {
@"
# Edukasi Teknologi — $dateText

## $($lesson.Topic)

### Penjelasan
$($lesson.What)

### Contoh
```
$($lesson.Example)
```

### Latihan
$($lesson.Task)

### Referensi
$($lesson.Ref)
"@ | Set-Content -LiteralPath $file -Encoding UTF8
}

git add -- "$file"
if (git diff --cached --quiet) { exit 0 }
git commit -m "lesson: $dateText"
git push origin main
