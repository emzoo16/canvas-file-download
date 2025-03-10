from dotenv import load_dotenv
import colorama
import argparse
from canvasdownload import fileUtils
from canvasdownload import initialize
from canvasdownload import listFiles
from canvasdownload import editFiles
from canvasdownload import downloadFiles
from canvasdownload import editIgnoreList
from canvasdownload import values


def main():
    load_dotenv(values.env_path)
    colorama.init()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="subcommands")

    parser_initialise = subparsers.add_parser("init", help="initialize the tool")
    parser_initialise.set_defaults(func=initialize.initialize)

    parser_course = subparsers.add_parser("edit-courses", help="list available courses")
    parser_course.set_defaults(func=editFiles.edit)

    parser_course = subparsers.add_parser(
        "download-files", help="download files from canvas"
    )
    parser_course.set_defaults(func=downloadFiles.download_files)

    parser_diff = subparsers.add_parser(
        "list-files", help="view differences between local files and files on canvas"
    )
    parser_diff.set_defaults(func=listFiles.list_files)

    parser_diff = subparsers.add_parser(
        "edit-ignorelist", help="Add and remove files from the ignorelist"
    )
    parser_diff.set_defaults(func=editIgnoreList.edit_ignore_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled\n")
