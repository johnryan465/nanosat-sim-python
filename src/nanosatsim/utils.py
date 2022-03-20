import orekit
from orekit.pyhelpers import setup_orekit_curdir


def initial_orekit():
    vm = orekit.initVM()  # type: ignore
    setup_orekit_curdir(filename="resources/orekit-data")
