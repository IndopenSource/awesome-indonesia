# Contributing

Repo ini mengikuti gaya Awesome List.

## Klasifikasi submit

Gunakan repo ini untuk proyek open source Indonesia yang masih fresh dan aktif pada 2026.

- Submit proyek app, library, tool, atau installer yang aktif ke repo ini.
- Submit resource non-app, direktori, materi belajar, atau daftar komunitas ke [Awesome Indonesia Legacy](https://github.com/IndopenSource/awesome-indonesia-legacy).
- Submit proyek lama, kurang aktif, atau kandidat yang potensial direvival ke [Awesome Indonesia Revival](https://github.com/IndopenSource/awesome-indonesia-revival).

## Cara menambah proyek

1. Tambahkan nama repo ke `repos.json` dengan format `owner/repo`, disisipkan sesuai urutan abjad (huruf besar dan kecil dianggap sama). Jangan menambah di baris paling akhir kecuali memang urutannya di sana.
2. Jalankan `make validate` untuk memastikan format list benar.
3. Buat pull request dengan ringkasan proyek yang ditambahkan.
4. README akan diperbarui lewat PR metadata otomatis setelah PR digabungkan ke `main`.

## Standar kontribusi

- Tambahkan proyek open source yang relevan dengan ekosistem Indonesia dan masih fresh/aktif pada 2026.
- Pastikan repo publik dan bisa diakses dari GitHub.
- Pastikan repo bukan duplikasi dari entri yang sudah ada.
- Jangan edit tabel README secara manual jika metadata bisa dihasilkan dari GitHub API.
- Deskripsi, pembuat, bahasa, lisensi, stars, forks, issue, tanggal update, latest release, dan tags diambil otomatis dari GitHub API.

## Perintah lokal

```bash
make validate
make update
make lint
make check
```

Gunakan `make update` hanya jika ingin melihat hasil README lokal sebelum membuat PR.

## Workflow otomatis

Contributor cukup mengubah `repos.json`. Setelah PR contributor digabungkan,
workflow `Update README` akan membuat PR metadata terpisah berisi hasil generate
README terbaru.

Workflow ini memakai repository secret `README_UPDATE_TOKEN` agar bisa membuat PR
tanpa membuka permission write untuk seluruh organization. Token tersebut harus
berupa fine-grained GitHub token dengan akses hanya ke repo ini dan permission:

- `Contents`: read and write
- `Pull requests`: read and write

`main` tetap wajib lewat pull request dan branch protection. Workflow tidak
melakukan approve, merge, atau push langsung ke `main`.

## Format repos.json

```json
[
  "another-owner/another-repo",
  "owner/repo"
]
```

Daftar diurutkan berdasarkan abjad. `make validate` gagal jika urutannya salah dan menyebutkan entri mana yang harus dipindah.

## Rekomendasi update

- Gunakan nama owner dan repo yang valid.
- Jika metadata di README terlihat kurang lengkap, update metadata di repo asalnya terlebih dahulu.
- Indeks proyek di README diurutkan berdasarkan abjad, sedangkan tabel daftar proyek diurutkan otomatis berdasarkan jumlah stars terbanyak.
- Latest release mengikuti data GitHub Releases. Jika repo belum punya release, kolom akan berisi `N/A`.
- Workflow `Update README` berjalan harian, berjalan setelah perubahan `repos.json` di `main`, dan bisa dipicu manual dari tab Actions.
