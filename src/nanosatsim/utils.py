import orekit
from orekit.pyhelpers import setup_orekit_curdir


def initial_orekit(filename="resources/orekit-data"):
    vm = orekit.initVM()  # type: ignore
    setup_orekit_curdir(filename=filename)
