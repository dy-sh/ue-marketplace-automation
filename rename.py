# Copyright: Dmitry Savosh (d.savosh@gmail.com)

from utils.utils import *
import sys

# settings:
rename_archives = False

if len(sys.argv) != 2:
    print("Please, provide path as argument!")
    print('Example:')
    print(r'python rename.py "D:\Unreal Assets"')
    exit()

in_path = sys.argv[1]
# in_paths = [r"C:\Users\User\Downloads\Assets"]

path_list = os.listdir(in_path)
for page_file_name in path_list:
    full_page_file_name = os.path.join(in_path, page_file_name)
    if not os.path.isfile(full_page_file_name) or not page_file_name.endswith(".html"):
        continue

    title = read_title_from_html_file(full_page_file_name)
    if ' - UE Marketplace' not in title:
        continue

    exist_asset_name = os.path.splitext(page_file_name)[0]
    correct_asset_name, category = get_asset_name_from_page_title(title)

    if correct_asset_name != exist_asset_name:
        # search for asset archive file
        if rename_archives:
            archives = find_archives_for_page(full_page_file_name)
            for arc in archives:
                ext = os.path.splitext(arc)[1]
                new_asset_file_name = os.path.join(in_path, correct_asset_name) + ext
                os.rename(arc, new_asset_file_name)
            if len(archives) == 0:
                print("Cant find asset archive for page: " + full_page_file_name)
                continue
        # rename page
        new_asset_file_name = os.path.join(in_path, correct_asset_name) + ".html"
        os.rename(full_page_file_name, new_asset_file_name)
