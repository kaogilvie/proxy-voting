import requests
import logging

consolehandler = logging.StreamHandler()
logger = logging.getLogger('tracker')
logger.addHandler(consolehandler)
logger.setLevel(logging.INFO)

logger.info("Create rollcall URL")

YEAR = '2020'
SESSION = '2' #even years are 2, odd are 1
CONGRESS_NUMBER = '116'
MAX_ROLL_CALL_NUMBER = 253
roll_call_url = f'https://clerk.house.gov/legislative/proxy-letters/{CONGRESS_NUMBER}/{SESSION}/votes/{YEAR}'

no_proxy = 0
roll_call_number = 1
while roll_call_number <= MAX_ROLL_CALL_NUMBER:
    logger.info(f"Downloading roll call {roll_call_number}")

    r = requests.get(f"{roll_call_url}/roll{roll_call_number}.pdf")

    if r.status_code == 404:
        logger.info("Can't find proxy vote for ")
        no_proxy += 1
    else:
        with open(f'data/{YEAR}/pdfs/{roll_call_number}.pdf', 'wb') as p:
            p.write(r.content)

    roll_call_number += 1

logger.info(f"No proxy votes: {no_proxy}")
