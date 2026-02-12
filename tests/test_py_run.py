from agent.tools.py_run import py_run
from .test_helper import show


for expect, args in [
    (None, ("sandbox", "calculator/main.py")),
    (None, ("sandbox", "calculator/main.py", ["3 + 5"])),
    (None, ("sandbox", "calculator/tests.py")),
    ("PathOutsideWorkingDirectory", ("sandbox", "../main.py")),
    ("NotAFile", ("sandbox", "nonexistent.py")),
    ("NotPythonFile", ("sandbox", "lorem.txt")),
]:
    show(py_run(*args), expect)
