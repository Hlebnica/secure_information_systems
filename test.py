import pandas as pd
import numpy as np

S = ["read", "write", "grant"]  # Набор операций над объектами
U = ["User1", "User2", "User3", "User4", "User5", "User6"]  # Множество субъектов
O = ["Object1", "Object2", "Object3", "Object4", "Object5"]  # Множество объектов доступа


def get_random_rights(access_rights):
    rights_ = np.random.choice(access_rights, size=np.random.choice(len(access_rights) + 1), replace=False)

    if len(rights_) == 0 or len(rights_) == 1 and "grant" in rights_:
        rights_ = ["ban"]
    elif len(rights_) == len(access_rights):
        rights_ = ["full access"]
    return rights_


access_matrix = pd.DataFrame(columns=[f"Object{n + 1}" for n in range(len(O))], index=U[:len(U)])
access_matrix = access_matrix.applymap(lambda x: get_random_rights(S))

access_matrix.iloc[[np.random.randint(len(access_matrix.index))]] = [[['full access']]]
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

