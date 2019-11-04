class Car:
	def __init__(self,make,model,year):
		self.make = make
		self.model = model 
		self.year = year
		self.odometer_reading = 0

	def get_descripitive_name(self):
		long_name = f"{self.year} {self.make} {self.model}"
		return long_name.title()

	def read_odometer(self):
		print(f"This car has {self.odometer_reading} miles on it.")

	def update_odometer(self,mileage):
		if mileage >= self.odometer_reading:
			self.odometer_reading = mileage
		else:
			print("You can't roll back an odometer")
		self.odometer_reading = mileage

	def increment_odometer(self,miles):
		self.odometer_reading += miles

my_new_car = Car('audi','a4',2019)
print(my_new_car.get_descripitive_name())
#my_new_car.odometer_reading = 5
my_new_car.update_odometer(23_500)
my_new_car.read_odometer()
my_new_car.increment_odometer(100)
my_new_car.read_odometer()


class Battery:
	def __init__(self,battery_size=75):
		self.battery_size = battery_size
	def describe_baterry(self):
		print(f"This car has a {self.battery_size}-kWh battery.")
class ElectricCar(Car):

	def __init__(self,make,model,year):
		super().__init__(make,model,year)
		self.battery = Battery()


	def fill_gas_tank(self):
		print("This car dosn't need a gas tank!")




my_tesla = ElectricCar('tesla','model s',2019)
#print(my_tesla.get_descripitive_name())
#my_tesla.read_odometer()
my_tesla.battery.describe_baterry()