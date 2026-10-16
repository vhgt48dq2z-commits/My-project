import random 
box = ["snake", "cake", " phone", "hole"]
choice = random.choice(box) 
print(choice) 
if choice == "snake":
    print("You died")
elif choice=="cake":
    print("You win")
