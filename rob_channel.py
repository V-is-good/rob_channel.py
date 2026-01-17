from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

# Configura el cliente con tu token de bot
app = Client("my_bot", bot_token="8579213873:AAFsNOtQGo1yb0Fx-T7F8_PQ29Mqm-37RO4")

# Función para agregar un usuario como administrador
def add_admin(channel_username, user_id):
    app.add_chat_members(channel_username, user_id, admin_rights=True)

# Manejador de mensajes para el comando /rob
@app.on_message(filters.command("rob"))
def rob_channel(client, message):
    # Extrae la URL y el nombre de usuario del canal del mensaje
    args = message.text.split(" ")
    if len(args) < 3:
        message.reply_text("Uso: /rob <nombre_de_usuario_del_canal> <url_del_canal>")
        return

    channel_username = args[1]
    channel_url = args[2]

    try:
        # Invita al bot al canal
        app.add_chat_members(channel_username, "me")

        # Agrega al usuario deseado como administrador
        add_admin(channel_username, 7086746844)  # Tu ID de usuario

        message.reply_text(f"¡He robado el canal {channel_username} y te he dado acceso como administrador!\nURL del canal: {channel_url}")
    except UserAlreadyParticipant:
        message.reply_text(f"Ya soy miembro del canal {channel_username}.")
    except Exception as e:
        message.reply_text(f"Ocurrió un error: {e}")

# Inicia el bot
app.run()