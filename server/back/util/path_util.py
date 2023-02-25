from util.config_util import CONFIG

def model_path(model_name):
    return f'{CONFIG.path.modelPath}/{model_name}/weights/best.pt'

def dataset_path(dataset_name):
    return f'{CONFIG.path.datasetPath}/{dataset_name}'

def input_path(input_name):
    return f'{CONFIG.path.inputPath}/{input_name}'

def output_path(output_name):
    return f'{CONFIG.path.outputPath}/{output_name}'