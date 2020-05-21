import shutil
import os


blow_wg_path = '/Users/floraxue/adaptive-tts/blow-syn/blow_200331_test/syn_manual/ckpt_60000_wg_out'

for filename in os.listdir(blow_wg_path):
    dst_fn = filename.split('mel')[0]
    dst_fn = dst_fn[:-1]
    dst_fn = dst_fn + '.wav'
    dst = os.path.join(blow_wg_path, dst_fn)
    src = os.path.join(blow_wg_path, filename)
    shutil.move(src, dst)

