from __future__ import unicode_literals, print_function

import errno
import os, binascii
import sys
import pymysql
import re

# Library untuk signature validation
import base64
import hashlib
import hmac

# Library untuk menghandle argument yang di passing pada saat deploy server
from argparse import ArgumentParser

# Flask framework untuk mengatur routing dan request
from flask import Flask, request, abort

# Official SDK Linebot untuk konfigurasi dan inisialisasi webhook, serta komunikasi dengan api bot
from linebot import(
    LineBotApi, WebhookHandler
)
# Library linebot sdk untuk handling exception yang dihasilkan oleh sdk line bot
from linebot.exceptions import(
    InvalidSignatureError
)
# Library untuk masing-masing fitur/model yang diperlukan untuk bot ini
# MessageEvent untu menghandle pesan yang masuk ke webhook
# TextMessage adalah object pesan teks
# TextSendMessage handler untuk mengirim pesan teks (push/reply)
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom
)

# from conn import *
from messagevar import *

app = Flask(__name__)

# Line channel secret, didapat dari line developer
channel_secret = "59ddbf04f1c9b55f927c83f93c836ba5"
# Line access token, didapat dari line developer
channel_access_token = "Nu2ufpRa8DhhJ7BSxJpmEILjv69vqaYzGLxF0s00Cjg0pEwuFdARlC9awrtZgR7fjXBf3gnVS6wNaI6VoPjS4NbbMhhxyne6fpj8I3SW32LMd7tmWEgOTeT/YacRHmqzHnhEIgZPhqOp4o5HFXoldgdB04t89/1O/w1cDnyilFU="

# Cek apakah line secret ada
if channel_secret is None:
    print('Set LINE_CHANNEL_SECRET sebagai environment variable')
    sys.exit(1)
# Cek apakah line secret ada
if channel_access_token is None:
    print('Set LINE_CHANNEL_ACCESS_TOKEN sebagai environment variable')
    sys.exit(1)

# Inisialisasi instance LineBotApi
line_bot_api = LineBotApi(channel_access_token)

# Inisialisasi handler untuk masing-masing model pada webhook
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    text = event.message.text

    if text[:1] == '/':
        parsedText = text.split()
        command = parsedText[0][1:]

        if command == 'register':
            print("Event register berjalan", file=sys.stdout)
            # Jika pesan dikirimkan secara private (private chat)
            if isinstance(event.source, SourceUser):
                print("Mendapat pesan dari user lewat private chat", file=sys.stdout)
                profile = line_bot_api.get_profile(event.source.user_id)
                #check apakah userid sudah register atau belum
                #event.source.user_id is 
                isRegisteredVar = isRegistered(event.source.user_id)
                # Jika tidak terjadi error, dan user sudah register
                if isRegisteredVar:
                    print("User sudah terdaftar", file=sys.stdout)
                    #Reply buat gausa register
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text=alreadyRegistered)
                    )
                # Jika tidak terjadi error, dan user belum register
                elif isRegisteredVar == None:
                    print("User belum terdaftar, proses pendaftaran", file=sys.stdout)
                    generatedToken = generateToken()
                    # Jika register berhasil dan tidak ada error
                    if registerUser(event.source.user_id, generatedToken, profile.display_name):
                        print("User berhasil registrasi",file=sys.stdout)
                        #Reply register berhasil & lanjut ke tahap selanjutnya
                        #Kirim token
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextMessage(text=regSuccess.format(generatedToken))
                        )
                    # Jika terjadi error pada saat registrasi
                    else:
                        print("Error terjadi pada saat registrasi",file=sys.stderr)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextMessage(text=exceptionMsg.format(22,adminEmail))
                        )
                # Jika terjadi error
                else:
                    print("Error terjadi pada saat pengecekan status registrasi",file=sys.stderr)
                    # exception raised
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text=exceptionMsg.format(23,adminEmail))
                    )
            # Jika pesan dikirimkan melalui grup/bukan private chat
            else:
                print("Pesan dikirim melalui selain private chat", file=sys.stdout)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text=chatRoomFailed)
                )

        elif command == 'help':
            if isinstance(event.source, SourceUser):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text=helpMsg)
                )
            else :
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text=chatRoomFailed)
                )
        
        elif command == 'about':
            if isinstance(event.source, SourceUser):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text=aboutMsg.format(hotdropGithub))
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text=chatRoomFailed)
                )
        
        elif command == 'addsensor':
            print(parsedText[1])
            # Jika Event add sensor diterima melalui private chat
            if isinstance(event.source, SourceUser):
                print("event add sensor diterima melalui privvate chat" ,file=sys.stdout)
                if re.match('^[\w-]+$', parsedText[1]):
                    print("nama sensor valid",file=sys.stdout)
                    print(parsedText[1])
                    id_user = isRegistered(event.source.user_id)
                    if id_user:
                        print("User sudah registrasi",file=sys.stdout)
                        if registerSensor(parsedText[1], id_user['id_user']):
                            print("Sensor berhasil di tambahkan",file=sys.stdout)
                            #Reply penambahan sensor berhasil & lanjut ke tahap selanjutnya
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextMessage(text=addSensorSuccess.format(parsedText[1]))
                            )
                        # Jika terjadi error pada saat menambah sensor
                        else:
                            print("Terjadi error penambahan sensor",file=sys.stdout)
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextMessage(text=exceptionMsg.format(24,adminEmail))
                            )
                    elif isRegisteredVar == None:
                        print("User belum teregistrasi",file=sys.stdout)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextMessage(text=unregisteredMsg)
                        )
                    else:
                        print("Terjadi error pada saat cek status registrasi",file=sys.stdout)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextMessage(text=exceptionMsg.format(23,adminEmail))
                        )
                else:
                    print("Nama sensor tidak valid",file=sys.stdout)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text=illegalCharSensor)
                    )
            else:
                print("Menerima chat diluar private chat")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text=chatRoomFailed)
                )
                

def registerUser(line_user_id, generatedToken, full_name):
    dbconn = pymysql.connect(
        host='localhost',
        user='root',
        password='9L1reyib',
        db='hotdrop',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    success = False
    try:        
        with dbconn.cursor() as cursor:
            sql = "INSERT INTO `tb_user` (`line_id_user`, `token`, `full_name`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (line_user_id, generatedToken, full_name))
        dbconn.commit()
        success = True
    finally:
        dbconn.close()
        return success

def registerSensor(nama_sensor, id_user):
    print("nama sensor : {}, id_user : {}".format(nama_sensor, id_user),file=sys.stdout)
    dbconn = pymysql.connect(
        host='localhost',
        user='root',
        password='9L1reyib',
        db='hotdrop',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    success = False
    try:
        with dbconn.cursor() as cursor:
            sql = "INSERT INTO `tb_sensor` (`fk_id_user`, `sensor_name`) VALUES (%d, %s)"
            cursor.execute(sql, (id_user, nama_sensor))
        dbconn.commit()
        success = True
    finally:
        dbconn.close()
        return success

def isRegistered(line_user_id):
    dbconn = pymysql.connect(
        host='localhost',
        user='root',
        password='9L1reyib',
        db='hotdrop',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    registered = False
    try:
        with dbconn.cursor() as cursor:
            sql = "SELECT `id_user` FROM `tb_user` WHERE `line_id_user`=%s"
            cursor.execute(sql, (line_user_id,))
            result = cursor.fetchone()
            registered = True
            print(registered)
            print(result)
            return result
    finally:
        dbconn.close()
        if registered == False:
            return False

def generateToken():
    token = binascii.b2a_hex(os.urandom(16))
    return token

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + '[--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)