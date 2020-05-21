import boto3
# from boto.mturk.connection import MTurkConnection
# from boto.mturk.question import HTMLQuestion
import numpy as np

import os
import argparse

from mturk_html import html_start, html_end, test, real, filenames_div


bad_names = ["bad-LJ001-0015", "bad-LJ001-0051", "bad-LJ001-0063", "bad-LJ001-0072", "bad-LJ001-0079", "bad-LJ001-0094"]
good_names = ["GT-LJ001-0063", "GT-LJ001-0072", "GT-LJ001-0096", "GT-LJ001-0102", "GT-LJ001-0173"]

def creat_quesiton(expname):
    alreay_used = set()

    modified_good_names = [name for name in good_names if name[-2:] not in alreay_used]

    divs = []

    goods = np.random.choice(modified_good_names, size=2, replace=False)
    divs.append(test.format(testname=goods[0]))
    divs.append(test.format(testname=goods[1]))
    alreay_used.add(goods[0][-2:])
    alreay_used.add(goods[1][-2:])

    modified_bad_names = [name for name in bad_names if name[-2:] not in alreay_used]
    bads = np.random.choice(modified_bad_names, size=2, replace=False)
    divs.append(test.format(testname=bads[0]))
    divs.append(test.format(testname=bads[1]))

    for i in range(10):
        audio_id = 'audio{}'.format(i)
        src_id = 'srcreal{}'.format(i) 
        slider_id = 'sreal{}'.format(i)
        divs.append(real.format(realexp=expname, realname='undefined', 
                                audio_id=audio_id,
                                src_id=src_id, slider_id=slider_id))

    np.random.shuffle(divs)

    filenames = ""
    for fn in os.listdir('audio_files/' + expname):
        filenames += fn + ","
    filenames = filenames[:-1]
    hidden_div = filenames_div.format(filenames=filenames)

    question_html_value = html_start
    question_html_value += hidden_div
    for i in range(len(divs)):
        question_html_value += divs[i]
    question_html_value += html_end

    return question_html_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--expname", type=str, required=True)
    args = parser.parse_args()

    q = creat_quesiton(args.expname)
    with open("gen_mturk.html", "w") as fp:
        fp.write(q)


