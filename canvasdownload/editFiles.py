from canvasdownload import fileUtils
from canvasdownload import canvasUtils
from canvasapi import Canvas
from PyInquirer import prompt, style_from_dict, Token
from canvasdownload import values


def edit(args):
    user_config = fileUtils.load_config(values.config_path)
    course_string_list = []

    available_courses = canvasUtils.get_available_courses_for_user()
    selected_course_ids = user_config["courses"]

    for (course_name, course) in available_courses.items():
        if course.id in selected_course_ids:
            course_string_list.append({"name": course_name, "checked": True})
        else:
            course_string_list.append({"name": course_name})

    questions = [
        {
            "type": "checkbox",
            "qmark": "➤",
            "message": "Edit your current course selections",
            "name": "courses",
            "choices": course_string_list,
            "validate": lambda answer: "You must choose at least one course"
            if len(answer) == 0
            else True,
        }
    ]

    answers = prompt(questions, style=values.style)
    course_names = answers["courses"]
    user_course_ids = canvasUtils.get_course_ids_from_names(
        course_names, available_courses
    )

    fileUtils.make_directories_if_not_exist(course_names, user_config["directory"])

    user_config["courses"] = user_course_ids
    fileUtils.save_to_config(user_config, values.config_path)

    print("Courses updated. Current courses are:")
    canvasUtils.print_list(course_names)