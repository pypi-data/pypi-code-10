import click
from mh_cli import cli

from selenium.common.exceptions import TimeoutException
from common import pass_state, init_driver, selenium_options
from mh_pages.pages import RecordingsPage, \
    AdminPage, \
    TrimPage, \
    UploadPage

__all__ = ['upload', 'trim']

@cli.command()
@click.option('--presenter', help="Presenter video")
@click.option('--presentation', help="Presentation video")
@click.option('--combined', help="Combined presenter/presentation video")
@click.option('--series', help="Series title. Should match an existing series.")
@click.option('--title', default='mh-ui-testing upload', help="Recording title")
@click.option('-i', '--inbox', is_flag=True, help="Use a MH inbox media file")
@click.option('--live_stream', is_flag=True)
@selenium_options
@pass_state
@init_driver('/admin')
def upload(state, presenter, presentation, combined, series, title, inbox, live_stream):
    """Upload a recording from a local path or the inbox"""

    page = RecordingsPage(state.driver)
    page.upload_recording_button.click()

    page = UploadPage(state.driver)

    page.enter_text(page.title_input, title)
    page.enter_text(page.type_input, "L01")

    if series is not None:
        page.set_series(series)

    page.set_upload_files(presenter=presenter,
                          presentation=presentation,
                          combined=combined,
                          is_inbox=inbox)
    page.workflow_select.select_by_value('DCE-production')
    page.set_live_stream(live_stream)
    page.set_multitrack(combined is not None)
    page.upload_button.click()
    page.wait_for_upload_finish()

@cli.command()
@click.option('-f', '--filter')
@click.option('-c', '--count', type=int, default=None)
@selenium_options
@pass_state
@init_driver('/admin')
def trim(state, filter=None, count=None):
    """Execute trims on existing recording(s)"""

    page = AdminPage(state.driver)
    page.recordings_tab.click()
    page = RecordingsPage(state.driver)
    page.max_per_page()
    page.switch_to_tab(page.on_hold_tab)

    if filter is not None:
        field, value = filter.split(':', 1)
        page.filter_recordings(field, value)

    link_idx = 0
    while True:

        # kinda annoying that we have to do this each time
        page.refresh_off()

        try:
            # re-resolve the trim link elements each time because the refs go
            # stale when the page reloads
            # also, iterate via incrementing idx so that we don't somehow trim
            # the same thing > once (e.g. the entry doesn't get removed from
            # the table because the workflow hasn't actually resumed)
            link = page.trim_links[link_idx]
        except (TimeoutException,IndexError):
            break

        href = link.get_attribute('href')
        scheme, js = href.split(':', 1)
        page.js(js)
        page.switch_frame(page.trim_iframe)
        page = TrimPage(state.driver)
        page.trim()
        page.default_frame()
        page.reload()
        page = RecordingsPage(state.driver)

        if count is not None:
            count -= 1
            if count == 0:
                break

