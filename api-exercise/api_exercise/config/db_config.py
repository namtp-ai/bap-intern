from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_CONNECTION_STRING: str = "mongodb+srv://Hoangminh:06092001@mongodb.ghm8i.mongodb.net/ICQC?authSource=admin&replicaSet=atlas-8pwbap-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"
