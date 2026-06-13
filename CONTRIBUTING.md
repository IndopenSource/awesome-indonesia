# Contributing

Repo ini mengikuti gaya Awesome List.

## Cara menambah proyek

1. Tambahkan nama repo ke `repos.json` dengan format `owner/repo`.
2. Jalankan `make validate` untuk memastikan format list benar.
3. Buat pull request dengan ringkasan proyek yang ditambahkan.
4. README akan diperbarui otomatis setelah PR digabungkan ke `main`.

## Standar kontribusi

- Tambahkan proyek open source yang relevan dengan ekosistem Indonesia.
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

## Format repos.json

```json
[
  "owner/repo",
  "another-owner/another-repo"
]
```

## Rekomendasi update

- Gunakan nama owner dan repo yang valid.
- Jika metadata di README terlihat kurang lengkap, update metadata di repo asalnya terlebih dahulu.
- README diurutkan otomatis berdasarkan jumlah stars terbanyak.
- Latest release mengikuti data GitHub Releases. Jika repo belum punya release, kolom akan berisi `N/A`.
- Workflow `Update README` berjalan harian, berjalan setelah perubahan `repos.json` di `main`, dan bisa dipicu manual dari tab Actions.
