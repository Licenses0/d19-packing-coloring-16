#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 int n=stoi(argv[1]), K=stoi(argv[2]), mode=stoi(argv[3]), seed=stoi(argv[4]), iters=stoi(argv[5]);
 mt19937 rng(seed); string p=vector<string>{"####....","##.#..#.","#.","####.....","."}[mode]; if(n%p.size())return 1;
 vector<int> pos,ind(n,-1); int lo=mode==4?2:4;
 for(int i=0;i<n;i++)if(p[i%p.size()]=='.'){ind[i]=pos.size();pos.push_back(i);}
 int N=pos.size(), W=K+1;
 vector<vector<int>>nb(N*W);vector<int> bans(W);
 for(int c=lo;c<=K;c++){
  vector<bool> diff(n);for(int a=-c;a<=c;a++)for(int b=abs(a)-c;b<=c-abs(a);b++){
  int s=a+9*b;if(s>0 && s%2==0){diff[(s/2)%n]=diff[(n-(s/2)%n)%n]=true;}}
  bans[c]=diff[0];
  for(int i=0;i<N;i++)for(int j=0;j<N;j++)if(i!=j && diff[(n+pos[i]-pos[j])%n])nb[i*W+c].push_back(j);
 }
 vector<int> col(N),count(N*W),tabu(N*W);
 auto assign=[&](int i,int c){for(int j:nb[i*W+col[i]])count[j*W+col[i]]--;col[i]=c;for(int j:nb[i*W+c])count[j*W+c]++;};
 int rec=10000,great=10000,last=0; vector<int> best;
 for(int i=0;i<N;i++)assign(i,lo+rng()%(W-lo));
 for(int step=0;step<iters;step++){
  int bad=0,ci=-1,cc=0,mi=999,num=0;
  for(int i=0;i<N;i++)bad+=count[i*W+col[i]];bad/=2;
  if(bad<rec){rec=bad;last=step;best=col;if(bad<great){great=bad;if(bad<=4)cerr<<n<<" "<<K<<" "<<mode<<" "<<seed<<" "<<step<<" "<<bad<<"\n";}if(!bad){
   ofstream out("tmp/win_"+to_string(n)+"_"+to_string(K)+"_"+to_string(mode)+"_"+to_string(seed)+".txt");
   for(int i=0;i<n;i++)out<<(ind[i]<0?0:col[ind[i]])<<" ";out<<"\n";return 0;}}
  if(step-last>1600+N*3){for(int i=0;i<N;i++)assign(i,best[i]);for(int j=0;j<2+int(rng()%(N/12+1));j++)assign(rng()%N,lo+rng()%(W-lo)); last=step;
   if(rng()%7==0)rec=9999;
   continue;}
  for(int i=0;i<N;i++){int old=count[i*W+col[i]];if(!old)continue;
   for(int c=lo;c<=K;c++){if(c==col[i]||bans[c])continue;int d=count[i*W+c]-old;
   if(tabu[i*W+c]>step && d+bad>=rec)continue;
   if(d<mi){mi=d;ci=i;cc=c;num=1;}else if(d==mi && !((rng())%(++num))){ci=i;cc=c;}}}
  if(ci<0)continue;
  tabu[ci*W+col[ci]]=step+4+rng()%9+min(20,bad/4);
  assign(ci,cc);
 }
 cerr<<"end "<<n<<" "<<K<<" "<<mode<<" "<<seed<<" "<<great<<"\n";
}
