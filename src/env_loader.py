from dotenv import load_dotenv
import os

def load_environment_variables():
    load_dotenv()

def get_env_variable(key, prompt_message=None):
    value = os.getenv(key)
    if not value and prompt_message:
        value = input(prompt_message)
        save_env_variable(key, value)
    return value

def save_env_variable(key, value):
    with open('.env', 'a') as env_file:
        env_file.write(f"\n{key}={value}")