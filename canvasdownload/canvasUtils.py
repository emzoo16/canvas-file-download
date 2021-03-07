from canvasdownload import fileUtils
import re
import os
from pprint import pprint
from canvasdownload import values
from colorama import Style
from canvasapi import Canvas


def get_available_courses_for_user(selected_only=False):
    canvas = Canvas(os.environ.get("API_URL"), os.environ.get("API_KEY"))

    if selected_only == True:
        user_config = fileUtils.load_config(values.config_path)

    course_list = dict()
    courses = canvas.get_courses(enrollment_state="active", enrollment_type="student")

    for course in courses:
        if selected_only == True:
            if course.id in user_config["courses"]:
                course_list[course.course_code.replace(" ", "")] = course
        else:
            course_list[course.course_code.replace(" ", "")] = course
    return course_list


def get_course_ids_from_names(name_list, course_dict):
    course_ids = []
    for course_name in name_list:
        for (course_key, course) in course_dict.items():
            if course_name == course_key:
                course_ids.append(course.id)

    return course_ids


def filter_files(file_dict, regex_ignore_list):
    ignore_dict = dict()
    available_for_download_dict = dict()

    for (file_name, file) in file_dict.items():
        ignored = False

        for regex_to_ignore in regex_ignore_list:
            if re.search(regex_to_ignore, file_name):
                ignored = True

        if ignored:
            ignore_dict[file_name] = file
        else:
            available_for_download_dict[file_name] = file

    return ignore_dict, available_for_download_dict


def get_status_for_files(files_from_canvas, files_local, ignore_list):
    new_files = dict()
    already_downloaded = dict()

    for canvas_file in files_from_canvas:
        file_already_downloaded = False

        for local_file in files_local:
            if str(canvas_file) == local_file:
                file_already_downloaded = True

        if file_already_downloaded:
            already_downloaded[str(canvas_file)] = canvas_file
            file_already_downloaded = False
        else:
            new_files[str(canvas_file)] = canvas_file

    ignored_files, downloadable_files = filter_files(new_files, ignore_list)

    return downloadable_files, already_downloaded, ignored_files


def print_list(list, style=None, decorator=" "):
    for entry in list:
        if style == None:
            print(str(entry))
        else:
            print(style + decorator + " " + str(entry) + Style.RESET_ALL)