from importlib.abc import MetaPathFinder
from importlib import util
import subprocess
import sys


class PipFinder(MetaPathFinder):

    def find_spec(self, fullname, path, target=None):
        print(f"Module {self} not installed.  Attempting to pip install")
        cmd = f"{sys.executable} -m pip install {self}"
        try:
            subprocess.run(cmd.split(), check=True)
        except subprocess.CalledProcessError:
            return None

        return util.find_spec(self)


if __name__ == "__main__":
    sys.meta_path.append(PipFinder)


import numba as nb
    
def listify(x):
    return [x]


def draw_histogram(data):
    plt.hist(data)



