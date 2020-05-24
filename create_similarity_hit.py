import boto3
# from boto.mturk.connection import MTurkConnection
# from boto.mturk.question import HTMLQuestion
import numpy as np
import random
import os
import argparse

from similarity_html import html_start, html_end, q_div, radio_ctrl, audio_ctrl, filenames_div


tests_f_dir = 'audio_files/tests_f'
tests_m_dir = 'audio_files/tests_m'
EXTENSION = '.wav'


def create_div(divname, expname, dirname_pair, fname_pair):
    audio_controls = [
        audio_ctrl.format(expname=expname, fname=fname_pair[0],
                          dirname=dirname_pair[0],
                          divname='audiosrc_vc'),
        audio_ctrl.format(expname=expname, fname=fname_pair[1],
                          dirname=dirname_pair[1],
                          divname='audiosrc_t')
    ]
    random.shuffle(audio_controls)

    radio_control = radio_ctrl.format(divname='radio',
                                      expname=expname,
                                      fname=fname_pair[0])

    div = q_div.format(divname=divname+'_div',
                       audio_control1=audio_controls[0],
                       audio_control2=audio_controls[1],
                       radio_control=radio_control)

    return div


def create_tests():
    test_f_names = [fn for fn in os.listdir(tests_f_dir) if fn.endswith(EXTENSION)]
    test_m_names = [fn for fn in os.listdir(tests_m_dir) if fn.endswith(EXTENSION)]

    sel_f = np.random.choice(test_f_names, size=3, replace=False)
    sel_m = np.random.choice(test_m_names, size=3, replace=False)

    goods = [(sel_f[0], sel_f[0]), (sel_m[0], sel_m[0])]
    bads = [(sel_f[1], sel_m[1]), (sel_f[2], sel_m[2])]

    divs = [
        create_div(divname='test1', expname='GT', fname_pair=goods[0],
                   dirname_pair=('tests_f', 'tests_f')),
        create_div(divname='test2', expname='GT', fname_pair=goods[1],
                   dirname_pair=('tests_m', 'tests_m')),
        create_div(divname='test3', expname='bad', fname_pair=bads[0],
                   dirname_pair=('tests_f', 'tests_m')),
        create_div(divname='test4', expname='bad', fname_pair=bads[1],
                   dirname_pair=('tests_f', 'tests_m'))
    ]
    return divs


def create_sim_question(expname):

    divs = create_tests()

    for i in range(10):
        divs.append(create_div(divname='real'+str(i),
                               expname=expname,
                               fname_pair=('unknown_vc', 'unknown_t'),
                               dirname_pair=(expname, 'originals')))

    np.random.shuffle(divs)

    real_fns = ""
    for fn in os.listdir('audio_files/' + expname):
        real_fns += fn + ","
    real_fns = real_fns[:-1]
    original_fns = ""
    for fn in os.listdir('audio_files/originals'):
        original_fns += fn + ","
    original_fns = original_fns[:-1]
    hidden_div = filenames_div.format(real_fns=real_fns,
                                      original_fns=original_fns)

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

    q = create_sim_question(args.expname)
    with open("gen_sim_mturk.html", "w") as fp:
        fp.write(q)




