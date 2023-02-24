from misc import secrets
import logging

# logging.basicConfig(level=logging.INFO, filename="service.log", filemode="w") TODO: uncomment this code
secure_data = secrets.load_secrets()
import modules.tg_bot
