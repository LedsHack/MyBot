import telebot
import threading
import config as cfg
import get_promo as promo
from requests import get
token = 'ТОКЕН'
bot = telebot.TeleBot(token)
#valid group id
def check(id):
    if(str(id) == "-1001564114180"):
        return True
    else:
        send("Бот належить групі ІПЗ-1\nІ може використовуватися тільки там!", id)
        #print("#> " + str(id))
        return False
#send message
def send(sms, id):
  bot.send_message(id, sms)
#check admin status
def Permisson(user):
    return(user in getAdmin())
#admin config
def getAdmin():
    return (cfg.get("data/admin.json"))
#delete message(TODO) - (no use)
def clear(id, m_id):
    bot.delete_message(id, m_id)

@bot.message_handler(commands = ['admin'])
def admin(message):
    try:
        id = message.chat.id

        if(check(id)):
            if (Permisson("@" + message.from_user.username)):
                cmd = message.text.split()
                if(len(cmd) >= 2):

                    #add user permission admin
                    if(cmd[1] == "add"):
                        if(len(cmd) == 3):
                            if(not Permisson(cmd[2])):
                                cfg.set("data/admin.json", cmd[2], "@" + message.from_user.username)
                                send(cmd[2] + " видані права администратора", id)
                            else:
                                send(cmd[2] + " вже присутній в списку адміністрації", id)
                        else:
                            send("Використання: /admin add @username", id)

                    #remove user permission admin
                    elif(cmd[1] == "rem"):
                        if (len(cmd) == 3):
                            if(Permisson(cmd[2])):
                                send(cmd[2] + " удален со списка администрации", id)
                                cfg.rem("data/admin.json", cmd[2])
                            else:
                                send(cmd[2] + "  відсутній в списку адміністрації", id)
                        else:
                            send("Використання: /admin rem @username", id)

                    #admin list
                    elif (cmd[1] == "list"):
                        if (len(cmd) == 2):
                            list = getAdmin()
                            #print(list)
                            a = ""
                            for i in list:
                                a = a + "\n> " + i + " => " + list[i]
                            send("Список адміністраторів:" + a, id)
                            #bot.delete_message(id, message.message_id + 1)

                        else:
                            send("Використання: /admin list", id)
                    else:
                        send("Команда не знайденa!\n/admin add @username\n/admin rem @username\n/admin list", id)
                else:
                    send("Команда не знайденa!\n/admin add @username\n/admin rem @username\n/admin list", id)
    except Exception as error:
        send("Ошибка!\n" + str(error), 494198736)
        
@bot.message_handler(commands = ['kfc'])
def admin(message):
    try:
        id = message.chat.id
        if(check(id)):
            requests = promo.goPromo()
            if(requests[0]):
                bot.send_photo(id, get(requests[1][0]).content, caption = requests[1][1])
            else:
                send("Прости но 😢\n" + request[1], id)
    except Exception as error:
        send("Ошибка!\n" + str(error), 494198736)
        
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        id = message.chat.id
        if (check(id)):
            text = message.caption
            if (Permisson("@" + message.from_user.username)):
                if(text == None):
                    bot.delete_message(id, message.message_id)
                    send("Оскільки ви адміністратор вам обовязково потрібно додати опис файлу", id)
                else:
                    bot.forward_message("-1001736663041", id, message.message_id)
    except Exception as error:
        send("Ошибка!\n" + str(error), 494198736)


if __name__ == '__main__':
    print("!> Start")
    bot.polling(none_stop = True)
