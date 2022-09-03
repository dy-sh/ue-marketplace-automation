# Copyright: Dmitry Savosh (d.savosh@gmail.com)

from utils.utils import *
import sys

if len(sys.argv) != 3:
    print("Please, provide input and output path as argument!")
    print('Example:')
    print(r'python sort_pages.py "C:\Users\User\Downloads" "D:\Unreal Assets"')
    exit()

in_path = sys.argv[1]
# assets_path = r"C:\Users\User\Downloads"

out_path = sys.argv[2]
# out_path = r"C:\Users\User\Downloads"

out_sub_dir = ""

path_list = os.listdir(in_path)
for page_file_name in path_list:
    full_page_file_name = os.path.join(in_path, page_file_name)
    if not os.path.isfile(full_page_file_name) or not page_file_name.endswith(".html"):
        continue

    title = read_title_from_html_file(full_page_file_name)
    if ' - UE Marketplace' not in title:
        continue

    asset_name, category = get_asset_name_from_page_title(title)

    new_path = os.path.join(out_path, category)
    make_dir(new_path)

    if out_sub_dir != "":
        new_path = os.path.join(new_path, out_sub_dir)
        make_dir(new_path)

    os.rename(
        full_page_file_name,
        os.path.join(new_path, asset_name + ".html")
    )
