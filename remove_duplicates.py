# Copyright: Dmitry Savosh (d.savosh@gmail.com)

from utils.utils import *

# settings
remove_archives = True

if len(sys.argv) < 2:
    print("Please, provide path as argument!")
    print('Example:')
    print(r'python remove_duplicates.py "D:\Unreal Assets"')
    print(r'python remove_duplicates.py "D:\Unreal Assets" "D:\New Unreal Assets"')
    exit()

in_paths = [arg for i, arg in enumerate(sys.argv) if i != 0]
# in_paths = [r"C:\Users\User\Downloads\Assets"]

assets_list = {}

for in_path in in_paths:
    for path, subs, files in os.walk(in_path):
        for filename in files:
            full_page_file_name = os.path.join(path, filename)
            if not os.path.isfile(full_page_file_name):
                continue

            if not filename.endswith(".html"):
                continue

            if filename in assets_list:
                print("Which file to keep? (Press Enter to skip)")
                print("1: " + assets_list[filename])
                print("2: " + full_page_file_name)
                asset_name = os.path.splitext(filename)[0]
                i = input()
                remove_page_name = None
                if i == "1":
                    remove_page_name = full_page_file_name
                if i == "2":
                    remove_page_name = assets_list[filename]
                if remove_page_name:
                    remove_in_path = os.path.dirname(remove_page_name)
                    # remove archives
                    if remove_archives:
                        archives = find_archives_for_page(remove_page_name)
                        for arc in archives:
                            os.remove(arc)
                        if len(archives) == 0:
                            print("Cant find asset archive for page: " + remove_page_name)
                            continue
                    # remove page
                    os.remove(remove_page_name)

            assets_list[filename] = full_page_file_name
