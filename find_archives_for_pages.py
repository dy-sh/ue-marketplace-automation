# Copyright: Dmitry Savosh (d.savosh@gmail.com)

from utils.utils import *
import sys

# settings:
skip_if_page_already_has_archive = True
auto_confirm_if_full_match = True
move_page_to_folder_if_not_matched = False
not_matched_pages_subdir = "! not matched"
skip_words = ["the", "pack", "kit", "system", "advanced", "multiplayer", "ai", "with", 'stylized']

if len(sys.argv) != 3:
    print("Please, provide archives and pages path as argument!")
    print('Example:')
    print(r'python find_archives_for_pages.py "C:\Users\User\Downloads\Archives" "C:\Users\User\Downloads\Pages"')
    exit()

archives_path = sys.argv[1]
# assets_path = r"C:\Users\User\Downloads"

pages_path = sys.argv[2]


# out_path = r"C:\Users\User\Downloads"


def prompt_for_move(page_full_file_name, archive_full_file_name, auto_confirm_if_full_match=False):
    page_path, page_name, page_ext = split_file_name(page_full_file_name)
    arc_path, arc_name, arc_ext = split_file_name(archive_full_file_name)

    new_arc_file_name = os.path.join(page_path, page_name + arc_ext)
    if archive_full_file_name == new_arc_file_name:
        return True

    print("Page name    : " + page_name)
    print("Archive name : " + arc_name)

    if not (auto_confirm_if_full_match and page_name == arc_name):
        print('\nIs it match? ("y" if yes):')
        i = input()
        if i != "y":
            return False
    # move
    if os.path.isfile(new_arc_file_name):
        print("File already exist      : " + new_arc_file_name)
        print('Overwrite with new file : ' + archive_full_file_name)
        print('\n? ("y" if yes)')
        i = input()
        if i != "y":
            return False
        else:
            os.remove(new_arc_file_name)
    os.rename(
        archive_full_file_name,
        new_arc_file_name
    )
    return True


for path, subs, files in os.walk(pages_path):
    for page_file_name in files:
        page_full_file_name = os.path.join(path, page_file_name)

        if skip_if_page_already_has_archive:
            exist_archives = find_archives_for_page(page_full_file_name)
            if len(exist_archives) > 0:
                continue

        if not os.path.isfile(page_full_file_name):
            continue

        if not page_file_name.endswith(".html"):
            continue

        page_path, page_name, page_ext = split_file_name(page_full_file_name)

        archives = get_all_archives(archives_path)

        found = False
        # check for 100% same name
        for arc_full_file_name in archives:
            if not found:
                arc_path, arc_name, arc_ext = split_file_name(arc_full_file_name)
                if page_name.lower() == arc_name.lower():
                    print("-----------------------------\n")
                    print("Found full match:\n")
                    found = prompt_for_move(page_full_file_name, arc_full_file_name, auto_confirm_if_full_match)
        # check for same words
        if not found:
            page_words = page_name.split(" ")
            for arc_full_file_name in archives:
                if not found:
                    p, arc_name, ext = split_file_name(arc_full_file_name)
                    for word in page_words:
                        if len(word) < 4 or word.lower() in skip_words:
                            continue
                        if not found:
                            if word.lower() in arc_name.lower():
                                print("-----------------------------\n")
                                print(f'Found match by word "{word}":\n')
                                found = prompt_for_move(page_full_file_name, arc_full_file_name)
        if not found:
            print("Cant find asset archive for page: " + page_full_file_name + "\n")
            if move_page_to_folder_if_not_matched:
                make_dir(os.path.join(pages_path, not_matched_pages_subdir))
                os.rename(
                    page_full_file_name,
                    os.path.join(pages_path, not_matched_pages_subdir, page_name + page_ext)
                )
