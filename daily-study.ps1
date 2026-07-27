$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$lessons = @(
    @{ Topic = "Software Engineer: clean architecture"; What = "Clean architecture memisahkan aturan bisnis dari database, framework, dan detail antarmuka agar aplikasi mudah dirawat."; Example = "Pisahkan folder domain, service, repository, dan controller."; Task = "Gambar pembagian layer untuk aplikasi to-do list."; Ref = "https://martinfowler.com/bliki/PresentationDomainDataLayering.html" },
    @{ Topic = "Software Engineer: testing"; What = "Testing memeriksa perilaku program secara otomatis sehingga perubahan kode lebih aman."; Example = "Uji kasus normal, input kosong, dan input yang tidak valid."; Task = "Tulis tiga edge case untuk fitur login."; Ref = "https://docs.pytest.org/en/stable/getting-started.html" },
    @{ Topic = "Hardware Engineer: microcontroller"; What = "Microcontroller adalah komputer kecil yang membaca input sensor dan mengendalikan output seperti LED atau motor."; Example = "Arduino membaca tombol pada pin input lalu menyalakan LED pada pin output."; Task = "Buat diagram input-proses-output untuk lampu otomatis."; Ref = "https://docs.arduino.cc/learn/" },
    @{ Topic = "Hardware Engineer: digital logic"; What = "Gerbang AND, OR, dan NOT adalah dasar rangkaian digital untuk mengolah sinyal 0 dan 1."; Example = "Alarm berbunyi jika sensor pintu AND sistem keamanan aktif."; Task = "Buat truth table untuk gerbang AND dan OR."; Ref = "https://www.allaboutcircuits.com/textbook/digital/" },
    @{ Topic = "Automation Engineer: control loop"; What = "Control loop membandingkan kondisi aktual dengan target lalu menyesuaikan output secara otomatis."; Example = "Thermostat membaca suhu ruangan dan mengatur pemanas agar mendekati target."; Task = "Identifikasi sensor, controller, dan actuator pada mesin cuci."; Ref = "https://controlguru.com/" },
    @{ Topic = "Automation Engineer: PLC"; What = "PLC adalah komputer industri yang menjalankan logika kontrol secara andal untuk mesin dan proses produksi."; Example = "PLC membaca sensor limit switch lalu menggerakkan conveyor."; Task = "Gambar urutan proses sederhana untuk pintu otomatis."; Ref = "https://www.plcopen.org/" },
    @{ Topic = "AI Engineer: machine learning"; What = "Machine learning mempelajari pola dari data untuk membuat prediksi atau keputusan."; Example = "Model klasifikasi memprediksi apakah email termasuk spam atau bukan."; Task = "Bedakan data training, validation, dan testing."; Ref = "https://developers.google.com/machine-learning/crash-course" },
    @{ Topic = "AI Engineer: prompt engineering"; What = "Prompt engineering adalah cara menyusun instruksi yang jelas agar model AI menghasilkan jawaban yang lebih konsisten."; Example = "Sebutkan peran, tujuan, format output, batasan, dan contoh yang diinginkan."; Task = "Tulis prompt untuk membuat ringkasan artikel dalam lima poin."; Ref = "https://platform.openai.com/docs/guides/prompt-engineering" },
    @{ Topic = "Designer: visual hierarchy"; What = "Visual hierarchy mengatur ukuran, warna, kontras, dan posisi agar mata pengguna mengikuti informasi yang paling penting terlebih dahulu."; Example = "Judul lebih besar, tombol utama lebih kontras, dan detail sekunder dibuat lebih kecil."; Task = "Urutkan elemen halaman checkout berdasarkan tingkat kepentingannya."; Ref = "https://www.nngroup.com/articles/visual-hierarchy-ux-definition/" },
    @{ Topic = "Designer: typography"; What = "Typography mencakup pemilihan font, ukuran, jarak, dan panjang baris agar teks nyaman dibaca."; Example = "Gunakan ukuran heading yang jelas dan line-height yang cukup untuk paragraf."; Task = "Buat aturan tipografi sederhana untuk landing page."; Ref = "https://material.io/design/typography/understanding-typography.html" },
    @{ Topic = "UI/UX: user research"; What = "User research membantu memahami kebutuhan, kebiasaan, dan masalah pengguna sebelum solusi dirancang."; Example = "Wawancarai pengguna, amati alur kerja, lalu kelompokkan masalah yang berulang."; Task = "Buat lima pertanyaan wawancara untuk aplikasi pencatat keuangan."; Ref = "https://www.nngroup.com/articles/which-ux-research-methods/" },
    @{ Topic = "UI/UX: usability testing"; What = "Usability testing mengamati pengguna menyelesaikan tugas untuk menemukan bagian interface yang membingungkan."; Example = "Minta pengguna mencari dan membeli produk tanpa memberi tahu tombol mana yang harus ditekan."; Task = "Tulis tiga task test untuk aplikasi mobile."; Ref = "https://www.nngroup.com/articles/usability-testing-101/" }
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
