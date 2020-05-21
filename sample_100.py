import os
import random
import shutil

# blow_baseline_path = '/Users/floraxue/adaptive-tts/blow-syn/blow_baseline/ckpt_200426/'
# blow_mel_path = '/Users/floraxue/adaptive-tts/blow-syn/blow_200331_test/syn_manual/ckpt_60000'

# all_fns = []
# for filename in os.listdir(blow_baseline_path):
# 	all_fns.append(filename)

# subset = random.sample(all_fns, 100)

# new_blow_baseline_dir = 'audio_files/blow_baseline'
# new_blow_mel_dir = 'audio_files/blow_mel'
# os.makedirs(new_blow_baseline_dir, exist_ok=True)
# os.makedirs(new_blow_mel_dir, exist_ok=True)

# for fn in subset:
# 	print(fn)
# 	src = os.path.join(blow_baseline_path, fn)
# 	dst = os.path.join(new_blow_baseline_dir, fn)
# 	shutil.copyfile(src, dst)

# 	src = os.path.join(blow_mel_path, fn)
# 	dst = os.path.join(new_blow_mel_dir, fn)
# 	shutil.copyfile(src, dst)

# print("Done")


new_blow_baseline_dir = '/Users/floraxue/ondevicetrain/testMOS/audio_files/blow_baseline'
new_blow_wg_dir = '/Users/floraxue/ondevicetrain/testMOS/audio_files/blow_wg'
blow_wg_dir = '/Users/floraxue/adaptive-tts/blow-syn/blow_200331_test/syn_manual/ckpt_60000_wg_out'
os.makedirs(new_blow_wg_dir, exist_ok=True)

subset = []
for fn in os.listdir(new_blow_baseline_dir):
	subset.append(fn)

for fn in subset:
	src = os.path.join(blow_wg_dir, fn)
	dst = os.path.join(new_blow_wg_dir, fn)
	shutil.copyfile(src, dst)

