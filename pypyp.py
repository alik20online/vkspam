# -*- coding: utf-8 -*-
import vk_api, random, time, requests
from unicaps import CaptchaSolver
from vk_api.utils import get_random_id

link = 'https://vk.cc/c5oRnE'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Connection': 'keep-alive'
}
params = {
        'access_token': '63c704b863c704b863c704b83163989777663c763c704b839c833961703ccb1fa8fdef1',
        'v': '5.92',
        'url': link,
}
url = 'https://api.vk.com/method/utils.checkLink'
rq = requests.get(url=url, params=params, headers=headers).json()['response']['status']
print(rq)

if rq[:3] == 'not':
    print('Ссылка не в бане, можно спамить')
else:
    print('Пиздец, ссылка в бане, меняй ссылку')
    raise SystemExit

global f_count, str, f_sum, vk_session, vk, y, tok, UserIDList, r, f, g, key, errormsg, za, randmsg

def main():
    global f_count, str, f_sum, vk_session, r, y, tok, UserIDList, f, g, key, errormsg, za, randmsg
    errormsg = 0
    key = 0
    f_sum = 0
    f_count = 0
    time.sleep(1)

    try:
        r = []
        get_f = vk_session.method('friends.get', {'count': 1})
        UserIDList = ''
        for f in get_f['items']:

            search = vk_session.method('friends.search', {"is_closed": "false",
                                                          "can_access_closed": "true",
                                                          'can_write_private_message': 1, 'count': 330})
            if search['count'] > 0:
                for y in search['items']:
                    if y['id'] not in r:
                        r.append(y['id'])
                        UserIDList = UserIDList + str(y['id']) + '\n'
                    f_sum = f_sum + 1
            time.sleep(2)
    except vk_api.exceptions.ApiError:
        print('Невалид')
        raise SystemExit
    print('Друзей получено: ', f_sum)
    time.sleep(0)
    f = open('UserIDList.txt', 'w')
    f.write(UserIDList)
    f.close()
    time.sleep(0)
    CAPTCHA_KEY = 'ea0e11330dd8e2bf028f0181921520ec' # тут у нас токен от капчи
    print('Начинаю спамить')
    time.sleep(1)

    with open("UserIDList.txt", "r") as file:
        f_sum = sum(1 for f in file)
    with open("UserIDList.txt", "r") as file:
        try:
            for f in map(lambda line: line.rstrip('\n'), file):
                try:
                    try:
                        f_userid = int(f)
                        link = 'https://vk.cc/c5oRnE',
                        linkrnd = random.choice(link)
                        textmessage = f'Чисто от сердца:) {linkrnd}',
                        msg_id = vk.messages.send(user_id=f_userid, message=textmessage, random_id=get_random_id()) # отправляем сообщение
                        vk.messages.delete(delete_for_all=0, message_ids=msg_id) # удаляем сообщение
                        f_count = f_count + 1
                        print('Сообщение отправлено', f_count, '/', f_sum)
                        time.sleep(0)  # задерж очка

                    except vk_api.exceptions.Captcha as captcha:  # капчка
                        captcha.get_url()
                        solver = CaptchaSolver("rucaptcha.com", api_key=CAPTCHA_KEY) #тут меняем сервис на нужный, варианты: 2captcha.com, anti-captcha.com, azcaptcha.com, cptch.net, rucaptcha.com
                        solved = solver.solve_image_captcha(captcha.get_image(), is_phrase=False, is_case_sensitive=False)
                        print("Решаем капчу!")
                        captcha.try_again(solved.solution.text)
                        print(f'Баланс {solver.get_balance()}')



                except vk_api.exceptions.ApiError:
                    f_count = f_count + 1
                    print('Невозможно отправить сообщение', f_count, '/', f_sum)
                    errormsg = errormsg + 1
                    pass

        except ValueError:
            print('Спам закончен!')
            time.sleep(2)
    print('Спам закончен!')


def auth():
    global vk_session, vk
    time.sleep(1)
    tok = input('Введите токен: ')
    print('Выполняется авторизация')

    vk_session = vk_api.VkApi(token=tok)
    vk = vk_session.get_api()
    main()

if __name__ == "__main__":
    auth()

print('сообщений отправлено: {0}'.format(f_count - 1), 'Ошибок: {0}'.format(errormsg))