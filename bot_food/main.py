import os
import sys
from pathlib import Path
from tg_bot.bot_food import main

current_dir = Path(__file__).parent
sys.path.append(str(current_dir))


if __name__ == "__main__":
main()
