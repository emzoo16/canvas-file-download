from canvasdownload import values
from colorama import Style, Fore
from PyInquirer import Separator, prompt
from canvasdownload import canvasUtils
from canvasdownload import fileUtils
import os


def edit_ignore_list(args):
    course_string_list = []
    user_config = fileUtils.load_config(values.config_path)

    available_courses = canvasUtils.get_available_courses_for_user(selected_only=True)
    for (course_name, course) in available_courses.items():
        course_string_list.append({"name": course_name})

    questions = [
        {
            "type": "list",
            "qmark": "➤",
            "name": "course",
            "message": "Which course to ignore/allow files for?",
            "choices": course_string_list,
            "validate": lambda answer: "You must choose at least one course"
            if len(answer) == 0
            else True,
        }
    ]

    answer = prompt(questions, style=values.style)
    selected_course = available_courses[answer["course"]]
    download_directory = user_config["directory"] + "/" + answer["course"]

    files_in_directory = os.listdir(download_directory)

    files_from_canvas = selected_course.get_files()

    ignore_list = fileUtils.load_ignorelist(download_directory + "/.ignore-list")
    not_downloaded, already_downloaded, ignored = canvasUtils.get_status_for_files(
        files_from_canvas, files_in_directory, ignore_list
    )

    file_string_list = []

    for (file_name, file) in not_downloaded.items():
        file_string_list.append({"name": file_name})

    for (file_name, file) in ignored.items():
        file_string_list.append({"name": file_name, "checked": True})

    if len(file_string_list) > 0:
        print(
            Style.BRIGHT
            + "\nChoose files to ignore/allow "
            + selected_course.course_code
            + Style.RESET_ALL
        )

        questions = [
            {
                "type": "checkbox",
                "qmark": "➤",
                "name": "files",
                "message": "Check the files you want to ignore ",
                "choices": file_string_list,
            }
        ]

        answers = prompt(questions, style=values.style)
        selected_files = answers["files"]

        if len(selected_files) > 0:
            with open(
                download_directory + "/" + values.ignore_file_name, "w"
            ) as ignore_list_file:
                for file in selected_files:
                    ignore_list_file.write(file + "\n")
            print("\nThe current ignored files are")
            canvasUtils.print_list(selected_files, Style.DIM, "+")
            print("\n")
        else:
            open(download_directory + "/" + values.ignore_file_name, "w").close()
            print(Fore.GREEN + "\nIgnore list is currently empty\n" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "\nNo new files to ignore\n" + Style.RESET_ALL)