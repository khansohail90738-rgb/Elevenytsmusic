# start.py - Start Command and Basic Bot Interactions

from pyrogram import enums, errors, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Elevenyts import app, config, db, lang
from Elevenyts.helpers import buttons, utils


# ==============================
# DIGITAL STYLE THEME
# ==============================

DIGITAL_LINE = "━━━━━━━━━━━━━━━━━━"
DIGITAL_EMOJI = "⚡"


@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    """Handle /help command with digital styled menu."""

    try:
        await m.delete()
    except Exception:
        pass

    help_caption = f"""
{DIGITAL_LINE}
{DIGITAL_EMOJI} **{app.name} DIGITAL HELP MENU**
{DIGITAL_LINE}

🎵 **Advanced Music Features**
🎧 High Quality Streaming
⚙️ Smart Group Controls
🚀 Fast & Smooth Performance

💡 Use buttons below to explore commands.

{DIGITAL_LINE}
"""

    try:
        await m.reply_photo(
            photo=config.START_IMG,
            caption=help_caption,
            reply_markup=buttons.help_markup(m.lang),
            quote=True,
        )

    except Exception:
        await m.reply_text(
            text=help_caption,
            reply_markup=buttons.help_markup(m.lang),
            quote=True,
        )


@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    """
    Digital styled start command.
    """

    if message.chat.type != enums.ChatType.PRIVATE:
        try:
            await message.delete()
        except Exception:
            pass

    if not message.from_user:
        return

    # Blacklist check
    if (
        message.from_user.id in app.bl_users
        and message.from_user.id not in db.notified
    ):
        return await message.reply_text(
            "❌ You are blocked from using this bot."
        )

    # Help Menu
    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    private = message.chat.type == enums.ChatType.PRIVATE

    # ==============================
    # DIGITAL START MESSAGE
    # ==============================

    if private:
        _text = f"""
{DIGITAL_LINE}
⚡ **WELCOME TO {app.name.upper()}**
{DIGITAL_LINE}

👋 Hello {message.from_user.first_name}

🎵 Premium Music Experience
🚀 Ultra Fast Streaming
💎 Smart Digital Player

➥ Add me to your group
➥ Promote me as admin
➥ Enjoy lag free music

{DIGITAL_LINE}
"""
    else:
        _text = f"""
{DIGITAL_LINE}
⚡ **{app.name.upper()} CONNECTED**
🎵 Ready To Play Music
{DIGITAL_LINE}
"""

    # ==============================
    # DIGITAL BUTTONS
    # ==============================

    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Me",
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 Help",
                    callback_data="help_back"
                ),
                InlineKeyboardButton(
                    "⚙️ Settings",
                    callback_data="settings_back"
                ),
            ],
            [
                InlineKeyboardButton(
                    "💎 Support",
                    url="https://t.me/YourSupportGroup"
                )
            ],
        ]
    )

    try:
        await message.reply_photo(
            photo=config.START_IMG,
            caption=_text,
            reply_markup=key,
            quote=not private,
        )

    except errors.ChatSendPhotosForbidden:
        await message.reply_text(
            text=_text,
            reply_markup=key,
            quote=not private,
        )

    # ==============================
    # USER DATABASE
    # ==============================

    if private:
        if await db.is_user(message.from_user.id):
            return

        await utils.send_log(message)
        return await db.add_user(message.from_user.id)


@app.on_message(
    filters.command(["playmode", "settings"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
async def settings(_, message: types.Message):
    """
    Digital settings menu.
    """

    try:
        await message.delete()
    except Exception:
        pass

    admin_only = await db.get_play_mode(message.chat.id)

    settings_text = f"""
{DIGITAL_LINE}
⚙️ **DIGITAL SETTINGS PANEL**
{DIGITAL_LINE}

🏷️ Group : {message.chat.title}

🎵 Play Mode :
{'Admins Only' if admin_only else 'Everyone'}

🌐 Language : English

💡 Manage your music system below.

{DIGITAL_LINE}
"""

    await utils.safe_text(
        message,
        settings_text,
        reply_markup=buttons.settings_markup(
            message.lang,
            admin_only,
            "en",
            message.chat.id,
        ),
        quote=True,
    )


@app.on_message(filters.new_chat_members, group=7)
@lang.language()
async def _new_member(_, message: types.Message):
    """
    Detect bot added in groups.
    """

    if message.chat.type != enums.ChatType.SUPERGROUP:
        return await message.chat.leave()

    for member in message.new_chat_members:
        if member.id == app.id:

            welcome_text = f"""
{DIGITAL_LINE}
⚡ **THANKS FOR ADDING {app.name.upper()}**
{DIGITAL_LINE}

🎵 Music System Activated
🚀 Ready For Streaming

💎 Give Admin Permission
🎧 Start Playing Songs

{DIGITAL_LINE}
"""

            try:
                await message.reply_photo(
                    photo=config.START_IMG,
                    caption=welcome_text,
                )
            except Exception:
                await message.reply_text(welcome_text)

            if await db.is_chat(message.chat.id):
                return

            await db.add_chat(message.chat.id)
