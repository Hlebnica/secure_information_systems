import random
import pandas as pd
import sys

S = ["Read", "Write", "Grant privileges", "Forbidden", "All privileges"] # Набор привелегий
users = ("Admin", "User1", "User2", "User3", "User4", "User5") # Субъекты 
user_count = len(users)
objects = ("Object1", "Object2", "Object3", "Object4", "Object5") # Объекты
object_count = len(objects)

# Заполнения матрицы доступа

access_matrix = {}

for user in users:
    access_matrix[user] = {}
    for OBJECT in objects:
        if user == "Admin":
            access_matrix[user][OBJECT] = ["All privileges"]
        else:
            privileges_count = random.randint(1, 3)
            privileges = []
            match privileges_count:
                case 1:
                    privilege = random.randint(0, 4)
                    privileges.append(S[privilege])
                case _:
                    tmp_priv = random.sample(S[0:3], privileges_count)
                    for i in range(privileges_count):
                        privileges.append(tmp_priv[i])

            access_matrix[user][OBJECT] = privileges


print(pd.DataFrame.from_dict(access_matrix).T)

# Авторизация пользователя и вывод его прав

while True:
    print("login", end="")
    cur_user = input()

    if cur_user not in users:
        print("Wrong username!")
        continue

    else:
        print(f'User: {cur_user}')
        print('Identification successful, welcome to the system!')
        print('List of your privileges:')
        for _ in access_matrix[cur_user]:
            privileges= ""
            for priv in access_matrix[cur_user][_]:
                if len(privileges) == 0:
                    privileges += priv
                else:
                    privileges += ", " + priv
            print(f'\t{_}: {privileges}')
    break

# Обработка команд по матрице доступа

while True:
    command = input("Enter command > ")

    if command == "quit":
        print(f"The work of the user {cur_user} is finished. Goodbye.")
        cur_user = None
        break

    if command not in ("read", "write", "grant"):
        print("Wrong command")
        sys.stdout.flush()
        continue

    # Чтение файла
    elif command == "read": 
        print("Which object is being operated on? (read)")
        cur_obj = input()
        if cur_obj not in objects:
            print("There is no such object in the system.")
            sys.stdout.flush()
            continue
        if "Read" not in access_matrix[cur_user][cur_obj] and "All privileges" not in access_matrix[cur_user][cur_obj]:
            print("Refusal to perform an operation. You have no rights to perform it.")
            sys.stdout.flush()
            continue
        print("The operation was successful! (read)")

    # Запись в файл
    elif command == "write": 
        print("Which object is being operated on? (write)")
        cur_obj = input()
        if cur_obj not in objects:
            print("There is no such object in the system.")
            sys.stdout.flush()
            continue
        if "Write" not in access_matrix[cur_user][cur_obj] and "All privileges" not in access_matrix[cur_user][cur_obj]:
            print("Refusal to perform an operation. You have no rights to perform it.")
            sys.stdout.flush()
            continue
        print("The operation was successful! (write)")

    # Передача прав доступа
    elif command == "grant": 
        print("Which object is being operated on? (grant)")
        cur_obj = input()
        if cur_obj not in objects:
            print("There is no such object in the system.")
            sys.stdout.flush()
            continue
        if "Grant privileges" not in access_matrix[cur_user][cur_obj] and "All privileges" not in access_matrix[cur_user][cur_obj]:
            print("Refusal to perform an operation. You have no rights to perform it.")
            sys.stdout.flush()
            continue
        print("What privilege is being transferred? (Read/Write/Grant privileges/Forbidden/All privileges)")
        cur_privilege = input()
        if cur_privilege not in S:
            print("There is no such privilege in the system. ")
            sys.stdout.flush()
            continue
        print("To which user is the right transferred? ")

        selected_user = input()
        if selected_user not in users:
            print("There is no such user in the system.")
            sys.stdout.flush()
            continue
        if cur_privilege not in access_matrix[selected_user][cur_obj] and "All privileges" not in access_matrix[selected_user][cur_obj]:
            access_matrix[selected_user][cur_obj].append(cur_privilege)
            print("The operation was successful.")
        else:
            print("User already has this privilege.")