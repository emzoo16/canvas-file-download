from canvasdownload import canvasUtils
from canvasdownload import fileUtils
import os
from colorama import Style, Fore
from canvasdownload import values
from PyInquirer import prompt


def list_files(args):
    course_string_list = []
    user_config = fileUtils.load_config(values.config_path)

    available_courses = canvasUtils.get_available_courses_for_user(selected_only=True)

    for (course_name, course) in available_courses.items():
        course_string_list.append({"name": course_name})

    if len(user_config["courses"]) > 1:
        course_string_list.append({"name": "View All"})

    questions = [
        {
            "type": "list",
            "qmark": "➤",
            "name": "courses",
            "message": "Which course to view files for?",
            "choices": course_string_list,
            "validate": lambda answer: "You must choose at least one course"
            if len(answer) == 0
            else True,
        }
    ]

    answer = prompt(questions, style=values.style)
    selected_courses = []

    if answer["courses"] == "View All":
        selected_courses = list(available_courses.values())
    else:
        selected_courses = [available_courses[answer["courses"]]]

    for course in selected_courses:
        directory = user_config["directory"] + "/" + course.course_code.replace(" ", "")

        print(Style.BRIGHT + "\n" + course.course_code + Style.RESET_ALL)

        files_in_directory = os.listdir(directory)
        files_from_canvas = course.get_files()
        ignore_list = fileUtils.load_ignorelist(directory + "/.ignore-list")

        not_downloaded, already_downloaded, ignored = canvasUtils.get_status_for_files(
            files_from_canvas, files_in_directory, ignore_list
        )

        if len(not_downloaded) > 0:
            print("\nFiles not downloaded ")
            canvasUtils.print_list(list(not_downloaded.keys()), Fore.GREEN, "+")
        else:
            print(
                Fore.GREEN
                + "\nNo new files to download, all up to date!"
                + Style.RESET_ALL
            )

        if len(already_downloaded) > 0:
            print("\nAlready downloaded files ")
            canvasUtils.print_list(list(already_downloaded.keys()), Fore.BLUE, " ")

        if len(ignored) > 0:
            print("\nIgnored files ")
            canvasUtils.print_list(list(ignored.keys()), Style.DIM, " ")

        print(
            "\n"
            + str((len(list(files_from_canvas))))
            + " files total, "
            + str(len(not_downloaded))
            + " files not yet downloaded, "
            + str(len(ignored))
            + " files ignored"
        )
        print("----------------------------------------------------------")

    print("\n")