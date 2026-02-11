from agent.tools.fs_write import write_file

a = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
b = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
c = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

print("\n".join([a,b,c]))
