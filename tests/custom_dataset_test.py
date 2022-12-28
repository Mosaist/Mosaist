# %%
import sys

sys.path.append('../image_handling')
from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *
from model_stuffs import *

# %%
video_to_dataset('face.mp4', 'face')

# %%
train_images('face')

# %%
