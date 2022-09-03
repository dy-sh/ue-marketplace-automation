# Copyright: Dmitry Savosh (d.savosh@gmail.com)

import os
import sys
import json
import shutil
import requests
from bs4 import BeautifulSoup
import subprocess


class UnrealAssset:
    asset_name: str
    engine_ver: str
    web_page_url: str
    category: str
    path: str


def make_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(os.path.join(path))


def remove_if_exist(path: str):
    if os.path.isfile(os.path.join(path)):
        os.remove(os.path.join(path))
    if os.path.isdir(path) and os.path.exists(path):
        shutil.rmtree(path)


def escape_filename(file_name: str):
    invalid = '<>:"/\|?*'
    for char in invalid:
        file_name = file_name.replace(char, '')
    while file_name.endswith("."):  # archivers and other apps can throw exception if filename ends with "."
        file_name = file_name[:-1]
    return file_name


def get_asset_name_from_page_title(title: str):
    asset_name = title.rsplit(' in ', 1)[0]  # remove "in Code Plugins - Marketplace"
    asset_name = asset_name.replace("_", " ")
    asset_name = escape_filename(asset_name)

    category = title.rsplit(' in ', 1)[1]
    category = category.rsplit(' - UE Marketplace', 1)[0]
    category = category.lower()
    if category.startswith("-"):
        category = "-"
    if category == "code plugins":
        category = "plugins"
    if category == "2d assets":
        category = "2d"
    if category == "architectural visualization":
        category = "archvis"
    if category == "visual effects":
        category = "fx"
    if category == "sound effects":
        category = "soundfx"

    return asset_name, category


def read_title_from_html_file(full_page_file_name: str):
    with open(full_page_file_name, "r", encoding='utf-8') as f:
        data = f.read()
    soup = BeautifulSoup(data, "html.parser")
    title = soup.title.string
    return title


def find_archives_for_page(full_page_file_name: str):
    archives = []
    p, n, e = split_file_name(full_page_file_name)
    for ext in [".zip", ".7z", ".rar"]:
        arc_full_name = os.path.join(p, n + ext)
        if os.path.isfile(arc_full_name):
            archives.append(arc_full_name)
    return archives


def get_all_archives(in_path: str):
    archives = []
    for path, subs, files in os.walk(in_path):
        for file_name in files:
            full_file_name = os.path.join(path, file_name)
            if os.path.isfile(full_file_name):
                for ext in [".zip", ".7z", ".rar"]:
                    if file_name.endswith(ext):
                        archives.append(full_file_name)
    return archives


def split_file_name(full_file_name: str):
    path = os.path.dirname(full_file_name)
    base_name = os.path.basename(full_file_name)
    name = os.path.splitext(base_name)[0]
    ext = os.path.splitext(base_name)[1]
    return path, name, ext


def read_manifest(manifest_file_name: str) -> UnrealAssset:
    asset = UnrealAssset()
    asset.path = os.path.dirname(os.path.abspath(manifest_file_name))
    f = open(manifest_file_name)
    data = json.load(f)
    asset.asset_name = data['CustomFields']['Vault.TitleText']
    supported_engine = data['CustomFields']['CompatibleApps'].split(",")
    asset.engine_ver = supported_engine[-1]
    catalog_item_id = data['CustomFields']['CatalogItemId']
    asset.web_page_url = f"https://www.unrealengine.com/marketplace/en-US/item/" + catalog_item_id
    categories = data['CustomFields']['Categories'].split(",")
    asset.category = ""
    for cat in categories:
        if not cat == "assets":
            asset.category = cat.replace("assets/", "").replace("projects/", "")
    f.close()
    return asset


def get_asset_name_from_web_page(url: str):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    name = ""
    for title in soup.find_all('title'):
        name += title.get_text()
    name = name.rsplit(' in ', 1)[0]  # remove "in Code Plugins - Marketplace"
    return name


def read_plugin(plugin_file_name: str) -> UnrealAssset:
    asset = UnrealAssset()
    asset.path = os.path.dirname(os.path.abspath(plugin_file_name))

    f = open(plugin_file_name)
    data = json.load(f)
    f.close()

    try:
        asset.engine_ver = data['EngineVersion']
    except:
        asset.engine_ver = "UNKNOWN"

    asset.web_page_url = ""
    asset.asset_name = data['FriendlyName']
    launcher_url = data['MarketplaceURL']

    if launcher_url is not None and launcher_url != "":
        product_id = launcher_url.split('/content/')[-1]
        product_id = product_id.split('/product/')[-1]
        web_page_url = 'https://www.unrealengine.com/marketplace/en-US/product/' + product_id
        asset_name = get_asset_name_from_web_page(web_page_url)
        if asset_name != "":
            asset.asset_name = asset_name
            asset.web_page_url = web_page_url

    asset.category = "plugins"
    return asset


def archive_dir(read_path: str, archive_file_name: str):
    if not archive_file_name.endswith(".7z"):
        archive_file_name += ".7z"
    print(f'\nArchiving: "{archive_file_name}"')
    if os.path.isfile(archive_file_name):
        print(f'\nCant create archive, already exist: "{archive_file_name}"')
        terminate()
    read_path = os.path.abspath(read_path)
    command = fr'tools\7z.exe a -t7z -mx=7 "{archive_file_name}" "{read_path}\*"'
    res = os.system(command)
    if res != 0 or not os.path.isfile(archive_file_name):
        print("\nArchiving failed!")
        terminate()
    print("Archiving complete\n")


def extract(archive_file_name: str, write_path: str):
    print(f'\nExtracting: "{archive_file_name}"')
    arc_path, arc_name, arc_ext = split_file_name(archive_file_name)
    new_arc_dir = os.path.join(write_path, arc_name)
    if os.path.isdir(new_arc_dir):
        print(f'\nCant extract archive, directory already exist: "{new_arc_dir}"')
        terminate()
    make_dir(new_arc_dir)
    command = fr'tools\7z.exe x "{archive_file_name}" "-o{new_arc_dir}"'
    res = os.system(command)
    if res != 0:
        print("Extracting failed!\n")
        terminate()
    print("Extracting complete\n")


def save_webpage(url: str, write_path: str, asset_name: str):
    # save webpage
    web_page_file_name = os.path.join(write_path, asset_name + ".html")
    print("\nDownloading asset webpage: " + web_page_file_name)
    remove_if_exist(web_page_file_name)
    command = fr'tools\monolith.exe {url} -o "{web_page_file_name}" -a -e -j -v -F'
    res = os.system(command)
    if res != 0 or not os.path.isfile(web_page_file_name):
        print("\nDownloading failed")
        terminate()
    print("Downloading complete\n")


def terminate():
    print('\a')  # beep
    exit(1)
