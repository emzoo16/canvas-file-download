from PyInquirer import prompt
import os
from colorama import Fore, Style
import fileUtils
import canvasUtils
from values import *


def initialize(args):
    course_string_list = []
    available_courses = canvasUtils.get_available_courses_for_user()

    for (course_name, course) in available_courses.items():
        course_string_list.append({"name": course_name})

    questions = [
        {
            "type": "checkbox",
            "qmark": "➤",
            "message": "Select courses to track (space to select)",
            "name": "courses",
            "choices": course_string_list,
            "validate": lambda answer: "You must choose at least one course"
            if len(answer) == 0
            else True,
        },
        {
            "type": "input",
            "qmark": "➤",
            "name": "directory",
            "message": "Specify a directory to keep your files",
            "validate": lambda userInput: userInput + " is not a valid directory"
            if not os.path.isdir(userInput)
            else True,
        },
    ]

    answers = prompt(questions, style=style)
    user_course_names = answers["courses"]
    user_course_ids = canvasUtils.get_course_ids_from_names(
        user_course_names, available_courses
    )

    user_directory = answers["directory"]

    fileUtils.make_directories_if_not_exist(user_course_names, user_directory)

    data = {"courses": user_course_ids, "directory": user_directory}

    fileUtils.save_to_config(data, config_path)

    print(
        Fore.GREEN
        + "config file successfully initialized at "
        + config_path
        + Style.RESET_ALL
    )
