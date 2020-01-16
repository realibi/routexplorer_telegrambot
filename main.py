import telebot
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


engine = create_engine("mysql+pymysql://%s:%s@localhost:3306/%s"
                       %("root","intersekt01","routexplorerdb"),echo=False)
if not database_exists(engine.url): 
    create_database(engine.url)	
    
con = engine.connect()
table_name = 'addresses'
command = "select * from _site_addresses;"
con.execute(command)

bot = telebot.TeleBot('759492961:AAEk5dQisql8M262cjCvDDHdJyd5XZTpL0E')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')


@bot.message_handler(content_types=['text'])
def send_text(message):
    delete_index = message.text.find("удалить")
    add_index = message.text.find("добавить")

    if delete_index != -1:
        deleting_address = message.text[0:delete_index-1]
        command = "delete from _site_addresses where address = '" + deleting_address + "';"
        print(command)
        con.execute(command)
        bot.send_message(message.chat.id, "Адрес " + deleting_address + " удален из списка ожидания")

    elif add_index != -1:
        command = "insert into _site_addresses(address, created_date, delivered) values('" + message.text[0:add_index] + "', '2020-01-14 14:48:58.315021', 0);" # Drop if such table exist
        con.execute(command)
    
        bot.send_message(message.chat.id, 'Адрес успешно добавлен в список ожидания!')

    else:
        bot.send_message(message.chat.id, 'Похоже, вы забыли добавить команду для выполнения. Добавьте нужную команду в конец сообщения, и попробуйте отправить сообщение снова.')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

    
bot.polling()