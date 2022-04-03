
from abc import ABC, abstractmethod
import orekit
from org.orekit.frames import FramesFactory
from org.orekit.frames import Frame as _Frame
from org.orekit.utils import IERSConventions


class Frame(_Frame):
    pass


class Frames(ABC):
    # @abstractmethod
    def getITRF(self) -> Frame:
        return FramesFactory.getITRF(IERSConventions.IERS_2010, True)

    def getEME2000(self):
        return FramesFactory.getEME2000()
