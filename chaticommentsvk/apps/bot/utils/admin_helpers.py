from chaticommentsvk.config.config import config


def settings_status():
    return f"Длинна очереди:{config.bot.queue_length}\n" f"Тип постов: {config.bot.check_type}\n"


def admin_vips_status():
    admins = "\n".join(map(str, config.bot.admins))
    vips = "\n".join(map(str, config.bot.vip))
    return f"🔘Список админов \n{admins}\n" f"🔘Список vip \n{vips}\n"
