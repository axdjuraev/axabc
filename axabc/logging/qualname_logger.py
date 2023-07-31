import os
import logging
import inspect


class QualNameLogger(logging.Logger):
    def __init__(self, name: str, level = 0, base_path=...) -> None:
        super().__init__(name, level)

        if base_path is ...:
            frame = self._get_init_frame()
            base_path = os.path.dirname(frame.f_code.co_filename) if frame else None

        self.base_path = base_path

    def _get_init_frame(self):
        frame = inspect.currentframe()

        while frame and 'self' in frame.f_locals and frame.f_locals['self'] is self:
            frame = frame.f_back

        return frame

    def _get_entity(self, frame):
        entity = frame.f_globals.get(frame.f_code.co_name)
        return entity

    def get_qualname(self):
        frame = self._get_init_frame()

        if not frame:
            return '__main__'

        entity = self._get_entity(frame)

        filename = frame.f_code.co_filename
        if self.base_path:
            filename = os.path.relpath(filename, self.base_path)

        if not entity:
            return f"{filename}"

        qualname = entity.__qualname__

        return f"{filename}:{qualname}:{frame.f_code.co_firstlineno}"

    def _log(self, level, msg, args, **kwargs):
        qualname = self.get_qualname()
        msg = f'({qualname}): {msg}'

        return super()._log(level, msg, args, **kwargs)
