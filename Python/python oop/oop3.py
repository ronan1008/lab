class Gun:

    def __init__(self, model):
        self.model = model
        self.bullet_count = 0

    def add_bullet(self, count):
        self.bullet_count += count

    def shoot(self):

        if self.bullet_count <= 0:
            print("[%s] no bullet... " % self.model)
            return 
        self.bullet_count -= 1 

        print("[%s] 凸凸凸....[%d]" %(self.model, self.bullet_count))

class Soldier:

    def __init__(self, name):
        self.name = name
        self.gun = None
    
    def fire(self):
        if self.gun == None:
            print("[%s] no gun " % self.name)
            return
        print("衝阿...[%s]" % self.name)
        self.gun.add_bullet(50)
        self.gun.shoot()


ak47 = Gun("AK47")

xusando = Soldier("許三多")
xusando.gun = ak47
xusando.fire()
print(xusando.gun)

