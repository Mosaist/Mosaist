# %%
import sys

sys.path.append('../image_handling')
from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *
from model_stuffs import *

dataset_name = 'cup2'

# %%
video_to_dataset(f'{dataset_name}.mp4', dataset_name)

# %%
train_images(dataset_name)

# %%
