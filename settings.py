import environs

env = environs.Env()
env.read_env()

TOKEN = env.str("TOKEN")
GROUP_ID = env.int("GROUP_ID")

DATABASE_PATH = env.str("DATABASE_PATH")

