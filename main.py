from scripts import video_renderer, frame_eraser, cropper
from data import data

#diversifier()

#done = video_renderer()
#if(done):
done = frame_eraser()
if(done):
    done = cropper()
print(done)
