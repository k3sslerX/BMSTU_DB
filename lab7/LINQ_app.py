import linq_to_obj
import linq_to_json
import linq_to_sql


def print_menu():
    print("1. LINQ to Object")
    print("2. LINQ to XML/JSON")
    print("3. LINQ to SQL")
    print("0. Выход")
    print("----------------------------------------")


mode = -1
while mode != 0:
    print_menu()
    try:
        mode = int(input('Введите действие: '))
    except ValueError:
        print("Введено неверное значение. Попрообуйте снова.")
        mode = -1
    else:
        if 0 > mode > 3:
            print('Введено неверное значение. Попробуйте снова.')
        else:
            if mode == 1:
                linq_to_obj.task_1()
            elif mode == 2:
                linq_to_json.task_2()
            elif mode == 3:
                linq_to_sql.task_3()
            elif mode == 0:
                print('Выход.')
            input('Нажмите Enter для выхода.')
