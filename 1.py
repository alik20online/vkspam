import vk_api
import time
from python_rucaptcha import ImageCaptcha

global f_count, str, f_sum, vk_session, vk, y, UserIDList, r, f, g, key, errormsg,MyID


def main():
    global f_count, str, f_sum, vk_session, r, y, UserIDList, f, g, key, errormsg, MyID
    errormsg = 0
    key = 0
    f_sum = 0  # кол-во строк с id друзей
    f_count = 0  # кол-во отправленных сообщений
    time.sleep(2)


    # сам парс
    try:
        r = []
        get_f = vk_session.method('friends.get', {'user_id': MyID, 'count': 1})  # получение списка всех друзей
        print('Начинаю парсить друзей')
        UserIDList = ''
        for f in get_f['items']:
            # получение друзей по одному из списка
            search = vk_session.method('friends.search', {'user_id': MyID, "is_closed": "false",
                                                          "can_access_closed": "true",
                                                          'can_write_private_message': 1, 'count': 400})
            if search['count'] > 0:
                for y in search['items']:
                    if y['id'] not in r:  # проверка на повторы
                        r.append(y['id'])
                        UserIDList = UserIDList + str(y['id']) + '\n'  # запись id в массив
                    f_sum = f_sum + 1
            time.sleep(2)
    except vk_api.exceptions.ApiError:  # проверка на auth
        print('Ошибка авторизации:')
        auth()
    print('Парс друзей окончен')
    print('Друзей получено: ', f_sum)
    time.sleep(2)

    f = open('UserIDList.txt', 'w')  # открытие / создание файлм
    f.write(UserIDList)  # запись в файл
    f.close()
    print('Сохраняю базу в UserIDList.txt')
    time.sleep(1)

    msgtospam = input('Введите сообщение для спама: ')
    time.sleep(2)

    print('Начинаю спамить')
    time.sleep(2)
    RUCAPTCHA_KEY = "1a93cd060213d05b9f1def843e3a00e1"
    with open("UserIDList.txt", "r") as file:  # получение кол-ва строк из списка
        f_sum = sum(1 for f in file)
    with open("UserIDList.txt", "r") as file:  # смпам по списку
        try:
            for f in map(lambda line: line.rstrip('\n'), file):  # f это f_userid в str
                try:
                    try:
                        f_userid = int(f)  # преобразование str в int
                        message_id = vk.messages.send(user_id=f_userid, message=msgtospam, random_id=0)  # отправка спама
                        f_count = f_count + 1
                        print('Сообщение отправлено', f_count, '/', f_sum)
                        vk.messages.delete(delete_for_all=0, message_ids=message_id)
                        time.sleep(0)
               

                    except vk_api.exceptions.Captcha as captcha:
                        captcha.get_url()
                        captcha.get_image()
                        image_link = captcha.get_url()
                        user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_link=image_link)
                        print(f"капча введена успешно")
                        captcha.try_again(user_answer['captchaSolve'])

                except vk_api.exceptions.ApiError:  # проверка на ошибки
                    print(f_userid, ': Невозможно отправить сообщение', f_count, '/', f_sum)
                    errormsg = errormsg + 1
                    pass

        except ValueError:
            print('Спам закончен!')
            time.sleep(2)
    print('Спам закончен!')


def auth():  # авторизация
    global vk_session, vk, MyID
    time.sleep(1)
    MyID = input('Введите id: ')
    tok = input('Введите токен: ')
    print('Выполняется авторизация')

    vk_session = vk_api.VkApi(token=tok)
    vk = vk_session.get_api()
    main()


if __name__ == "__main__":
    auth()

print('сообщений отправлено: {0}'.format(f_count - 1), 'Ошибок: {0}' .format(errormsg))
time.sleep(2)
input('Press ESC to exit')
