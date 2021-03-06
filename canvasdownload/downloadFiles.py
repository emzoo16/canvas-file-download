from canvasdownload import values
from colorama import Style, Fore
from PyInquirer import Separator, prompt
from canvasdownload import canvasUtils
from canvasdownload import fileUtils
import os


def download_files(args):
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
            "message": "Which course to download files for?",
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

    if len(not_downloaded.items()) > 0:
        print(
            Style.BRIGHT
            + "\nNew files available for download "
            + selected_course.course_code
            + Style.RESET_ALL
        )
        for (file_name, file) in not_downloaded.items():
            file_string_list.append({"name": file_name, "checked": True})

        file_string_list.append(Separator("----------------"))

        for (file_name, file) in ignored.items():
            file_string_list.append(
                {
                    "name": file_name,
                    "disabled": "ignored from ignore list",
                }
            )

        questions = [
            {
                "type": "checkbox",
                "qmark": "➤",
                "name": "files",
                "message": "Check the files you want to download ",
                "choices": file_string_list,
            }
        ]

        answers = prompt(questions, style=values.style)
        selected_files = answers["files"]

        for file in selected_files:
            print(Style.DIM + "Downloading " + file + "..." + Style.RESET_ALL)
            selected_file_object = not_downloaded[file]
            selected_file_object.download(download_directory + "/" + file)

        print(Style.DIM + "\nDownload finished" + Style.RESET_ALL)
    else:
        print(
            Fore.GREEN
            + "No files to download for "
            + selected_course.course_code
            + ". All up to date"
            + Style.RESET_ALL
        )
