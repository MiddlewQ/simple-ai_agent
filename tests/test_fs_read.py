from agent.tools.fs_read import fs_read
from .test_helper import show

for expect, args in [
    (None, ("sandbox", "calculator/main.py")),
    (None, ("sandbox", "calculator/pkg/calculator.py")),
    ("PathOutsideWorkingDirectory", ("sandbox", "/bin/cat")),
    ("NotAFile", ("sandbox", "pkg/does_not_exist")),  # or whatever you return
]:
    show(fs_read(*args), expect)
