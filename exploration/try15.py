import concurrent.futures as cf,subprocess
from pathlib import Path
def run(args):
 if list(Path('tmp').glob('win_*_15_*.txt')):return
 with open('tmp/15log','a') as f:subprocess.run(['tmp/hunt',*map(str,args)],stderr=f)
with cf.ThreadPoolExecutor(3) as ex:
 list(ex.map(run,[(n,15,m,j,250000) for j in (31,32,33) for n in (128,144,160,168,180,192,208,224,240) for m in (0,1,2,3,4) if n%[8,8,2,9,1][m]==0]))
