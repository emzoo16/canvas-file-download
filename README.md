# canvas-file-download

A command line tool to download files from canvas. Written using in Python using the Argparse and CanvasApi libraries.

## Usage:

```
usage: canvas [-h]
              {init,edit-courses,download-files,list-files,edit-ignorelist}
              ...

positional arguments:
  {init,edit-courses,download-files,list-files,edit-ignorelist}
                        subcommands
    init                initialize the tool
    edit-courses        edit current course list
    download-files      download files from canvas
    list-files          view differences between local files and files on
                        canvas
    edit-ignorelist     Add and remove files from the ignorelist

optional arguments:
  -h, --help            show this help message and exit
  ```
#### init 
Initialises tool by allowing user to select which courses they want to track files for. Creates directories to store files for the selected courses. Selected courses are added to a config file stored under the user's home directory.

#### edit-courses
Edit the current courses being tracked. Creates/deletes course directories depending on the user's selections.

#### download-files
Download files for a particular course. User selects from files on Canvas that have not been downloaded into the local directory.

#### list-files
View differences in files between local directory and the files on Canvas. Showing any new files on Canvas, already downloaded files, as well as files ignored for download.

#### edit-ignorelist
Add/remove files from the ignorelist found within each local course directory. Any files on the ignorelist will not be shown for download.

## Installation
From the root directory run:
```
pip install .
```
