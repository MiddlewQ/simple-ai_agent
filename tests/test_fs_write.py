from agent.tools.fs_write import fs_write
from .test_helper import show

for expect, args in [
    (None, ("sandbox", "lorem.txt", "wait, this isn't lorem ipsum")),
    (None, ("sandbox", "more_lorem/morelorem.txt", "lorem ipsum dolor sit amet")),
    ("PathOutsideWorkingDirectory", ("calculator", "/tmp/temp.txt", "this should not be allowed")),  # adjust if your type differs
]:
    show(fs_write(*args), expect)
