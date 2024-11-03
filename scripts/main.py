import os
import platform
import time

from datetime import datetime
from wombo_generator import clicker

operating_system = platform.platform()

if 'Windows' in operating_system:
    INPUT_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\words\\01_new_prompts\\"
    PROCESSED_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\words\\02_processed\\"
    FAILED_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\words\\03_failed\\"
else:
    INPUT_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/words/01_new_prompts"
    PROCESSED_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/words/02_processed"
    FAILED_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/words/03_failed"


def main():
    while True:
        time.sleep(60)

        for file in os.listdir(INPUT_DIR):  # iterrate over input files
            filename = os.fsdecode(file)
            processed = clicker(f'{INPUT_DIR}/{filename}')

            nowstr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
            if processed:  # All lines in the file succesful
                if 'Windows' in operating_system:
                    os.rename(f'{INPUT_DIR}/{filename}', f'{PROCESSED_DIR}\{nowstr}{filename}')
                else:
                    os.rename(f'{INPUT_DIR}/{filename}', f'{PROCESSED_DIR}/{nowstr}{filename}')
            else:
                if 'Windows' in operating_system:
                    os.rename(f'{INPUT_DIR}/{filename}', f'{FAILED_DIR}\{nowstr}{filename}')
                else:
                    os.rename(f'{INPUT_DIR}/{filename}', f'{FAILED_DIR}/{nowstr}{filename}')


if __name__ == "__main__":
    main()
