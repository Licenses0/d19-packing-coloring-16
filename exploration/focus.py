import concurrent.futures as cf,subprocess,os
from pathlib import Path
nums=[192,144,96,152,168,120,184,216,232,288,72,104,128,136,160,176,200,208,224,240,248,264,272,280,296,304,312,320,328,336,344,352,360,384]
jobs=[(n,16,0,j,650000) for j in range(4,25) for n in nums]
def run(args):
 if any(Path('tmp').glob('win_*_16_*.txt')): return
 with open('tmp/focuslog','a') as f:subprocess.run(['tmp/hunt',*map(str,args)],stderr=f)
with cf.ThreadPoolExecutor(5) as ex:list(ex.map(run,jobs))
