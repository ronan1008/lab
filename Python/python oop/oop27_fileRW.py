file_read = open("README.txt",encoding="utf8")
file_write = open("README_copy.txt",'w')

text = file_read.read()
file_write.write(text)


file_read.close()
file_write.close()