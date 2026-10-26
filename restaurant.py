from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


class MenuItem(ABC):
    def __init__(self, name: str, base_price: float):
        self.name = name
        self.base_price = base_price

    @abstractmethod
    def calculate_price(self) -> float:
        pass

    def get_display_name(self) -> str:
        return self.name


class Pizza(MenuItem):
    SIZES = ("маленькая", "средняя", "большая")

    def __init__(self, name: str, base_price: float, size: str = "средняя"):
        super().__init__(name, base_price)
        if size not in self.SIZES:
            raise ValueError(f"Размер должен быть одним из: {', '.join(self.SIZES)}")
        self.size = size

    def calculate_price(self) -> float:
        if self.size == "большая":
            return self.base_price * 1.30
        return self.base_price

    def get_display_name(self) -> str:
        return f"{self.name} ({self.size})"


class Drink(MenuItem):
    def __init__(self, name: str, base_price: float, is_ice: bool = False):
        super().__init__(name, base_price)
        self.is_ice = is_ice

    def calculate_price(self) -> float:
        return self.base_price

    def get_display_name(self) -> str:
        return f"{self.name} со льдом" if self.is_ice else self.name


class ComboSet(MenuItem):
    DISCOUNT = 0.15

    def __init__(self, name: str, items: list):
        super().__init__(name, 0)
        self.items = list(items)

    def calculate_price(self) -> float:
        total = sum(item.calculate_price() for item in self.items)
        return total * (1 - self.DISCOUNT)

    def get_display_name(self) -> str:
        inside = ", ".join(i.get_display_name() for i in self.items)
        return f"{self.name} [{inside}]"


class PaymentStrategy(ABC):
    @abstractmethod
    def collect_payment(self, amount: float) -> bool:
        pass


class CardPayment(PaymentStrategy):
    def __init__(self, card_number: str, expiry_month: int, expiry_year: int):
        self.card_number = card_number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year

    def _is_valid(self) -> bool:
        today = date.today()
        return (self.expiry_year, self.expiry_month) >= (today.year, today.month)

    def collect_payment(self, amount: float) -> bool:
        if not self._is_valid():
            print(f"❌ Карта просрочена ({self.expiry_month:02d}/{self.expiry_year}). Оплата отклонена.")
            return False
        masked = "**** **** **** " + self.card_number[-4:]
        print(f"💳 С карты {masked} списано {amount:.2f} руб.")
        return True


class CashPayment(PaymentStrategy):
    def collect_payment(self, amount: float) -> bool:
        print(f"💵 Оплата наличными курьеру: приготовьте {amount:.2f} руб.")
        return True


class OrderStatus(Enum):
    NEW = "Новый"
    COOKING = "Готовится"
    DELIVERING = "В доставке"
    DELIVERED = "Доставлен"


class Order:
    def __init__(self):
        self.__items = []
        self.__status = OrderStatus.NEW
        self.__is_paid = False

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @property
    def is_paid(self) -> bool:
        return self.__is_paid

    def next_step(self) -> None:
        stages = list(OrderStatus)
        index = stages.index(self.__status)
        if index == len(stages) - 1:
            raise ValueError("Заказ уже доставлен, дальше двигаться некуда.")
        self.__status = stages[index + 1]
        print(f"📦 Статус заказа: {self.__status.value}")

    def add_item(self, item: MenuItem) -> None:
        if self.__status != OrderStatus.NEW:
            raise ValueError(
                f"Нельзя добавить «{item.get_display_name()}»: заказ уже в статусе «{self.__status.value}»."
            )
        self.__items.append(item)

    def get_total_cost(self) -> float:
        return sum(item.calculate_price() for item in self.__items)

    def get_items(self) -> list:
        return list(self.__items)

    def pay(self, payment_method: PaymentStrategy) -> bool:
        if not self.__items:
            raise ValueError("Корзина пуста — платить не за что.")
        if self.__is_paid:
            raise ValueError("Заказ уже оплачен.")
        self.__is_paid = payment_method.collect_payment(self.get_total_cost())
        return self.__is_paid

    def print_receipt(self) -> None:
        print("\n===== ЧЕК =====")
        for item in self.__items:
            print(f"  {item.get_display_name():<60} {item.calculate_price():>8.2f} руб.")
        print(f"  {'ИТОГО':<60} {self.get_total_cost():>8.2f} руб.")
        print(f"  Статус: {self.__status.value}")
        print("===============\n")


if __name__ == "__main__":
    pizza = Pizza("Пепперони", 500, "большая")
    cola = Drink("Кола", 100, is_ice=True)
    lemonade = Drink("Лимонад", 120)
    small_pizza = Pizza("Маргарита", 400, "маленькая")
    combo = ComboSet("Обед", [small_pizza, lemonade])

    order = Order()
    order.add_item(pizza)
    order.add_item(cola)
    order.add_item(combo)
    order.print_receipt()

    order.pay(CardPayment("1234567812345678", 1, 2020))
    order.pay(CardPayment("1234567812345678", 12, 2030))

    order.next_step()

    try:
        order.add_item(Drink("Сок", 90))
    except ValueError as e:
        print("⚠️ Ошибка:", e)

    order.next_step()
    order.next_step()

    try:
        order.status = OrderStatus.NEW
    except AttributeError:
        print("🔒 Менять статус напрямую нельзя!")

    order2 = Order()
    order2.add_item(Drink("Чай", 80))
    order2.pay(CashPayment())
