class HouseItem:
    def __init__(self, name, area):
        self.name = name 
        self.area = area
    def __str__(self):
        return "[%s] 占地 %.2f" % (self.name, self.area)

class House:

    def __init__(self, house_type, area):
        self.house_type = house_type
        self.area = area

        self.free_area = area
        self.item_list = []

    def __str__(self):
        return ("戶型: %s\n總面積: %.2f[剩餘面積: %.2f]\n家具: %s" 
            %(self.house_type, self.area, 
            self.free_area, self.item_list))

    def add_item(self, item):
        print("要添加 %s" % item)
        #1.判斷家具面積
        if item.area > self.free_area:
            print("%s 的面積太大，無法添加" % item.name)
            
            return 
        #2.將家具的名稱添加到列表中
        self.item_list.append(item.name)

        #3.計算剩餘面積
        self.free_area -= item.area



bed = HouseItem("席夢思",40)
chest =HouseItem("衣櫃",2)
table = HouseItem("餐桌",20)

my_home = House("兩室一廳",60)
my_home.add_item(bed)
my_home.add_item(chest)
my_home.add_item(table)

print(my_home)