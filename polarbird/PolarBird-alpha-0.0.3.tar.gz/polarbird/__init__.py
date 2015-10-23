import curses

from polarbird.polarbird import PolarBird

@curses.wrapper
def start_app(screen):
    pl = PolarBird(screen)
    pl.start_app()
