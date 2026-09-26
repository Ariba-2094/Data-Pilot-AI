from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
files=sorted(Path('work').glob('page-*.png'))
for batch in range(3):
 canvas=Image.new('RGB',(1420,2000),'#d9e0e4')
 for j,p in enumerate(files[batch*4:batch*4+4]):
  im=Image.open(p);im.thumbnail((700,990));canvas.paste(im,((j%2)*710,(j//2)*1000))
 canvas.save(f'work/review-{batch}.png')
