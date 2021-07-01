import os
from pdf2docx import Converter
from telegram.ext import *
from telegram import *
import docx2pdf
from server import keep_alive
import subprocess
import time


def start(update, context):
    update.message.reply_text("Welcome to DOCX and PDF converter\n"
                              "Please upload <b>Docx</b> to convert into <b>pdf</b> or\n"
                              "upload <b>Pdf</b> to convert into <b>docx</b>", parse_mode="HTML"
                              )


def pdf_handler(update, context):
    fileid = update.message.document
    print(fileid)
    file = bot.get_file(fileid.file_id)
    filename = fileid.file_name
    file.download(filename)
    time_to_wait = 30
    time_counter = 0
    while not os.path.exists(filename):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait: break
    cv = Converter(filename)
    cv.convert()
    cv.close()
    bot.send_document(chat_id=update.effective_chat.id, document=open(filename.split(".")[0] + ".docx", 'rb'))


def docx_handler(update, context):
    fileid = update.message.document
    file = bot.get_file(fileid.file_id)
    filename = fileid.file_name
    file.download(filename)
    time_to_wait = 30
    time_counter = 0
    while not os.path.exists(filename):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait: break
    docx2pdf.convert(filename)
    bot.send_document(chat_id=update.effective_chat.id, document=open(filename.split(".")[0] + ".pdf", 'rb'))


keep_alive()

dp = updater.dispatcher
dp.add_handler(CommandHandler("Start", start))
dp.add_handler(MessageHandler(Filters.document.pdf, pdf_handler))
dp.add_handler(MessageHandler(Filters.document.docx, docx_handler))
updater.start_polling()
updater.idle()
