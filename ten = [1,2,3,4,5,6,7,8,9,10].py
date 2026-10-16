ten = [1,2,3,4,5,6,7,8,9,10]
evens = [x for x in ten if x % 2 == 0]
sq = []
print(evens)
amount =len(ten)
for square in evens:
    square = square ** 2
    print(square)
    sq.append(square)
print(sq)

def output(lst = ten):
    while True:
        a = input("Enter index or 0 to exit: "). strip()
        if a == '0':
            break
        try:
            index = int(a)
            if index<0:
                raise IndexError
            print(f"Element at index {index} is {lst[index]}")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
        except IndexError:
            print("Index out of range. Please enter a valid index.")
output()