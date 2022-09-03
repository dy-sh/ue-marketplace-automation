# Unreal Engine Marketplace Automation

This is a set of scripts for automating Epic Games Launcher and downloading/archiving Unreal Engine Marketplace products (assets).

These scripts can be useful if you have a huge amount of assets that you would like to download and save to disk.  
Along with the assets, web pages describing the asset will be downloaded.  
Some scripts will help you get organized if you already have an asset library and would like to catalog it.

The scripts use the following tools, which you can download and put in the `\tools` folder:
- [7-Zip](https://www.7-zip.org)
- [Y2Z / monolith](https://github.com/Y2Z/monolith)


### download.py

This script downloads assets from the Epic Games Launcher.  
  
How to use:  
  
Create project with name `Temp`. It will be used for downloading assets. Assets will be added to this project.  
You can override project name in `add_to_project\temp_project_name.png` file.  
Make screenshot of title on project selection window.  
This project must be visible in the list, when `Show all projects` checkbox selected  
in the `Select the Project to Add the Asset to` window.  
Use name staring from `A` if you have many projects.  
  
- Open Epic Launcher  
- Switch it to English language (if not switched yet)  
- Go to `Unreal Engine` tab  
- Go To `Library` tab  
- Select categories, or use search filter  
- If assets `Install to Engine`/`Add to Project`/`Create Project` buttons on the screen,  
run the script (`python download.py`) and just wait  
- Is something goes wrong, to stop the script, press `Win+M` (or any other hotkey to hide launcher from the screen)  
  
Assets will be downloaded to `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache folder`.  
All engine plugins will be downloaded to `C:\Program Files\Epic Games\UE_5.0\Engine\Plugins\Marketplace`  
and manifests in `C:\Program Files\Epic Games\UE_5.0\.egstore`.  
Clean these folders if you want to delete all downloaded cache.  
You must save only the oldest (and largest) `.manifest` and same name `.mancpn`  
in the `\.egstore` folder (this is the engine's own manifest).  
  

### archive.py

This script will get all the downloaded assets from Epic Games Launcher cache folder
and archive them to `.7z` archives.  
Next, it will download `.html` from the Marketplace web-site and save it near the archive.  
It takes two arguments: input and output folder.  

Example:

`python archive.py "C:\ProgramData\Epic\EpicGamesLauncher\VaultCache" "C:\Users\User\Downloads\Assets"`


### repack.py  
  
This script will find all `.rar`/`.zip` archives in specified path  
and repack them to `.7z` with maximum compression method.   
  
Example:

`python repack.py "D:\Unreal Assets"`  


### find_archives_for_pages.py  
  
This script will try to match saved `.html` pages with downloaded `.zip`/`.rar`/`.7z` archives.  
It will ask you if the names don't match 100%.  
Next, it will rename archive as page name and move it to page folder.  
  
Example:

`python find_archives_for_pages.py "C:\Users\User\Downloads\Archives" "C:\Users\User\Downloads\Pages"`
  

### remove_duplicates.py  
  
This script will help to remove duplicates from downloaded assets.  
It will find all saved `.html` pages and compare it names.  
Next, it will ask you which file to keep.  
It will remove `.html` and `.7z` file of duplicated asset.  
  
Example:

`python remove_duplicates.py "D:\Unreal Assets"`  

You can specify multiple folders:   

`python remove_duplicates.py "D:\Folder1" "D:\Folder12" "D:\Folder13"`  


### sort_pages.py  
  
This script will sort saved `.html` from Unreal Engine Marketplace and place it by asset category.  
  
Example:

`python sort_pages.py "C:\Users\User\Downloads" "D:\Unreal Assets"`  


### rename.py  
  
This script will find all saved `.html` pages and read their titles.  
Next, it will rename `.html` pages and archives with same name to correct asset name from page title.  
  
Example:

`python rename.py "D:\Unreal Assets"`  
  