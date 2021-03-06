import os
import sys

from modules.exception.exceptions import InvalidOSException


## This class is responsible for communicating with the command line.
#
# It will call the os library and set the necessary environment variables.
# It furthermore checks if any paths are empty and replaces them with the default paths from the config file
# When everything is set, it will execute the labeling_module class
# the function which gets called from the controller
# @param path the path where the matrices should be loaded from, may be empty
# @param saving_name the path under which the labeled matrices should be saved, may be empty
# @param saving_path the name under which the labeled matrices should be saved, may be empty
# @throws InvalidOSException when run on a operating system other thant linux is used
def start(path, saving_name, saving_path):
    if not __is_linux():
        raise InvalidOSException("Labeling only works on linux with Ginkgo installed")
    os.environ['CXX'] = '/usr/local/bin/g++-6.4'
    os.environ['CC'] = '/usr/local/bin/gcc-6.4'
    os.environ['PATH'] = os.getenv("PATH", "fail") + ':/usr/local/cuda-9.0/bin/'
    os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/lib'
    os.environ['LD_LIBRARY_PATH'] = os.getenv("LD_LIBRARY_PATH", "fail") + ':/usr/local/lib'
    os.environ['LD_LIBRARY_PATH'] = os.getenv("LD_LIBRARY_PATH", "fail") + ':/usr/local/lib64'
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'

    os.system('python3.6 modules/model/labeling_module/labeling_module.py ' + path + " " + saving_name +
              " " + saving_path)


def __is_linux() -> bool:
    return str(sys.platform) == 'linux'
