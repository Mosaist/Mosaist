import os

import cv2
import ffmpeg

import util.path_util as path_util

def save_from_file(file):
    file_name = file.filename
    file_path = path_util.input_video_path(file_name)
    file.save(file_path)

    return file_path

def get_images(video):
    success, image = video.read()

    while success:
        success, image = video.read()
        if not success:
            break

        yield image

def get_size(video):
    major_ver, _, _ = (cv2.__version__).split('.')
 
    if int(major_ver) < 3 :
        return tuple(map(int, (
            video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH),
            video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        )))
    else:
        return tuple(map(int, (
            video.get(cv2.CAP_PROP_FRAME_WIDTH),
            video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )))

def get_fps(video):
    major_ver, _, _ = (cv2.__version__).split('.')
 
    if int(major_ver) < 3 :
        return video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        return video.get(cv2.CAP_PROP_FPS)

def get_frame_count(video):
    major_ver, _, _ = (cv2.__version__).split('.')
 
    if int(major_ver) < 3 :
        return int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    else:
        return int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
def to_h264(video_name):
    input_path = path_util.input_video_path(video_name)
    output_path = path_util.output_video_path(video_name)

    os.rename(output_path, f'{output_path}.temp')
    video_track = ffmpeg.input(f'{output_path}.temp')
    audio_track = ffmpeg.input(input_path).audio

    try:
        ffmpeg.output(video_track, audio_track, output_path, vcodec='libx264').run()
    except:
        print(f'[H264 Encoding] {video_name} doesn\'t contain audio track.')
        ffmpeg.output(video_track, output_path, vcodec='libx264').run()

    os.remove(f'{output_path}.temp')