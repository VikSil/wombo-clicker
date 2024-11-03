import numpy as np
import os
import pandas as pd
import platform
import random

from browser import Browser
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

operating_system = platform.platform()

if 'Windows' in operating_system:
    DOWNLOAD_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '\\pics\\010_new\\'
    INPUT_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '\\words\\01_new_prompts\\'
else:
    DOWNLOAD_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/pics/010_new'
    INPUT_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/words/01_new_prompts'

STYLES = [
    'dreamland_v3',
    'cartoon_v3',
    'surrealism_v3',
    'expressionism_v3',
    'impressionism_v3',
    'pastel_v3',
    'diorama_v3',
    'papercut_v3',
    'flat_v3',
    'graffiti_v3',
]


def clicker(input_file: str):
    """
    Reads the input file
    For each line in the file generates images via wombo dream.ai
    """
    print('I am a clicker')
    prompts = pd.read_csv(input_file, sep='|', header=None, names=['prompt', 'style', 'count'])
    prompts = prompts.replace({np.nan: None})
    print('Processing prompts:')
    print(prompts)

    browser = Browser()
    open_wombo(browser)
    browser.sleep(10)

    results = [
        process_prompt(row[0], row[1], row[2], browser)
        for row in zip(prompts['prompt'], prompts['style'], prompts['count'])
    ]

    browser.sleep(5)

    if False in results:  # at least one of the lines failed
        print('Some of the prompts failed. Will reprocess them.')
        prompts['results'] = results
        if 'Windows' in operating_system:
            filename = f'{INPUT_DIR}\\reprocess_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        else:
            filename = f'{INPUT_DIR}/reprocess_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'

        failed_df = prompts[prompts.results != True]
        failed_df = failed_df.replace({None: np.nan})
        failed_df = failed_df.drop(columns=['results'])
        failed_df.to_csv(filename, sep='|', index=False, header=False)

        return False
    return True


def close_popup(browser: Browser):
    try:  # check for regular popup
        browser.find_element(by=By.CLASS_NAME, id='Overlay__ModalBody-sc-1pt5jsh-1')
    except NoSuchElementException:
        pass
    else:
        browser.click_button(by=By.CLASS_NAME, id='Button-sc-1fhcnov-2')

    try:  # check for login screen - cannot be closed
        browser.find_element(by=By.CLASS_NAME, id='LoginModalBody__InputsContainer-sc-1828sj0-2')
    except NoSuchElementException:
        pass
    else:
        return False

    browser.sleep(1)

    return True


def open_wombo(browser: Browser):
    browser.open_page('https://dream.ai/create')


def process_prompt(prompt: str, style: str, count: int, browser: Browser) -> bool:
    print(f'processing prompt {prompt} in style {style} of count {count}')

    style_ = style

    for i in range(count):

        if style is None:  # random style if no style is given
            style_ = random.choice(STYLES)
            print(f'style will be {style_}')

        if not close_popup(browser):
            return False

        try:
            # click the style button
            browser.click_if_not_selected(
                by=By.XPATH,
                id=f"//img[contains(@src, '{style_}')]",
            )

            browser.sleep(2)

            # add prompt
            browser.add_input(by=By.CLASS_NAME, id='TextInput__Input-sc-1qnfwgf-1', value=prompt)

            browser.sleep(2)

        except Exception as e:  # something unexpected
            print('exception in first try block')
            print(e)
            return False

        if not close_popup(browser):
            return False

        try:
            # click "Generate" button
            browser.click_button(by=By.CLASS_NAME, id='fMNHJW')

            browser.sleep(10)
            close_popup(browser)

            # click download button when it appears
            browser.wait_and_click(by=By.CLASS_NAME, id='SelectableItem__DownloadButton-sc-6c0djm-6', timeout=60)
            browser.sleep(2)

            # rename last downloaded file
            if 'Windows' in operating_system:
                filename = max([DOWNLOAD_DIR + "\\" + f for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getctime)
            else:
                filename = max([DOWNLOAD_DIR + "/" + f for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getctime)
            new_filename = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")}{prompt}_{style_}_{i}.jpg'
            os.rename(f'{filename}', f'{DOWNLOAD_DIR}/{new_filename}')

        except Exception as e:  # likely waiting timeout
            print('exception in second try block')
            print(e)
            return False

    return True
