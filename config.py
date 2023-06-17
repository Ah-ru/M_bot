import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TGAPI")
group_id = os.getenv("GID")
database = os.getenv("NDB")