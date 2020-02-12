
# Comprehension 生成式
orig_list = [2,4,6,8,10]
new_list = [ x * x for x in orig_list ]
new_list_gre_than_4 = [ x * x  for x in orig_list if x > 4 ]
print(new_list)
print(new_list_gre_than_4)

dic_list = {key: item*item  for key,item in enumerate(orig_list)}
print(dic_list)

print("--------------------------")



print("--------------------------")

#enumerate
toys_list = ['car','robot','army','ball','box','doll','train','cake']

for n , item in enumerate(toys_list):
	if n % 2 == 0:
		continue
	print(n,item)

print("--------------------------")

#list slice
toys_number = len(toys_list)
toy_slice_head = toys_list[ :toys_number//2]
toy_slice_tail = toys_list[toys_number//2 : ]

print(toy_slice_head)
print(toy_slice_tail)

print("--------------------------")

# sort and sortedb
toy_slice_head.sort()
sort_toy_tail = sorted(toy_slice_tail)

print(toy_slice_head)
print(sort_toy_tail)

print("--------------------------")


#custom sort
furniture = ['chair','curtain','desk','kitchen table','window']

def compare_num_of_chars(string1):
	return len(string1)

furniture.sort()
print(furniture)
furniture.sort(key = compare_num_of_chars)
print(furniture)
print("--------------------------")
#custom sort
num_list = [[1,2,3],[2,1,3],[4,0,1]]

def compare_list_by_second(array1):
	return array1[1]

num_list.sort(key = compare_list_by_second)
print(num_list)

print("--------------------------")

# + and * and extend method in list 
x = [1,3]
y = [2,3]
z = [None] * 3
x.extend(y)
total = x + z
print(z)
print(x)
print(total)
print("--------------------------")
original  = [[0],1]
shallow = original[:]
import copy
deep = copy.deepcopy(original)
original[0][0] = 9
print(original)
print(deep)

print("--------------------------")

one, two, three, four = 1, 2, 3, 4
print(one,two,three,four) 

print("--------------------------")

x, y, *_ = ("Apple","Book","Other1","Other2")

print(x,y)

print("--------------------------")

x = "hello"
x =list(x)
print(x)

print("--------------------------")
x = "www.python.org.tw"
y= x.strip(".wtorg")
z= x.strip("tworg")
z=list(z)
del z[0],z[-1]
z= ''.join(z)
print(y,z)
print("--------------------------")
listStr = ["123","str"]
for x in listStr:
	print( x.isdigit() )
	print( x.isalpha() )
	print( x.islower() )
	print( x.isupper() )
	print('----boundry----')

print("--------------------------")
x = "I Love You or You Love me"	
print(x.find("Love"))
print(x.find("I"))
print(x.rfind("Love"))
print(x.replace("Love","Hate"))

print("--------------------------")

n=101
result =  "success"  if n > 100 else "failed"
print(result)

print("---end---")
