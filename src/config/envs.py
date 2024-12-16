from dotenv import load_dotenv
import os

load_dotenv()
envs = {
    "PORT": os.getenv("PORT"), 
    "DEBUG": os.getenv("DEBUG") == "True"
}