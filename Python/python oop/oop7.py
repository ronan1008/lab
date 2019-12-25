class Dog:
    def __init__(self, name):
        self.name = name 

    def game(self):
        print("%s play and jump" % self.name)

class XiaoTianDog(Dog):

    def game(self):
        print("%s fly into sky" % self.name)


class Person:
    def __init__(self, name):
        self.name = name
    
    def game_with_dog(self, dog):
        print("%s and %s happy to play" % (self.name, dog.name))

        dog.game()


#wangcai = Dog("旺財")
wangcai = XiaoTianDog("飛天旺財")
xiaoming = Person("小明")
xiaoming.game_with_dog(wangcai)


