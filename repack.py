# Copyright: Dmitry Savosh (d.savosh@gmail.com)

from utils.utils import *

# settings :
delete_temp_dir_if_exist = True
delete_7z_archive_if_exist = False
delete_original_archive = True
do_not_repack_7z = True
temp_subdir = "! temp"

if len(sys.argv) != 2:
    print("Please, provide path as argument!")
    print('Example:')
    print(r'python repack.py "D:\Unreal Assets"')
    exit()

archives_path = sys.argv[1]
# archives_path = r"C:\ProgramData\Epic\EpicGamesLauncher\VaultCache"

archives = get_all_archives(archives_path)
if do_not_repack_7z:
    archives = [a for a in archives if not a.endswith(".7z")]

for i, archive_full_file_name in enumerate(archives):
    print(f"-------------- ARCHIVE {i + 1} / {len(archives)} ---------------")

    arc_path, arc_name, arc_ext = split_file_name(archive_full_file_name)

    new_archive_name = os.path.join(arc_path, arc_name + ".7z")
    if delete_7z_archive_if_exist:
        remove_if_exist(new_archive_name)

    temp_dir = os.path.join(arc_path, temp_subdir)
    if delete_temp_dir_if_exist:
        remove_if_exist(temp_dir)

    extract(archive_full_file_name, temp_dir)

    temp_arc_subdir = os.path.join(temp_dir, arc_name)

    archive_dir(temp_arc_subdir, new_archive_name)
    remove_if_exist(temp_dir)
    if delete_original_archive and os.path.isfile(new_archive_name):
        remove_if_exist(archive_full_file_name)

print("================ COMPLETE ==================")
