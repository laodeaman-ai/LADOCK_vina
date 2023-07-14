# LADOCK_vina
Aplikasi ini menggunakan skrip prepare_ligand4.py dan prepare_receptor4.py dari paket MGLTools untuk mengubah file PDB menjadi file PDBQT yang diperlukan dalam simulasi docking. Selain itu, aplikasi juga menggunakan paket AutoDock Vina dan AutoDock Vina Split untuk melakukan simulasi docking. Aplikasi ini menghasilkan file konfigurasi "config.txt" yang berisi koordinat titik pusat, ukuran grid box, dan parameter tambahan untuk setiap file PDB yang diproses.

## Instalasi

1. Pastikan Anda memiliki Python 3.x terinstal di komputer Anda.
2. Unduh atau salin kode aplikasi ini ke direktori lokal Anda.
3. Buka terminal atau command prompt dan navigasikan ke direktori tempat Anda menyimpan kode aplikasi.

## Penggunaan
1. Siapkan direktori dengan struktur berikut:
   - Ligand: Direktori berisi file-file ligand dalam format PDB.
   - Target: Direktori berisi file-file target dalam format PDB.
   - Output: Direktori tujuan untuk menyimpan file-file hasil konversi, konfigurasi dan simulasi.

2. Edit konfigurasi aplikasi di file `config.py` sesuai kebutuhan Anda:
   - `ligand_dir`: Nama direktori ligand.
   - `target_dir`: Nama direktori target.
   - `mgltools_dir`: Path menuju direktori MGLTools.
   - `output_dir`: Nama direktori output.
   - `ligand_center`: True jika ingin menghasilkan file PDBQT pusat berat ligand, False jika tidak.
   - `target_center`: True jika ingin menghasilkan file PDBQT pusat berat target, False jika tidak.
   - `size_x`, `size_y`, `size_z`: Ukuran grid box dalam angka float.
   - `num_modes`, `exhaustiveness`, `cpu`: Parameter tambahan untuk file konfigurasi.

3. Jalankan skrip `ladock.py`.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini dan kirimkan pull request dengan perubahan yang diusulkan.

## Licensi

Proyek ini dilisensikan di bawah [MIT License](https://opensource.org/licenses/MIT).

## Kontak
Jika Anda memiliki pertanyaan atau masukan, silakan hubungi:
La Ode Aman
laode_aman@ung.ac.id
Universitas Negeri Gorontalo
