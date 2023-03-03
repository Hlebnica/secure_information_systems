import pandas as pd
import numpy as np

S = ["Доступ на чтение", "Доступ на запись", "Передача прав"] # Набор операций над объектами
U = ["Пользователь 1", "Пользователь 2", "Пользователь 3", "Пользователь 4", "Пользователь 5", "Пользователь 6"] # Множество субъектов
O = ["Объект 1", "Объект 2", "Объект 3", "Объект 4", "Объект 5"] # Множество объектов доступа

def get_random_rights(access_rights):
    rights = np.random.choice(access_rights, size=np.random.choice(len(access_rights) + 1), replace=False)

    if len(rights) == 0 or len(rights) == 1 and "Передача прав" in rights:
        rights = ["Запрет"]
    elif len(rights) == len(access_rights):
            rights = ["Полные права"]
    return rights

access_matrix = pd.DataFrame(columns=[f"Объект{n+1}" for n in range(len(O))], index=U[:len(U)])
access_matrix = access_matrix.applymap(lambda x: get_random_rights(S))

access_matrix.iloc[[np.random.randint(len(access_matrix.index))]] = ['Полные права']
print(access_matrix)

while True:
    user_id = input("Введите идентификатор пользователя: ")

    if user_id not in U:
        print("Неверный идентификатор пользователя.")
        continue
    else:
        user_rights = access_matrix.loc[user_id] 
        print(f"Идентификация прошла успешно, добро пожаловать в систему, {user_id}!")
        print("Перечень Ваших прав:")

        for obj, rights in user_rights.items():
            print(f"{obj}: {', '.join(rights)}")
        break
        
while True:
    command = input("Жду ваших указаний > ")

    if command.lower() == "quit":
        print(f"Работа пользователя {user_id} завершена. До свидания.")
        break

    if command.lower() not in S:
        print("Неверная команда.")
        continue

    obj_number = input("Над каким объектом производится операция? ")
    if obj_number not in O:
        print("Неверный номер объекта.")
        continue

    obj_index = O.index(obj_number)
    user_rights = access_matrix.loc[user_id]
    obj_rights = user_rights[f"Объект{obj_index+1}"]

    if command.lower() == "grant":
        if "Передача прав" not in obj_rights:
            print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")
            continue

        obj_to_grant = input("Право на какой объект передается? ")
        if obj_to_grant not in O:
            print("Неверный номер объекта.")
            continue

        user_to_grant = input("Какому пользователю передается право? ")
        if user_to_grant not in U:
            print("Неверный идентификатор пользователя.")
            continue

        object_to_grant = input("Право на какой объект передается? ")
    if object_to_grant not in O:
        print("Неверный идентификатор объекта.")
        continue

    right_to_grant = input("Какое право передается? ")
    if right_to_grant not in S:
        print("Неверный идентификатор права.")
        continue

    if "Передача прав" not in user_rights[object_to_grant]:
        print("Отказ в выполнении операции. У Вас нет прав для ее осуществления")
        continue

    user_rights_to_grant = access_matrix.loc[user_to_grant]
    if "Передача прав" not in user_rights_to_grant[object_to_grant]:
        print("Отказ в выполнении операции. У пользователя, которому Вы хотите передать право, нет прав на передачу прав.")
        continue

    access_matrix.at[user_to_grant, object_to_grant] = [right_to_grant]
    print("Операция прошла успешно")

    if command == "quit":
        print(f"Работа пользователя {user_id} завершена. До свидания.")
        break

    else:
        print("Неверная команда. Повторите попытку.")
