import os
import gdown

def setup_repository():
    # Downloading, extracting models.
    models_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'models')
    os.makedirs(models_path, exist_ok=True)
    models_archive_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models.zip')
    gdown.extractall(path=models_archive_path, to=models_path)
    os.remove(models_archive_path)

    # Setting up the data folder with runtime_config.ini file
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'data')
    os.makedirs(data_path, exist_ok=True)
    runtime_config_path = os.path.join(data_path, 'runtime_config.ini')
    if os.path.exists(runtime_config_path):
        os.remove(runtime_config_path)
    pfile = open(runtime_config_path, 'w')
    pfile.write("[Predictions]\n")
    pfile.write("non_overlapping=true\n")
    pfile.write("reconstruction_method=probabilities #probabilities, thresholding\n")
    pfile.write("reconstruction_order=resample_first #resample_first, resample_second\n")
    pfile.write("probability_threshold=0.4\n")
    pfile.close()


setup_repository()

