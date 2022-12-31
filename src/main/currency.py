

class CurrencyManager:
    DEFAULT_POINTS = 10
    DEFAULT_RESEARCH = 0
    def __init__(self, camera) -> None:
        self.game = camera.game
        self.camera = camera
        self._points = self.DEFAULT_POINTS
        self._research = self.DEFAULT_RESEARCH
        self.stats_menu = camera.stats

    @property
    def points(self) -> float|int:
        return self._points
    @points.setter
    def points(self, points):
        self._points = points
        self.stats_menu.actualise_text()

    @property
    def research(self) -> float|int:
        return self._research
    @research.setter
    def research(self, research):
        self._research = research
        self.stats_menu.actualise_text()

    @property
    def dpoints(self) -> int:
        return int(self._points)
    @property
    def dresearch(self) -> int:
        return int(self._research)
