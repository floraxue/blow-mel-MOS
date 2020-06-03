import os
import shutil


ori_dir = '/Users/floraxue/adaptive-tts/blow-syn/targets_2'

os.makedirs('audio_files/targets_gt1', exist_ok=True)
os.makedirs('audio_files/targets_gt2', exist_ok=True)

person_to_fn = {}
for fn in os.listdir(ori_dir):
	person = fn.split('_')[0]
	if person not in person_to_fn:
		person_to_fn[person] = []
	person_to_fn[person].append(fn)


for person, filenames in person_to_fn.items():
	fn = filenames[0]
	src = os.path.join(ori_dir, fn)
	dst = os.path.join('audio_files/targets_gt1', person + '.wav')
	shutil.move(src, dst)

	fn = filenames[1]
	src = os.path.join(ori_dir, fn)
	dst = os.path.join('audio_files/targets_gt2', person + '.wav')
	shutil.move(src, dst)


