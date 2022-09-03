# Unreal Engine Marketplace Automation

This is a set of scripts for automating the Epic Games Launcher and downloading/archiving Unreal Engine Marketplace products (assets).

These scripts can be useful if you have a huge amount of assets that you would like to download and save to disk.
Along with the assets, web pages describing the assets will be downloaded. 
Some scripts will help you get organized if you already have an asset library and would like to catalog it.

The scripts use the following tools, which you can download and put in the `\tools` folder:
- [7-Zip](https://www.7-zip.org)
- [Y2Z / monolith](https://github.com/Y2Z/monolith)


### download.py

This script downloads assets from the Epic Games Launcher.  
  
How to use:  
  
Create project with name `Temp`. Assets will be added to this project when downloading.  
You can override the project name in the `add_to_project\temp_project_name.png` file.  
Take a screenshot of the title in the project selection window and save it in this file. 
The project should be visible in the list if the `Show all projects` checkbox is selected
in the `Select the Project to Add the Asset to` window  
(use the project name with the letter `A` if you have many projects.  

  
- Open the Epic Games Launcher  
- Switch it to English (if another language is used)  
- Go to the `Unreal Engine` tab  
- Go To the `Library` tab  
- Select asset categories or use the search filter in the `Vault` section
- If the `Install to Engine`/`Add to Project`/`Create Project` buttons appear on the screen,  
run the script (`python download.py`) and just wait  

The script will control the cursor and download one asset after another.  
It will automatically recognize the asset type and perform all the necessary actions.
If something goes wrong to stop the script, press `Win + M` (or any other hotkey to hide the launcher from the screen).
  
Assets will be downloaded to the `C:\ProgramData\Epic\EpicGamesLauncher\VaultCache folder` folder.  
Engine plugins will be downloaded to the `C:\Program Files\Epic Games\UE_5.0\Engine\Plugins\Marketplace` folder  
and their manifests to the `C:\Program Files\Epic Games\[EngineVersion]\.egstore` folder.  
Clear these folders if you want to delete the entire downloaded cache.  
You should save only the oldest (and largest) `.manifest` and same named `.mancpn` file  
in the `\.egstore` folder (this is the engine's own manifest).  
  

### archive.py

This script will get all downloaded assets from the Epic Games Launcher cache folder  
and archive them into `.7z` archives.  
Then it will download `.html` page from the Marketplace web-site and save it next to the archive.  
It takes two arguments: an input and an output folder.  

Example:

`python archive.py "C:\ProgramData\Epic\EpicGamesLauncher\VaultCache" "C:\Users\User\Downloads\Assets"`


### repack.py  
  
This script will find all the `.rar`/`.zip` archives at the specified path  
and repack them to `.7z` with the maximum compression method.   
  
Example:

`python repack.py "D:\Unreal Assets"`  


### find_archives_for_pages.py  
  
This script will try to match the saved `.html` pages with the downloaded `.zip`/`.rar`/`.7z` archives.  
It will ask you which file to take if the names don't match 100%.  
Then it will rename the archive according to the page name and move it to the page folder.  
  
Example:

`python find_archives_for_pages.py "C:\Users\User\Downloads\Archives" "C:\Users\User\Downloads\Pages"`
  

### remove_duplicates.py  
  
This script will help to remove duplicates from downloaded assets.  
It will find all the saved `.html` pages and compare their names.  
Then it will ask you which file to keep.  
It will delete `.html` and `.7z` files of the duplicated asset.  
  
Example:

`python remove_duplicates.py "D:\Unreal Assets"`  

You can specify multiple folders:   

`python remove_duplicates.py "D:\Folder1" "D:\Folder12" "D:\Folder13"`  


### sort_pages.py  
  
This script will sort the saved `.html` pages and place them by asset categories.  
  
Example:

`python sort_pages.py "C:\Users\User\Downloads" "D:\Unreal Assets"`  


### rename.py  
  
This script will find all saved `.html` pages, will read their contents and rename the pages   
and the archives of the same name in accordance with the name of the asset.  
  
Example:

`python rename.py "D:\Unreal Assets"`  
  