import os
import shutil


ori_dir = 'audio_files/originals'

person_to_fn = {}
for fn in os.listdir(ori_dir):
	person = fn.split('_')[0]
	if person not in person_to_fn:
		person_to_fn[person] = []
	person_to_fn[person].append(fn)


for person, filenames in person_to_fn.items():
	fn = filenames[0]
	src = os.path.join(ori_dir, fn)
	dst = os.path.join(ori_dir, person + '.wav')
	shutil.move(src, dst)
	for fn in filenames[1:]:
		os.remove(os.path.join(ori_dir, fn))


