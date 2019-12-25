class Animal:

    def eat(self):
        print("吃")

    def drink(self):
        print("喝")

    def run(self):
        print("跑")

    def sleep(self):
        print("睡")

class Dog(Animal):

    def bark(self):
        print("叫")

class XiaoTianQuan(Dog):

    def fly(self):
        print("I can fly")

    def bark(self):
        print("叫得跟神一樣")
        super().bark()
        print("$@#%@%")


class Cat(Animal):
    
    def catch(self):
        print("catch mouse")






xtq = XiaoTianQuan()
xtq.bark()


