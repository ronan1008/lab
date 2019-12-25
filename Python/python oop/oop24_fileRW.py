file = open("README.txt",encoding="utf8")

text = file.read()
print(text)

print("_"*30)
#指針移動到末尾，所以讀取不到
text = file.read()
print(text)

file.close()