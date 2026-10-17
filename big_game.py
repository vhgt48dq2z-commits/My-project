import random
import time
import sys


def safe_input(prompt, valid_values=None, default=None):
    try:
        value = input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nВвод был прерван. Применяется значение по умолчанию.")
        return default

    if valid_values is not None and value not in valid_values:
        print("\nНекорректный ввод. Применяется значение по умолчанию.")
        return default

    return value


player = {
    "hp": 100,
    "ammo": 60,
    "saved": 0,
}

squad_hp = [100, 100]

survivors = [
    {"name": "Учительница Анна", "hp": 100, "rescued": False},
    {"name": "Ученик Дима", "hp": 100, "rescued": False},
    {"name": "Ученица Катя", "hp": 100, "rescued": False},
    {"name": "Алкоголик Петрович", "hp": 100, "rescued": False},
]


rooms = [
    ("Кабинет химии", 1),
    ("Спортзал", 3),
    ("Столовая", 2),
    ("Библиотека", 1),
]


def pause():
    try:
        input("\nНажмите Enter, чтобы продолжить...")
    except (EOFError, KeyboardInterrupt):
        print("\nПауза пропущена.")


def radio(text):
    try:
        print("\n📻 РАЦИЯ:")
        print(text)
        time.sleep(1)
    except Exception as exc:
        print(f"\nОшибка радиосвязи: {exc}")


def status():
    print("\n-------------------------")
    print(f"❤️ Ваше HP: {player['hp']}")
    print(f"👥 Напарник 1: {squad_hp[0]} HP")
    print(f"👥 Напарник 2: {squad_hp[1]} HP")
    print(f"🔫 Патроны: {player['ammo']}")
    print(f"🧍 Спасено людей: {player['saved']}")
    print("-------------------------")


def mission_failed(reason):
    print("\n" + "=" * 35)
    print("       МИССИЯ ПРОВАЛЕНА")
    print("=" * 35)
    print(f"\n{reason}\n")
    status()
    sys.exit()


def fight_zombie(name, zombie_hp):
    print(f"\n🧟 {name} преграждает вам путь!")

    while zombie_hp > 0 and player["hp"] > 0:
        print(f"""
❤️ Ваше HP: {player['hp']}   🧟 HP зомби: {zombie_hp}

1. Стрелять
2. Отступить
""")
        action = safe_input("> ", valid_values=["1", "2"], default="2")

        if action == "1":
            if player["ammo"] <= 0:
                print("\nПатроны закончились!")
            else:
                damage = random.randint(15, 35)
                zombie_hp -= damage
                player["ammo"] -= 1
                print(f"\n💥 Вы нанесли {damage} урона зомби.")

                if zombie_hp > 0:
                    bite = random.randint(15, 40)
                    player["hp"] = max(0, player["hp"] - bite)
                    print(f"🧟 Зомби укусил вас! -{bite} HP")

        elif action == "2":
            print("\n🏃 Вы отступаете от зомби.")
            return False

        else:
            print("Неверная команда.")

    if player["hp"] <= 0:
        mission_failed(f"Вас загрыз зомби в кабинете «{name}».")

    return zombie_hp <= 0


def run_game():
    try:
        print("=" * 50)
        print("       Операция по эвакуации не зараженных")
        print("=" * 50)

        print("""
🌆 Утро. Город охвачен эпидемией.

Заражённые заполонили улицы, им нужен ням ням, иначе они пухнут с голоду. ПОНЯЛ?!

В  школе забаррикадировались
учителя и ученики.

Ваш отряд из трёх солдат направлен
эвакуировать выживших.
""")

        pause()

        print("""
 Бронемашина останавливается
у ворот школы.

Вы и двое напарников выходите
и осматриваете территорию.
""")

        pause()

        radio("""
— Приём.
— Внутри школы есть выжившие.
— Найдите и выведите их к воротам.
— Соблюдайте осторожность, зомби внутри.
""")

        print("""
Что будете делать?

1. Проверить оружие
2. Проверить рацию
3. Осмотреть здание школы
""")

        choice = safe_input("> ", valid_values=["1", "2", "3"], default="3")

        if choice == "1":
            print("\n🔫 Оружие в порядке. Патроны на месте.")
        elif choice == "2":
            print("\n📻 Связь устойчивая.")
        elif choice == "3":
            print("\n🏫 Здание трёхэтажное. Часть окон разбита.")
        else:
            print("\nВы решаете не тратить время.")

        pause()

        radio("""
— Группа, входите через главный вход.
— Двигайтесь по коридорам осторожно.
""")

        print("""
🚪 Вы входите в школу.

Коридоры темны и пусты.
Слышны далёкие стоны.
""")

        pause()

        event = random.randint(1, 3)

        if event == 1:
            print("""
🧟 Из-за угла выходит одиночный зомби!
""")
            fight_zombie("Зомби в коридоре", random.randint(40, 70))

        elif event == 2:
            print("""
 Коридор пуст.

Вы слышите шорох где-то наверху.
""")

        else:
            print("""
 Свет мигает и гаснет.

Вы включаете фонари и двигаетесь дальше.
""")

        pause()

        print("""
 Впереди несколько кабинетов.
Нужно проверить их один за другим.
""")

        pause()

        for room_name, danger in rooms:
            try:
                print(f"\n🚪 Вы подходите к кабинету: {room_name}")

                print("""
1. Войти и проверить
2. Пропустить кабинет
""")

                choice = safe_input("> ", valid_values=["1", "2"], default="2")

                if choice != "1":
                    print("Вы решаете не проверять этот кабинет.")
                    pause()
                    continue

                zombie_chance = danger * 20

                if random.randint(1, 100) <= zombie_chance:
                    zombie_hp = 30 + danger * 20
                    won = fight_zombie(room_name, zombie_hp)

                    if not won:
                        print("Вы не стали зачищать этот кабинет до конца.")
                        pause()
                        continue

                not_rescued = [s for s in survivors if not s["rescued"]]

                if not_rescued and random.randint(1, 100) <= 60:
                    found = random.choice(not_rescued)
                    found["rescued"] = True
                    player["saved"] += 1

                    print(f"""
 В кабинете «{room_name}» вы находите выжившего:
{found['name']}!

Вы уводите его в безопасное место.
""")
                else:
                    print(f"В кабинете «{room_name}» никого не оказалось.")

                pause()

            except Exception as exc:
                print(f"\nОшибка в кабинете «{room_name}»: {exc}")
                pause()
                continue

        radio("""
— Внимание, группа .
— Обнаружено скопление зомби
  в спортивном зале.
— Возможно, там люди.
""")

        print("""
Что будете делать?

1. Прорваться в спортзал с боем
2. Струсить и обойти спортзал стороной
""")

        choice = safe_input("> ", valid_values=["1", "2"], default="2")

        if choice == "1":
            print("""
🔫 Вы врываетесь в спортзал.

Внутри  зомби!
""")

            zombies_left = random.randint(2, 3)

            while zombies_left > 0 and player["hp"] > 0:
                won = fight_zombie(f"Зомби #{zombies_left}", random.randint(30, 60))

                if won:
                    zombies_left -= 1
                else:
                    print("\nВы отступаете из спортзала, не зачистив его до конца.")
                    break

            if zombies_left == 0:
                print("""
✅ Спортзал зачищен!

Там прятались несколько учеников,
но, к счастью, все они уже эвакуированы ранее.
""")

                player["ammo"] += 20
                print("🔫 Вы находите ящик с патронами: +20")

        else:
            print("""
Вы решаете не рисковать
и обходите спортзал стороной.
""")

        pause()

        rescued_names = [s["name"] for s in survivors if s["rescued"]]

        print("\n" + "=" * 35)
        print("       ЭВАКУАЦИЯ")
        print("=" * 30)

        if len(rescued_names) == 0:
            print("""
Вы не нашли ни одного выжившего.
Отряд возвращается к машине ни с чем.
""")
            mission_failed("Вы никого не спасли ")
        else:
            print(f"\nВы выводите {len(rescued_names)} человек(а) к воротам:")
            for name in rescued_names:
                print(f" - {name}")

        pause()

        radio("""
— Приём.
— Эвакуация принята.
— Возвращайтесь на базу.

""")

        print("\n" + "=" * 35)
        print("       МИССИЯ ЗАВЕРШЕНА")
        print("=" * 35)

        status()

        if player["saved"] >= 3:
            print("\nОтличная работа! Большая часть людей спасена.")
        elif player["saved"] >= 1:
            print("\nМиссия выполнена, но не все выжившие найдены.")
        else:
            print("\nВы серьезно?")

    except Exception as exc:
        print(f"\nПроизошла непредвиденная ошибка: {exc}")
        print("Игра завершена.")
        status()
        sys.exit(1)


if __name__ == "__main__":
    run_game()
