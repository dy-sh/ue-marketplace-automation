# Copyright: Dmitry Savosh (d.savosh@gmail.com)

from utils.utils import *

# settings :
delete_archived_asset = True

if len(sys.argv) != 3:
    print("Please, provide input and output path as argument!")
    print('Example:')
    print(r'python archive.py "C:\ProgramData\Epic\EpicGamesLauncher\VaultCache" "D:\Unreal Assets"')
    exit()

assets_path = sys.argv[1]
# assets_path = r"C:\ProgramData\Epic\EpicGamesLauncher\VaultCache"

out_path = sys.argv[2]
# out_path = os.path.abspath("H:\GAMEDEV ASSETS")

path_list = os.listdir(assets_path)
for asset_folder_name in path_list:
    old_asset_path = os.path.join(assets_path, asset_folder_name)
    if not os.path.isdir(old_asset_path):
        continue

    # if vault_cache_asset (manifest file exist)
    manifest_file_name = os.path.join(old_asset_path, 'manifest')
    if os.path.isfile(manifest_file_name):
        asset = read_manifest(manifest_file_name)
    else:
        # if engine plugin (.uplugin file exist)
        asset_files_list = os.listdir(old_asset_path)
        plugin_file_name = None
        for file_name in asset_files_list:
            if file_name.endswith(".uplugin"):
                plugin_file_name = os.path.join(old_asset_path, file_name)
                break
        if plugin_file_name:
            asset = read_plugin(plugin_file_name)
        else:
            # unrecognized asset
            continue

    asset.asset_name = escape_filename(asset.asset_name)

    print("Asset path: " + asset.path)
    print("Asset name: " + asset.asset_name)
    print("Asset url : " + asset.web_page_url)

    if asset.web_page_url == "":
        print('\a')
        print("Please, enter url for this asset (or hit enter to skip downloading web page):")
        asset.web_page_url = input()

    # create new asset folder
    make_dir(out_path)
    category_path = os.path.join(out_path, asset.category)
    make_dir(category_path)
    engine_ver_path = os.path.join(category_path, asset.engine_ver)
    make_dir(engine_ver_path)
    new_asset_path = engine_ver_path

    # rename asset folder
    if asset.category != "plugins":
        temp_asset_path = os.path.join(assets_path, asset.asset_name)
        if old_asset_path != temp_asset_path:
            remove_if_exist(temp_asset_path)
            os.rename(old_asset_path, temp_asset_path)
        asset.path = temp_asset_path

    # copy manifest
    if asset.category != "plugins":
        manifests_path = os.path.join(out_path, "! manifests")
        make_dir(manifests_path)
        manifest_path = os.path.join(manifests_path, asset.category, asset.asset_name)
        make_dir(manifest_path)
        remove_if_exist(os.path.join(manifest_path, "manifest"))
        shutil.copyfile(
            os.path.join(asset.path, "manifest"),
            os.path.join(manifest_path, "manifest")
        )

    # archive
    new_archive_name = os.path.join(new_asset_path, asset.asset_name + ".7z")
    archive_dir(asset.path, new_archive_name)

    # save webpage
    if asset.web_page_url != "":
        save_webpage(asset.web_page_url, new_asset_path, asset.asset_name)

    # delete old asset folder
    if delete_archived_asset:
        remove_if_exist(asset.path)

    print("Downloading complete")
    print("----------------------------------------")
