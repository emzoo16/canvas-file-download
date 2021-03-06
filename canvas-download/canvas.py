from dotenv import load_dotenv
import colorama
import argparse
import editFiles
import initialize
import listFiles
import downloadFiles
import editIgnoreList

load_dotenv()
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