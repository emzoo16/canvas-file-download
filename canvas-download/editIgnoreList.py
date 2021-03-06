from values import *
from colorama import Style, Fore
from PyInquirer import Separator
import canvasUtils
import fileUtils
import os


def edit_ignore_list(args):
    course_string_list = []
    user_config = fileUtils.load_config(config_path)

    available_courses = canvasUtils.get_available_courses_for_user(selected_only=True)
    for (course_name, course) in available_courses.items():
        course_string_list.append({"name": course_name})

    questions = [
        {
            "type": "list",
            "qmark": "➤",
            "name": "course",
            "message": "Which course to download files for?",
            "choices": course_string_list,
            "validate": lambda answer: "You must choose at least one course"
            if len(answer) == 0
            else True,
        }
    ]

    answer = prompt(questions, style=style)
    selected_course = available_courses[answer["course"]]
    download_directory = user_config["directory"] + "/" + answer["course"]

    print(
        Style.BRIGHT
        + "\nChoose files to ignore/allow "
        + selected_course.course_code
        + Style.RESET_ALL
    )

    files_in_directory = os.listdir(download_directory)

    files_from_canvas = selected_course.get_files()

    ignore_list = fileUtils.load_ignorelist(download_directory + "/.ignore-list")
    not_downloaded, already_downloaded, ignored = canvasUtils.get_status_for_files(
        files_from_canvas, files_in_directory, ignore_list
    )

    file_string_list = []

    for (file_name, file) in not_downloaded.items():
        file_string_list.append({"name": file_name, "checked": True})

    questions = [
        {
            "type": "checkbox",
            "qmark": "➤",
            "name": "files",
            "message": "Check the files you want to ignore ",
            "choices": file_string_list,
        }
    ]

    answers = prompt(questions, style=style)
    selected_files = answers["files"]

    with open(download_directory + "/" + ignore_file_name, "a+") as ignore_list_file:
        for file in selected_files:
            ignore_list_file.write(file + "\n")

    print("\nThe following files added to ignore list")
    fileUtils.print_list(selected_files, Style.DIM, "+")
