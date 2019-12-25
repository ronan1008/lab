
class Cat:
    def __init__(self, new_name):
        self.name = new_name
        print("{} come on".format(self.name))


    def __del__(self):
        print("{} 我去了".format(self.name))

    def __str__(self):
        return "我是小貓[%s]" % self.name

tom = Cat("Tom")

print(tom)


class Person:

    def __init__(self, p_name, p_weight):
        self.name = p_name
        self.weight = p_weight

    def __str__(self):

        return "my name is {} my weight is {}".format(self.name, self.weight)

    def run(self):
        print("%s love run,run is good" % self.name)
        self.weight -= 0.5

    def eat(self):
        print("%s love eat,eat is good" % self.name)
        self.weight += 2

xiaoming = Person("小名",75.8)
xiaoming.run()
xiaoming.eat()
print(xiaoming)

xiaomei = Person("小美",45)
xiaomei.run()
xiaomei.eat()
print(xiaomei)
