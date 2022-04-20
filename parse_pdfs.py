from pdfminer.high_level import extract_text
import csv

# MAX_ROLL_CALL_NUMBER = 253
# MAX_ROLL_CALL_NUMBER = 449
MAX_ROLL_CALL_NUMBER = 109
CONGRESS = 117
SESSION = 2
YEAR = 2022

mega_list = []
ROLL_CALL = 1
while MAX_ROLL_CALL_NUMBER >= ROLL_CALL:
    try:
        print(f"working  on {ROLL_CALL}")
        text = extract_text(f'data/{YEAR}/pdfs/{ROLL_CALL}.pdf')
    except:
        print(f'skipping {ROLL_CALL}')
        ROLL_CALL += 1
        continue

    # handling 2020 format
    if 'Watson \nColeman' in text:
        text = text.replace('\nWatson \nColeman', '\nWatson Coleman')
    if 'Doyle, Michael F. \n(PA)' in text:
        text = text.replace('Doyle, Michael F. \n(PA)', 'Doyle, Michael F. (PA)')
        text = text.replace('\n\n(Cartwright)', '\n(Cartwright)')

    if '\n(Wasserman \nSchultz)' in text:
        text = text.replace('\n\nPayne', '\nPayne')
        text = text.replace('\n\nHastings', '\nHastings')
        text = text.replace('\n\n(Pallone)', '\n(Pallone)')
        text = text.replace('\n(Wasserman \nSchultz)', '\n(Wasserman Schultz)')

    split_up = text.split('\n\n')

    split_up.pop(-1)

    if (f"{YEAR}" in split_up[0]) and (len(split_up[0].split('\n'))==3):
        date = split_up.pop(0)
        date = date.split('\n')[2]

    removed_header = []
    for seg in split_up:
        seg_clean = seg.split(f"{YEAR}")[-1]
        if seg_clean not in (' ', ') ', '  '):
            removed_header.append(seg_clean)

    with open(f'data/{YEAR}/extracted/{ROLL_CALL}.csv', 'w') as file:
        f = csv.writer(file)
        f.writerow(['Voted By Proxy', 'Proxy', f'Congress: {CONGRESS}', f'Session: {SESSION}', f'Roll Call Vote: {ROLL_CALL}'])
        while len(removed_header) > 0:
            # print(len(removed_header))
            # print(removed_header)
            one = removed_header.pop(0)
            two = removed_header.pop(0)

            voted_by_proxy = one.split('\n')
            proxy = two.split('\n')

            if voted_by_proxy[0] in (' ', '  '):
                voted_by_proxy.pop(0)
            if proxy[0] in (' ', '  '):
                proxy.pop(0)

            len(voted_by_proxy)
            len(proxy)
            # make into list
            counter = 0
            write_list = []
            while counter < len(voted_by_proxy):

                write_list.append([voted_by_proxy[counter].strip(), proxy[counter].strip()])
                mega_list.append([voted_by_proxy[counter].strip(), proxy[counter].strip().removeprefix("(").removesuffix(")").strip(), CONGRESS, SESSION, ROLL_CALL, date])
                counter += 1

            for row in write_list:
                f.writerow(row)

    ROLL_CALL += 1

with open(f'data/{YEAR}/extracted/full_list.csv', 'w') as file:
    f = csv.writer(file)
    f.writerow(['Voted By Proxy', 'Proxy', 'Congress', 'Session', 'Roll Call Vote Number', 'Date'])

    for row in mega_list:
        f.writerow(row)
