from functions.run_python_file import run_python_file

a = run_python_file("calculator", "main.py")
b = run_python_file("calculator", "main.py", ["3 + 5"]) 
c = run_python_file("calculator", "tests.py") 
d = run_python_file("calculator", "../main.py") 
e = run_python_file("calculator", "nonexistent.py") 
f = run_python_file("calculator", "lorem.txt")

print("\n".join([a,b,c,d,e,f]))