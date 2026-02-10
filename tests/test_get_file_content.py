from functions.get_file_content import get_file_content

a = get_file_content("calculator", "main.py")
b = get_file_content("calculator", "pkg/calculator.py")
c = get_file_content("calculator", "/bin/cat")
d = get_file_content("calculator", "pkg/does_not_exist")

print("\n".join([a,b,c,d]))