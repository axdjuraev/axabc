import os
import logging
import inspect


class QualNameLogger(logging.Logger):
    def __init__(self, name: str, level = 0, base_path=...) -> None:
        super().__init__(name, level)

        if base_path is ...:
            frame = self._get_frame()
            base_path = os.path.dirname(frame.f_code.co_filename) if frame else None

        self.base_path = base_path

    def _get_frame(self, back_size = 0):
        # Get the current frame (frame of the current function)
        back_size = back_size + 2  # minimum back_size
        frame = inspect.currentframe()

        # Go back one frame to get the calling function frame
        for _ in range(back_size):
            if frame is None:
                return

            frame = frame.f_back

        # Get the calling function object from the frame
        return frame

    def _get_entity(self, frame):
        entity = frame.f_globals.get(frame.f_code.co_name)
        return entity


    def get_qualname(self, back_frame_size=1):
        frame = self._get_frame(back_frame_size + 1)  # 1 for including itself func

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

    def _log(self, level, msg, args, *, back_frame_size=1, **kwargs):
        qualname = self.get_qualname(back_frame_size)
        msg = f'({qualname}): {msg}'

        return super()._log(level, msg, args, **kwargs)
