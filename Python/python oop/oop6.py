class A:
    def test(self):
        print("A---test method")
    def demo(self):
        print("A---demo method")

class B:
    def test(self):
        print("B---test method")
    def demo(self):
        print("B---demo method")

class C(A, B):
    pass

c = C()
c.test()
c.demo()
print(C.__mro__)
print(dir(object))