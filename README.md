# rob_channel.py

Este repositorio contiene un bot de ejemplo para Pyrogram (Telegram) y un script ilustrativo.  
AVISO IMPORTANTE: el código que automatiza la adición o promoción de miembros en canales puede utilizarse indebidamente. No uses este bot para acceder, administrar o tomar control de canales ajenos sin el permiso explícito de sus propietarios. Hacerlo puede ser ilegal y/o violar los Términos de Servicio de Telegram. Usa este proyecto solo con fines legítimos y en canales donde tienes permiso.

## Descripción
El script escucha el comando `/rob` y pretende añadir/promover usuarios en un canal. El ejemplo original contiene un token de bot embebido (no seguro) y llamadas que probablemente no funcionen en todas las circunstancias. Este README explica cómo preparar un entorno seguro, ejecutar el bot y sugiere correcciones y buenas prácticas.

## Requisitos
- Python 3.8+
- Una cuenta de bot de Telegram (BotFather) y su token
- Pyrogram (se recomienda la última versión estable de la rama 2.x)
- tgcrypto (opcional pero recomendado para rendimiento criptográfico)

Instalación recomendada:
```bash
python -m venv .venv
source .venv/bin/activate   # o .venv\Scripts\activate en Windows
pip install pyrogram tgcrypto
```

## Seguridad y privacidad
- NUNCA subas el token de tu bot a un repositorio público. Trata el token como una contraseña.
- Borra cualquier token embebido del código y usa variables de entorno o un archivo .env (no versionado) para configuraciones sensibles.
- Revisa las limitaciones de la API de Telegram: los bots no pueden "unirse" arbitrariamente a canales privados por sí mismos; deben ser añadidos por un administrador humano del canal o usando enlaces de invitación.
- Obtén permiso explícito antes de añadir o promover usuarios en canales.

## Configuración
Exporta el token y el ID del usuario objetivo como variables de entorno (ejemplo en Linux/macOS):
```bash
export BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
export TARGET_USER_ID="7086746844"   # ajusta con el ID real del usuario que quieres promover (si aplica)
```

En Windows PowerShell:
```powershell
$env:BOT_TOKEN="123456:ABC..."
$env:TARGET_USER_ID="7086746844"
```

## Uso
Guarda el script (por ejemplo) como `rob_channel.py`. Asegúrate de haber configurado las variables de entorno. Ejecuta:
```bash
python rob_channel.py
```

Luego, desde Telegram charla con tu bot (o en el chat permitido), envía:
```
/rob <@nombre_de_usuario_del_canal_o_id> <url_del_canal_opcional>
```

El bot intentará promover al usuario cuyo ID esté en `TARGET_USER_ID`. Ten en cuenta que:
- El bot debe ser miembro del canal y tener permisos suficientes (ser administrador con permiso para promover otros).
- Si el canal es privado, el bot debe haber sido añadido por un administrador o usar un enlace de invitación válido.
- Si el bot no tiene permisos, la operación fallará.

## Código corregido y más seguro (ejemplo)
A continuación un ejemplo corregido y más seguro (no contiene token embebido). Este ejemplo usa `promote_chat_member` en lugar de intentos de auto-entrada al canal:

```python
# rob_channel.py (ejemplo mejorado)
import os
from pyrogram import Client, filters
from pyrogram.errors import RPCError

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID", "0"))

app = Client("my_bot", bot_token=BOT_TOKEN)

def promote_user(chat_id: str | int, user_id: int):
    # Ajusta los permisos que quieres otorgar
    return app.promote_chat_member(
        chat_id,
        user_id,
        can_change_info=True,
        can_post_messages=True,
        can_edit_messages=True,
        can_delete_messages=True,
        can_invite_users=True,
        can_pin_messages=True,
        can_manage_chat=True
    )

@app.on_message(filters.command("rob") & filters.private)
def rob_channel(client, message):
    if len(message.command) < 2:
        message.reply_text("Uso: /rob <@canal_o_chat_id> [url_opcional]")
        return

    channel_identifier = message.command[1]
    channel_url = message.command[2] if len(message.command) >= 3 else None

    if TARGET_USER_ID == 0:
        message.reply_text("TARGET_USER_ID no configurado en las variables de entorno.")
        return

    try:
        # Verificar que el bot es miembro/administrador del canal
        chat = client.get_chat(channel_identifier)

        # Promover al usuario objetivo (necesitas ser admin con permisos)
        promote_user(chat.id, TARGET_USER_ID)

        reply = f"Se intentó promover al usuario {TARGET_USER_ID} en {chat.title or chat.username}."
        if channel_url:
            reply += f"\nURL: {channel_url}"

        message.reply_text(reply)
    except RPCError as e:
        message.reply_text(f"Error de Telegram: {e}")
    except Exception as e:
        message.reply_text(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    app.run()
```

Notas sobre el ejemplo:
- Verifica permisos y pertenencia del bot antes de intentar promover.
- El bot no puede auto-invitarse a canales privados: un administrador humano debe añadirlo primero.
- Ajusta los permisos pasados a `promote_chat_member` según lo necesario.

## Buenas prácticas adicionales
- Mantén el token fuera del repositorio y usa secretos gestionados (por ejemplo, variables de entorno en tu host, secretos en CI/CD).
- Añade logs y manejo robusto de errores.
- Implementa validaciones para evitar comandos anónimos que intenten abusar del bot (por ejemplo, limitar acceso a usuarios concretos).
- Revisa y respeta los Términos de Servicio de Telegram.

## Problemas comunes
- "Bot is not a participant": añade el bot manualmente al canal y dale permisos admin.
- Permisos insuficientes: promueve al bot a admin con los permisos necesarios.
- Errores de API: revisa excepciones específicas (p. ej. FloodWait, ChatAdminRequired).

---
