class Animals:
    def __init__(self, name, species, age, weight, habitat):
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.habitat = habitat
    def describe(self):
        return (f"{self.name} ему {self.age} лет {self.species} весит {self.weight} kg, живущий в {self.habitat}.")
    def eat(self, food):
        return (f"{self.name} ест {food}.")

class Reptile(Animals):
    def __init__(self, name, species, age, weight, habitat, is_venomous, scale_type, body_temperature):
        super().__init__(name, species, age, weight, habitat)
        self.venomous = is_venomous
        self.scale_type = scale_type
        self.body_temperature = body_temperature

    def bask_in_sun(self):
        self.body_temperature += 5
        return (f"{self.name} греется на солнце. "
                f"Температура тела: {self.body_temperature}°C.")
    def shed_skin(self):
        return (f"{self.name} сбрасывает кожу. Чешуя типа: {self.scale_type}.")


class Amphibian(Animals):
    
 
    def __init__(self, name, species, age, weight, habitat,
                 skin_is_moist, lays_eggs_in_water, has_tail):
        super().__init__(name, species, age, weight, habitat)
        self.skin_is_moist = skin_is_moist                
        self.lays_eggs_in_water = lays_eggs_in_water      
        self.has_tail = has_tail                          
        self.stage = "взрослая особь"                     
 
    def swim(self):
        return (f"{self.name} плавает в воде и дышит кожей.")
 
    def metamorphosis(self):
        if self.lays_eggs_in_water:
            self.stage = "взрослая особь"
            return (f"{self.name} прошёл метаморфоз: икра → головастик → взрослая особь.")
        return (f"{self.name} развивается без водной стадии.")
 
 
if __name__ == "__main__":
    snake = Reptile("Каа", "Удав", 6, 12.5, "тропический лес",
                    is_venomous=False, scale_type="гладкая", body_temperature=25)
    frog = Amphibian("Кермит", "Лягушка", 2, 0.3, "пруд",
                     skin_is_moist=True, lays_eggs_in_water=True, has_tail=False)
 
    for animal in (snake, frog):
        print(animal.describe())
        print(animal.eat("насекомых" if animal is frog else "мышь"))
 
    print(snake.bask_in_sun())
    print(snake.shed_skin())
    print(frog.swim())
    print(frog.metamorphosis())
 
    # Проверка наследования
    print(isinstance(snake, Animals), isinstance(frog, Animals))
    print(isinstance(snake, Amphibian), isinstance(frog, Reptile))







class ZooShow:
    VIP_PRICE = 1500
    REGULAR_PRICE = 700

    def __init__(self):
        self.reptiles = [
            Reptile("Каа", "Удав", 6, 12.5, "тропический лес",
                    is_venomous=False, scale_type="гладкая", body_temperature=25),
            Reptile("Ржавый", "Кобра", 4, 5.0, "пустыня",
                    is_venomous=True, scale_type="сухая", body_temperature=28),
        ]
        self.amphibians = [
            Amphibian("Кермит", "Лягушка", 2, 0.3, "пруд",
                      skin_is_moist=True, lays_eggs_in_water=True, has_tail=False),
            Amphibian("Том", "Тритон", 3, 0.1, "болото",
                      skin_is_moist=True, lays_eggs_in_water=True, has_tail=True),
        ]

    def ask(self, question, options):
        while True:
            answer = input(question).strip()
            if answer in options:
                return answer
            print("Неверный ввод, попробуйте ещё раз.")

    def start(self):
        print("Билеты на шоу:")
        print(f"  VIP (места 1-10) — {self.VIP_PRICE} сом")
        print(f"  Обычный (места 11-50) — {self.REGULAR_PRICE} сом")
        print()

        print("Какое шоу хотите посмотреть?")
        print("  1 - Шоу пресмыкающихся")
        print("  2 - Шоу земноводных")
        show = self.ask("Ваш выбор: ", ["1", "2"])

        if show == "1":
            title = "ШОУ ПРЕСМЫКАЮЩИХСЯ"
            kind = "пресмыкающиеся"
            animals = self.reptiles
            action = "Сальто крутят"
        else:
            title = "ШОУ ЗЕМНОВОДНЫХ"
            kind = "земноводные"
            animals = self.amphibians
            action = "Стих читают "

        print()
        print(f"Программа шоу ({kind}):")
        for animal in animals:
            print(animal.describe())
            if isinstance(animal, Reptile):
                print(animal.bask_in_sun())
                print(animal.shed_skin())
            else:
                print(animal.swim())
                print(animal.metamorphosis())
            print()

        print("Выберите билет:")
        print(f"  1 - VIP, {self.VIP_PRICE} сом (места 1-10)")
        print(f"  2 - Обычный, {self.REGULAR_PRICE} сом (места 11-50)")
        ticket = self.ask("Ваш выбор: ", ["1", "2"])

        if ticket == "1":
            ticket_name = "VIP"
            price = self.VIP_PRICE
            seats = range(1, 11)
        else:
            ticket_name = "Обычный"
            price = self.REGULAR_PRICE
            seats = range(11, 51)

        seat = self.ask(f"Выберите место ({seats[0]}-{seats[-1]}): ",
                        [str(s) for s in seats])

        print()
        print(f"Ваш билет: {ticket_name}, место {seat}, цена {price} сом")
        print(f'"{title}" они {action}')


if __name__ == "__main__":
    ZooShow().start()