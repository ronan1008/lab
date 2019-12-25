class A:
    def __init__(self):
        self.num1 = 100
        self.__num2 = 200
    def __test(self):
        print("private methon %d %d" % (self.num1 , self.__num2))

    def test(self):
        print("public method %d" % self.__num2)
        self.__test()
        

class B(A):
    def demo(self):

        print("sub method %d" % self.num1)
        self.test()

        pass


b = B()
print(b)
b.demo()