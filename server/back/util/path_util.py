from util.config_util import CONFIG

def model_path(model_name):
    return f'{CONFIG.path.modelPath}/{model_name}/weights/best.pt'

def dataset_path(dataset_name):
    return f'{CONFIG.path.datasetPath}/{dataset_name}'

def targetset_path(targetset_name):
    return f'{CONFIG.path.targetsetPath}/{targetset_name}'

def input_image_path(input_name):
    return f'{CONFIG.path.inputPath}/images/{input_name}'

def input_video_path(input_name):
    return f'{CONFIG.path.inputPath}/videos/{input_name}'

def output_image_path(output_name):
    return f'{CONFIG.path.outputPath}/images/{output_name}'

def output_video_path(output_name):
    return f'{CONFIG.path.outputPath}/videos/{output_name}'