# music A + the same two bars (20.0–24.0 s) repeated at 24.0 s → 4 s longer, seamless on the bar line
import sys,numpy as np,soundfile as sf,librosa
y,sr=librosa.load(sys.argv[1],sr=44100,mono=False)
y=np.atleast_2d(y);a,b,c=int(20*sr),int(24*sr),int(24*sr);xf=int(.012*sr)
head,loop,tail=y[:,:c],y[:,a:b].copy(),y[:,c:]
r=np.linspace(0,1,xf)
def join(p,q):
    o=p[:,-xf:]*(1-r)+q[:,:xf]*r;return np.concatenate([p[:,:-xf],o,q[:,xf:]],axis=1)
out=join(join(head,loop),tail)
sf.write(sys.argv[2],out.T,sr);print(out.shape[1]/sr)
