from agent.tools.fs_list import fs_list
from .test_helper import show

for expect, args in [
    (None, ("sandbox", ".")),
    (None, ("sandbox", "calculator/pkg")),
    ("OutsideWorkingDirectory", ("sandbox", "/bin")),
    ("OutsideWorkingDirectory", ("sandbox", "../")),
]:
    show(fs_list(*args), expect)