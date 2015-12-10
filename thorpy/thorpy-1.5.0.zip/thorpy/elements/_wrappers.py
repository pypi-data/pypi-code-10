from thorpy.elements.element import Element
from thorpy.elements.clickable import Clickable
from thorpy.elements.ghost import Ghost
from thorpy.elements.box import Box
from thorpy.miscgui.storage import store
from thorpy.miscgui import constants, style, functions
from thorpy.painting.painters.imageframe import ButtonImage

def make_alert(text, font_size=style.FONT_SIZE, font_color=style.FONT_COLOR,
                ok_text="Ok"):
    from thorpy.miscgui.launchers.launcher import make_ok_box
    e_text = make_text(text, font_size, font_color)
    box = make_ok_box([e_text], ok_text=ok_text)
    return box

def launch_blocking_alert(text, parent=None, font_size=style.FONT_SIZE,
                            font_color=style.FONT_COLOR, ok_text="Ok"):
    box_alert = make_alert(text, font_size, font_color, ok_text)
    box_alert.center()
    from thorpy.menus.tickedmenu import TickedMenu
    m = TickedMenu(box_alert)
    box_alert.get_elements_by_text(ok_text)[0].user_func = functions.quit_menu_func
    box_alert.get_elements_by_text(ok_text)[0].user_params = {}
    m.play()
    box_alert.unblit()
    if parent:
        parent.partial_blit(None, box_alert.get_fus_rect())
        box_alert.update()

def launch_alert(text, font_size=style.FONT_SIZE, font_color=style.FONT_COLOR,
                ok_text="Ok"):
    from thorpy.miscgui.launchers.launcher import launch
    box_alert = make_alert(text, font_size, font_color, ok_text)
    box_alert.center()
    launch(box_alert)

def launch_choices(text, choices, title_fontsize=style.FONT_SIZE,
                    title_fontcolor=style.FONT_COLOR):
    """choices are tuple (text,func)"""
    elements = [make_button(t,f) for t,f in choices]
    ghost = make_stored_ghost(elements)
    e_text = make_text(text, title_fontsize, title_fontcolor)
    box = Box.make([e_text, ghost])
    box.center()
    from thorpy.miscgui.launchers.launcher import launch
    from thorpy.miscgui.reaction import ConstantReaction
    launcher = launch(box)
    for e in elements:
        reac = ConstantReaction(constants.THORPY_EVENT,
                                launcher.unlaunch,
                                {"id":constants.EVENT_UNPRESS,
                                 "el":e})
        box.add_reaction(reac)
    return launcher

def launch_blocking_choices(text, choices, parent=None, title_fontsize=style.FONT_SIZE,
                    title_fontcolor=style.FONT_COLOR):
    """choices are tuple (text,func)"""
    elements = [make_button(t,f) for t,f in choices]
    ghost = make_stored_ghost(elements)
    e_text = make_text(text, title_fontsize, title_fontcolor)
    box = Box.make([e_text, ghost])
    box.center()
    from thorpy.miscgui.reaction import ConstantReaction
    for e in elements:
        reac = ConstantReaction(constants.THORPY_EVENT,
                                functions.quit_menu_func,
                                {"id":constants.EVENT_UNPRESS,
                                 "el":e})
        box.add_reaction(reac)
    from thorpy.menus.tickedmenu import TickedMenu
    m = TickedMenu(box)
    m.play()
    box.unblit()
    if parent:
        parent.partial_blit(None, box.get_fus_rect())
        box.update()

def make_stored_ghost(elements, mode="h"):
    ghost = Ghost(elements)
    ghost.finish()
    store(ghost, mode=mode)
    ghost.fit_children()
    return ghost


def make_button(text, func=None, params=None):
    button = Clickable(text)
    button.finish()
    button.scale_to_title()
    if func:
        button.user_func = func
    if params:
        button.user_params = params
    return button

def make_image_button(img_normal, img_pressed=None, img_hover=None,
                        alpha=255, colorkey=None, text=""):
    e = Clickable(text)
    painter = ButtonImage(img_normal, img_pressed, img_hover, alpha, colorkey)
    e.set_painter(painter)
    e.finish()
    return e

def make_text(text, font_size=style.FONT_SIZE, font_color=style.FONT_COLOR):
    params = {"font_color":font_color, "font_size":font_size}
    button = Element(text, normal_params=params)
    if not "\n" in text:
        button.set_style("text")
    button.finish()
    if "\n" in text:
        button.scale_to_title()
        button.set_main_color((0,0,0,0))
    return button
