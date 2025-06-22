import os
from multiprocessing import Process

def start_main():
    os.system("python3 main.py")

def start_bot(bot_file):
    os.environ["BOT_ID"] = bot_file
    os.system(f"python3 child_bot.py")

if __name__ == "__main__":
    Process(target=start_main).start()
    
    for bot_id in ["bot1", "bot2", "bot3", "bot4", "bot5", "bot6", "bot7", "bot8", "bot9", "bot10"]:
        Process(target=start_bot, args=(bot_id,)).start()
