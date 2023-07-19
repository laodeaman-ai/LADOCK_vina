# Silakan melakukan editing sesuai kebutuhan dan kenyataan Anda 
ligand_dir = "Ligand" # nama direktori ligand
target_dir = "Target" # nama direktori target
mgltools_dir = "/home/arga/MGLTools-1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24"
output_dir = "output"  # Nama direktori output yang ingin Anda buat
ligand_center = False  # Ganti menjadi False jika tidak ingin menghasilkan file .pdbqt pusat berat ligand
target_center = True  # Ganti menjadi True jika ingin menghasilkan file .pdbqt pusat berat target

# Parameter simulasi docking vina
size_x = 30.0
size_y = 30.0
size_z = 30.0
num_modes = 10
exhaustiveness = 8
cpu = 4
vina = "vina_1.2.5_linux_x86_64"
vina_split = "vina_split_1.2.5_linux_x86_64"
