import os
import shutil
from Bio.PDB import PDBParser
import config

# Jangan melakukan editing 
ligand_center = False 
target_center = True
ligand_dir = config.ligand_dir
target_dir = config.target_dir
mgltools_dir = config.mgltools_dir
output_dir = config.output_dir
ligand_center = config.ligand_center
target_center = config.target_center
size_x = config.size_x
size_y = config.size_y
size_z = config.size_z
num_modes = config.num_modes
exhaustiveness = config.exhaustiveness
cpu = config.cpu

prepare_ligand_script = os.path.join(mgltools_dir, "prepare_ligand4.py")
prepare_receptor_script = os.path.join(mgltools_dir, "prepare_receptor4.py")

# Membuat direktori output
os.makedirs(output_dir, exist_ok=True)
print(f"Direktori {output_dir} berhasil dibuat.")

# Mengubah file PDB menjadi PDBQT dalam direktori Ligand
ligand_files = os.listdir(ligand_dir)
for file_name in ligand_files:
    if file_name.endswith(".pdb"):
        pdb_file = os.path.join(ligand_dir, file_name)
        pdbqt_file = os.path.splitext(file_name)[0] + ".pdbqt"
        pdbqt_file_path = os.path.join(ligand_dir, pdbqt_file)
        command = f"{prepare_ligand_script} -l {pdb_file} -o {pdbqt_file_path}"
        os.system(command)
        print(f"File {file_name} berhasil diubah menjadi {pdbqt_file}")

# Mengubah file PDB menjadi PDBQT dalam direktori Target
target_files = os.listdir(target_dir)
for file_name in target_files:
    if file_name.endswith(".pdb"):
        pdb_file = os.path.join(target_dir, file_name)
        pdbqt_file = os.path.splitext(file_name)[0] + ".pdbqt"
        pdbqt_file_path = os.path.join(target_dir, pdbqt_file)
        command = f"{prepare_receptor_script} -r {pdb_file} -o {pdbqt_file_path}"
        os.system(command)
        print(f"File {file_name} berhasil diubah menjadi {pdbqt_file}")

if target_center: 
    target_pdbqt_files = [f for f in os.listdir(target_dir) if f.endswith((".pdbqt", ".pdb"))]
    for target_pdbqt_file in target_pdbqt_files:
        shutil.copy(os.path.join(target_dir, target_pdbqt_file), output_dir)
    print(f"File PDBQT Target berhasil dipindahkan ke direktori {output_dir}.")

if ligand_center:
    ligand_pdbqt_files = [f for f in os.listdir(ligand_dir) if f.endswith((".pdbqt", ".pdb"))]
    for ligand_pdbqt_file in ligand_pdbqt_files:
        shutil.copy(os.path.join(ligand_dir, ligand_pdbqt_file), output_dir)
    print(f"File PDBQT Ligand berhasil dipindahkan ke direktori {output_dir}.")

# Membuat sub direktori dengan menggunakan nama dasar (basename) dari file PDBQT dalam direktori output
pdbqt_files = [f for f in os.listdir(output_dir) if f.endswith(".pdbqt")]
for pdbqt_file in pdbqt_files:
    pdbqt_basename = os.path.splitext(pdbqt_file)[0]
    pdbqt_dir = os.path.join(output_dir, pdbqt_basename)
    os.makedirs(pdbqt_dir, exist_ok=True)
    shutil.move(os.path.join(output_dir, pdbqt_file), os.path.join(pdbqt_dir, pdbqt_file))
    print(f"Direktori {pdbqt_dir} berhasil dibuat dan file {pdbqt_file} dipindahkan ke direktori tersebut.")
  
    if ligand_center:
        target_pdbqt_files = [f for f in os.listdir(target_dir) if f.endswith(".pdbqt")]
        for target_pdbqt_file in target_pdbqt_files:
            shutil.copy(os.path.join(target_dir, target_pdbqt_file), pdbqt_dir)
        print(f"File PDBQT Target berhasil dipindahkan ke direktori {pdbqt_dir}.")

    if target_center:
        ligand_pdbqt_files = [f for f in os.listdir(ligand_dir) if f.endswith(".pdbqt")]
        for ligand_pdbqt_file in ligand_pdbqt_files:
            shutil.copy(os.path.join(ligand_dir, ligand_pdbqt_file), pdbqt_dir)
        print(f"File PDBQT Ligand berhasil dipindahkan ke direktori {pdbqt_dir}.")
        
def calculate_gridbox_center(structure):
    model = structure[0]  # Mengambil model pertama dari struktur PDB
    atoms = model.get_atoms()  # Mendapatkan daftar atom dalam model
    
    x_sum = y_sum = z_sum = 0.0
    num_atoms = 0
    
    for atom in atoms:
        x, y, z = atom.get_coord()
        x_sum += x
        y_sum += y
        z_sum += z
        num_atoms += 1
    
    x_center = round(x_sum / num_atoms, 3)
    y_center = round(y_sum / num_atoms, 3)
    z_center = round(z_sum / num_atoms, 3)
    
    return x_center, y_center, z_center

# Direktori input (file PDB) dan output (file config.txt)
input_directory = output_dir  
output_directory = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]

## Loop melalui setiap file PDB dalam direktori input
for filename in os.listdir(input_directory):
    if filename.endswith(".pdb"):
        pdb_file = os.path.join(input_directory, filename)

        # Membaca struktur PDB
        parser = PDBParser()
        structure = parser.get_structure("ligand", pdb_file)

        # Menghitung koordinat titik pusat grid box
        gridbox_center = calculate_gridbox_center(structure)

        # Menulis koordinat titik pusat, ukuran grid box, dan parameter tambahan dalam file "config.txt"
        config_filename = "config.txt"
        output_subdirectory = os.path.join(input_directory, os.path.splitext(filename)[0])
        config_filepath = os.path.join(output_subdirectory, config_filename)
        
        config_filename = "config.txt"
        with open(config_filepath, "w") as file:
            file.write(f"center_x = {gridbox_center[0]:.3f}\n")
            file.write(f"center_y = {gridbox_center[1]:.3f}\n")
            file.write(f"center_z = {gridbox_center[2]:.3f}\n")
            file.write(f"size_x = {size_x:.3f}\n")
            file.write(f"size_y = {size_y:.3f}\n")
            file.write(f"size_z = {size_z:.3f}\n")
            file.write(f"num_modes = {num_modes}\n")
            file.write(f"exhaustiveness = {exhaustiveness}\n")
            file.write(f"cpu = {cpu}\n")
            file.write("\n")
            file.write("# Script ini ditulis oleh La Ode Aman\n")
            file.write("# Email: laodeaman.ai@gmail.com\n")
            file.write("# laode_aman@ung.ac.id\n")
            file.write("# Universitas Negeri Gorontalo, Indonesia\n")

        print(f"Koordinat titik pusat, ukuran grid box, dan parameter tambahan untuk file {filename} telah ditulis dalam file {config_filepath}.")
        print("Script ini ditulis oleh La Ode Aman")
        print("Email: laodeaman.ai@gmail.com")
        print("laode_aman@ung.ac.id")
        print("Universitas Negeri Gorontalo, Indonesia")
 
# Mendapatkan path saat ini
current_directory = os.getcwd()

# Mendapatkan path output directory
output_directory_path = os.path.abspath(os.path.join(current_directory, input_directory))

# Loop melalui setiap direktori dalam output_directory
for subdir in os.listdir(output_directory_path):
    subdir_path = os.path.join(output_directory_path, subdir)
    if os.path.isdir(subdir_path):
        # Jalankan perintah exec_vina.py di dalam direktori dengan menggunakan path lengkap
        exec_vina_script = os.path.join(current_directory, "exec_vina.py")
        os.chdir(subdir_path)
        os.system(f"python {exec_vina_script}")

# Kembali ke direktori awal setelah selesai
os.chdir(current_directory)
