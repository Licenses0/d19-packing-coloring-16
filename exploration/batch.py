import concurrent.futures as cf,subprocess
jobs=[(n,k,mode,j,200000) for j in range(1,4) for n in (144,160,168,180,192,216,240,128,120,224,256) for k in (16,17) for mode in (0,1,2,3,4) if n%[8,8,2,9,1][mode]==0]
def run(args):
 with open('tmp/huntlog','a') as f:subprocess.run(['tmp/hunt',*map(str,args)],stderr=f)
with cf.ThreadPoolExecutor(4) as ex:list(ex.map(run,jobs))
