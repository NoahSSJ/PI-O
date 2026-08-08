from pathlib import Path
from config import loader

main = loader.ConfigLoader()
# main.load_config()
print(Path('.').resolve())
    