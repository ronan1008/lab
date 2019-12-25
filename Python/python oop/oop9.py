class Tool():

    count = 0 

    @classmethod
    def show_tool_count(cls):

        print("工具對象的數量 %d" % cls.count)

    def __init__(self, name):
        self.name = name 

        Tool.count += 1
    

tool1 = Tool("AXes")
tool2 = Tool("Toys")

Tool.show_tool_count()