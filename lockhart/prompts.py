import ast
from collections import namedtuple
import textwrap

import openai


def write_docstring(code):

    parsed = parse_function(code)
    prompt = f'''
# Python 3.10

{code}

# Please write a high quality python docstring conforming to the google code style for docstrings for the above code.

The name of the function is: ```{parsed.name}```.

It has the following signature {parsed.args}.

Do not return the full function.
Only return the docstring.
Include an example if you can.
It should start with a short summary written in an imperative mood.
followed by a newline.
followed by a short description.
followed by another newline.
then followed by any of the following sections sections if they apply to this function (Args: , Returns: , Raises: , Yields: , Note: , Example: )
"""
'''
    # prompt = f"Please write a python docstring conforming to the google code style for docstrings.\n\n{code}\n"
    # prompt = f'# Python 3.10\n{code}\n\n# An elaborate, high quality docstring for the above function:\n"""'

    print(f"generating a response for \n\n{prompt}")
    print("-" * 80)
    print()

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", '"""'],
    )
    text = response["choices"][0]["text"]
    text = textwrap.indent(f'"""\n{text}\n"""', "    ")
    print(text)
    return text


def write_test(code):

    parsed = parse_function(code)
    prompt = f'Please write a test from the following function using pytest: ```{parsed.name}``` with the following signature {parsed.args}, and the following source code {code}, do not return the full function, only return the docstring surrounded by `"""`, indent the docstring to match the function indentation level'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
    )
    return response["choices"][0]["text"]


def refactor_code(code, prompt):

    prompt = f"refactor the following code to {prompt}\n\n{code}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
    )
    return response["choices"][0]["text"]


def write_blog(code):
    """

    Write a blog post about the given code.

    This function takes in a code snippet as an argument and generates a blog post about it using OpenAI's Completion API.

    Args:
        code (str): The code snippet to generate a blog post about.

    Returns:
        str: A blog post about the given code snippet.

    Example:
        response = write_blog("def hello_world():\n    print('Hello World!')")
        print(response)

    """

    prompt = f"Write a blog post about the following code in Markdown. \n\n```{code}```"

    print(f"generating a response for {prompt[:200]}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
    )
    return response["choices"][0]["text"]


Function = namedtuple("Function", "name, args")


def parse_function(code: str) -> Function:
    tree = ast.parse(code)
    args = []
    name = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            name = node.name
            args = [
                f"{arg.arg}:"  # {arg.annotation.value}"
                if arg.annotation
                else f"{arg.arg}: None"
                for arg in node.args.args
            ]
    if name is None:
        raise ValueError("input is not a FunctionDef")
    return Function(name, args)


# code_str = """def example_function(arg1:int,arg2:str)->int:
#     pass"""
# name, args, return_annotation = extract_function_signature(code_str)
# print(name)
# print(args)
# print(return_annotation)


def parse_code():
    tree = ast.parse(my_code)
    args = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            args = [
                f"{arg.arg}: {arg.annotation.value}"
                if arg.annotation
                else f"{arg.arg}: None"
                for arg in node.args.args
            ]
    return name, args
