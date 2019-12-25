class Tool():
    count = 0 

    def __init__(self, name):
        self.name = name 

        Tool.count += 1
    


tool = Tool("斧頭")
tool2 = Tool("鎚子")

print(Tool.count)

print("工具對象總數 %d" %tool.count)