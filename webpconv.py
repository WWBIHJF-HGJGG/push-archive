"""Convert a card to WebP at original pixel size. Picks the lowest quality in QS
whose SSIM (luma, 8x8 blocks) >= MIN_SSIM, defaulting to the highest."""
import io,numpy as np
from PIL import Image
QS=(82,85,88,90,92,95); MIN_SSIM=0.985
def _ssim(a,b):
    a=np.asarray(a.convert('L'),np.float64); b=np.asarray(b.convert('L'),np.float64)
    h,w=(a.shape[0]//8)*8,(a.shape[1]//8)*8
    a=a[:h,:w].reshape(h//8,8,w//8,8); b=b[:h,:w].reshape(h//8,8,w//8,8)
    ma,mb=a.mean((1,3)),b.mean((1,3)); va,vb=a.var((1,3)),b.var((1,3))
    cov=((a-ma[:,None,:,None])*(b-mb[:,None,:,None])).mean((1,3))
    c1,c2=(.01*255)**2,(.03*255)**2
    return float((((2*ma*mb+c1)*(2*cov+c2))/((ma**2+mb**2+c1)*(va+vb+c2))).mean())
def convert(src,dst):
    im=Image.open(src); im.load()
    im=im.convert('RGBA' if im.mode in('RGBA','LA','P') and 'A' in im.getbands() or im.mode=='P' else 'RGB')
    if im.mode=='RGBA' and im.getextrema()[3][0]==255: im=im.convert('RGB')
    best=None
    for q in QS:
        buf=io.BytesIO(); im.save(buf,'WEBP',quality=q,method=6,sharp_yuv=True)
        s=_ssim(im.convert('RGB'),Image.open(io.BytesIO(buf.getvalue())).convert('RGB'))
        best=(q,s,buf.getvalue())
        if s>=MIN_SSIM: break
    open(dst,'wb').write(best[2])
    return dict(w=im.width,h=im.height,q=best[0],ssim=round(best[1],4),bytes=len(best[2]))
