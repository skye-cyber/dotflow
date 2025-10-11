from .pythonic import PythonicAPI


# Mixin for DotInterpreter
class PythonicAPIMixin:
    """Mixin to add Pythonic API methods to DotInterpreter."""

    @property
    def py(self) -> PythonicAPI:
        """Access Pythonic API methods."""
        return PythonicAPI(self)
