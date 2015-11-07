# -*- coding:utf8 -*-
"""deck2pdf capturing engine by Shost.py

"""
from . import CaptureEngine as AbstractEngine
import os
import logging
from ghost import Ghost


Logger = logging.getLogger(__file__)


class CaptureEngine(AbstractEngine):
    def start(self):
        super(CaptureEngine, self).start()
        self._ghost = Ghost()
        self._session = self._ghost.start()
        self._session.set_viewport_size(1135, 740)

    def end(self):
        self._session.exit()

    def _calc_slide_num(self):
        self._session.open(self._url)
        return int(self._session.evaluate('slidedeck.slides.length')[0])

    def capture_page(self, slide_idx, is_last=False):
        FILENAME = os.path.join(self.save_dir, "screen_{}.png".format(slide_idx))
        curSlide = int(self._session.evaluate('slidedeck.curSlide_')[0])
        if is_last:
            self._session.open('{}#{}'.format(self._url, slide_idx+1))
        else:
            while slide_idx >= curSlide:
                self._session.evaluate('slidedeck.nextSlide();')
                curSlide = int(self._session.evaluate('slidedeck.curSlide_')[0])
                Logger.debug(slide_idx, curSlide)
            self._session.evaluate('slidedeck.prevSlide();')
        # Get Screen Shot
        self._session.sleep(2)
        self._session.capture_to(FILENAME)
        self._slide_captures.append(FILENAME)

    def capture_all(self):
        self.start()
        slides = self._calc_slide_num()
        Logger.debug('{} slides'.format(slides))
        self._session.evaluate('for (var idx = slidedeck.curSlide_; idx > 0; idx--) { slidedeck.prevSlide();}')

        for slide_idx in range(slides):
            is_last = (slide_idx == slides - 1)
            self.capture_page(slide_idx, is_last)
        self.end()
