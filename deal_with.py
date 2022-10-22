import database
import time

operating = database.DataBase("127.0.0.1", "root", "123", "test", 3306)


def login_deal_with(user_name, password):
    result = operating.select_password_by_user_name_login(user_name)
    print(result)
    if result[0] == password:
        return True, result[1]
    else:
        return False, ""


def select_washing():
    result = operating.select_all_washing()
    time_ = []
    id = []
    k_x = []
    user_id = []
    for i in result:
        id.append(i[0])
        time_.append(i[1] + 10 - int(time.time()))
        k_x.append(i[2])
        user_id.append(i[3])
    return time_, id, k_x, user_id


def borrow(washing_id, user):
    operating.update_washing_j(int(time.time()), 1, user, washing_id)
    operating.update_user(user, washing_id)


def still(washing_id, user):
    operating.update_washing_h(washing_id)
    operating.update_user(user, 0)

