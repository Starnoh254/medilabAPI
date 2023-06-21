# Try/Except
# try:
#     x=5+4
# except:
#     print("failed")


# OOP
#An object has state and behaviours
#States - properties/attributes that define an object e.g color,height,name etc
#behaviours - functionality(what does the object do) e.g move(), eat() etc
#in programming states are properties and behaviours are functions/method
#class Dog():
    #constructor of properties
   # def __init__(self):
      #  self.color = "brown" 
       # self.age =4
       # self.name = "Mark"
       # self.weight = "30lb"

        # a function inside a class is called a method
   # def bark(self):
       # return f"{self.name} says woof!"
        
    #def laugh(self):
       # return f"{self.name} says woof!"
        

#Calll the object/Instantiate
#dog = Dog()
#print(dog.age)
#prefer
#message = dog.bark()
#print(type(message))

bookings = [{
    'x' :10,
    'y' :15
},{
    'x' :100,
    'y' : 76
}]


for booking in bookings:
    member = {
    'b':78
}
bookings['z'] = member
print(bookings)