from PyInquirer import prompt, style_from_dict, Token
import os

style = style_from_dict(
    {
        Token.QuestionMark: "#00FFFF bold",
        Token.Selected: "#90EE90",  # default
        Token.Pointer: "#7B68EE bold",
        Token.Instruction: "",  # default
        Token.Answer: "#32CD32 bold",
        Token.Question: "",
    }
)

config_path = os.path.expanduser("~") + "/canvas-config.yaml"

ignore_file_name = ".ignore-list"