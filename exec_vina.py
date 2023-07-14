import os
import csv
import shutil
import config

vina = config.vina
vina_split = config.vina_split

# Menentukan nama direktori saat ini sebagai nama file receptor.pdbqt
receptor_pdbqt = os.path.basename(os.getcwd()) + '.pdbqt'

# Mendapatkan daftar file ligand dalam direktori kerja
pdbqt_files = [file for file in os.listdir('.') if file.endswith('.pdbqt') and file != receptor_pdbqt]

# Simulasi Ligan Tunggal
for pdbqt_file in pdbqt_files:
    output_file = f"{pdbqt_file.replace('.pdbqt', '_output.pdbqt')}"
    command = f'../../{vina} --receptor {receptor_pdbqt} --ligand {pdbqt_file} --config config.txt --out {output_file}'
    os.system(command)
    print(f"Simulasi selesai untuk file: {pdbqt_file}. Output: {output_file}")

# Mendapatkan daftar file output pdbqt di direktori saat ini
output_files = [file for file in os.listdir('.') if file.endswith('_output.pdbqt')]

# Spliting setiap file output
for file in output_files:
    command = f'../../{vina_split} --input {file}'
    os.system(command)
    print(f"Splitting selesai untuk: {file}")

# Menentukan direktori "model1"
model1_dir = 'model1'

# Membuat direktori "model1"
os.makedirs(model1_dir, exist_ok=True)

# Mendapatkan daftar file output yang sesuai dengan pola *_output_ligand_01.pdbqt
output_files = [file for file in os.listdir('.') if file.endswith('_output_ligand_01.pdbqt')]

# Memindahkan file ke direktori "model1"
for output_file in output_files:
    shutil.move(output_file, os.path.join(model1_dir, output_file))

print("Proses selesai. Direktori 'model1' telah dibuat dan file-file output telah dipindahkan ke dalamnya.")

# Mendapatkan daftar file output yang sesuai dengan pola *_output_ligand_01.pdbqt
output_files = [file for file in os.listdir(model1_dir) if file.endswith('_output_ligand_01.pdbqt')]

# Mendapatkan daftar file pdbqt dalam direktori "model1"
pdbqt_files = [file for file in output_files if file.endswith('.pdbqt')]

# Membuat file CSV untuk menyimpan data energi
csv_file = os.path.join(model1_dir, 'energy_summary.csv')
with open(csv_file, 'w') as f:
    f.write('Ligand,Binding Affinity (Kcal/mol)\n')

# Memproses setiap file pdbqt
for pdbqt_file in pdbqt_files:
    pdbqt_path = os.path.join(model1_dir, pdbqt_file)
    ligand_name = pdbqt_file.split('_output')[0]  # Mendapatkan nama ligan dari nama file
    energy = None

    # Membaca baris pertama setelah "REMARK VINA RESULT:"
    with open(pdbqt_path, 'r') as f:
        for line in f:
            if line.startswith('REMARK VINA RESULT:'):
                energy = line.split()[3]  # Mendapatkan nilai energi
                break  # Hentikan pencarian setelah ditemukan

    # Menyimpan nilai energi dalam file CSV
    with open(csv_file, 'a') as f:
        f.write(f'{ligand_name},{energy}\n')

    pdb_file = pdbqt_file.replace('.pdbqt', '.pdb')
    pdbqt_path = os.path.join(model1_dir, pdbqt_file)
    pdb_path = os.path.join(model1_dir, pdb_file)

    # Menggunakan Obabel untuk mengkonversi file PDBQT ke PDB
    command = f'obabel {pdbqt_path} -opdb -O {pdb_path}'
    os.system(command)

    print(f"Proses selesai untuk file: {pdbqt_file}")

print("Proses selesai. Data energi tersimpan dalam file energy_summary.csv di direktori 'model1'.")
