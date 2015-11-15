#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# (c) 2005-2011, Marcin Kasperski
######################################################################
import re
from twisted.trial import unittest
from mekk.fics.constants import block_codes
from mekk.fics.datatypes import style12
from mekk.fics.datatypes.generic import GenericText
from mekk.fics.datatypes.color import Color, BLACK, WHITE
from mekk.fics.datatypes.date import FicsDateInfo
from mekk.fics.datatypes.game_clock import GameClock
from mekk.fics.datatypes.game_info import GameReference, ExaminedGame, SetupGame, PlayedGame, GameSpec, GameInfo, ExaminedGameExt
from mekk.fics.datatypes.game_type import GameType
from mekk.fics.datatypes.list_items import ListContents
from mekk.fics.datatypes.notifications import  SeekRef, GameJoinInfo, Seek
from mekk.fics.datatypes.player import PlayerName, FingerInfo, ResultStats, PlayerRating
from mekk.fics.datatypes.channel import ChannelRef
from mekk.fics.parsing import info_parser
from mekk.fics.parsing.reply.block_mode_filter import BlockModeFilter
from mekk.fics.parsing.reply.finger import parse_finger_reply
from mekk.fics.parsing.reply.games import parse_games_reply_line
from mekk.fics.parsing.reply.who import parse_who_reply
from mekk.fics.parsing.reply.list_operations import parse_showlist_reply
from mekk.fics.parsing.reply.observe import parse_observe_reply, parse_unobserve_reply
from mekk.fics.parsing.reply_parser import parse_fics_reply
from mekk.fics.test_utils import load_tstdata_file, assert_dicts_equal, assert_tables_equal
from mekk.fics import errors
import datetime
from decimal import Decimal

# Proper SkipTest depends on whether we run under trial, or under nose. Let's hack it
import sys
if sys.argv[0].endswith("trial"):
    from twisted.trial.unittest import SkipTest as TrialSkipTest
    SkipTest = TrialSkipTest
else:
    from nose import SkipTest as NoseSkipTest
    SkipTest = NoseSkipTest

FICS_PARSE_DATA_DIR = "ficsparserdata"

def load_parse_data_file(name):
    return load_tstdata_file(FICS_PARSE_DATA_DIR, name)

def load_parse_data_file_patching_continuations(name):
    data = load_parse_data_file(name)
    # Usually \-lines are joined by BlockFilter or disabled by nowrap.
    # In tests where we don't use any of those, but utilize console grabs,
    # it is necessary to manually patch the data in the same way.
    return re.sub(r'\s?\n\\ *', ' ', data)


#noinspection PyTypeChecker
class ParseFicsLineTestCase(unittest.TestCase):
    def testTell(self):
        (w,d) = info_parser.parse_fics_line("Johny tells you: blah blah")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Johny'))
        self.failUnlessEqual(d.text, 'blah blah')
    def testTellTD(self):
        (w,d) = info_parser.parse_fics_line("Mamer(TD) tells you: bleh bleh")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Mamer'))
        self.failUnlessEqual(d.text, 'bleh bleh')
    def testTellSRTM(self):
        (w,d) = info_parser.parse_fics_line("Johny(SR)(TM) tells you: blah blah")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Johny'))
        self.failUnlessEqual(d.text, 'blah blah')
    def testDoubleTell(self):
        # see #2
        (w,d) = info_parser.parse_fics_line("Johny tells you: tell WatchBot blah blah")
        self.failUnlessEqual(w, 'tell')
        self.failUnlessEqual(d.player, PlayerName('Johny'))
        self.failUnlessEqual(d.text, 'blah blah')
    def testChannelTell(self):
        (w,d) = info_parser.parse_fics_line("playerbis(106): ble ble ble")
        self.failUnlessEqual(w, 'channel_tell')
        self.failUnlessEqual(d.player, PlayerName('playerbis'))
        self.failUnlessEqual(d.channel, 106)
        self.failUnlessEqual(d.text, 'ble ble ble')
    def testChannelTellGuest(self):
        (w,d) = info_parser.parse_fics_line("GuestKKLX(U)(4): your extremely lucky i just slipped my piece there")
        self.failUnlessEqual(w, 'channel_tell')
        self.failUnlessEqual(d.player, PlayerName('GuestKKLX'))
        self.failUnlessEqual(d.channel, 4)
        self.failUnlessEqual(d.text, 'your extremely lucky i just slipped my piece there')
    def testItShout(self):
        (w,d) = info_parser.parse_fics_line("--> MAd> (ics-auto-salutes 'Mekk)")
        self.failUnlessEqual(w, 'it_shout')
        self.failUnlessEqual(d.player, PlayerName('Mad'))
        self.failUnlessEqual(d.text, "MAd> (ics-auto-salutes 'Mekk)")
    def testItShout2(self):
        (w,d) = info_parser.parse_fics_line(
            "--> botchvinik Announcement!!!!  /\/\/\/\/\/\  RJJ /\/\/\/\/\/\ has arrived! !BCS->(gong)")
        self.failUnlessEqual(w, 'it_shout')
        self.failUnlessEqual(d.player, PlayerName('botchvinik'))
        self.failUnlessEqual(d.text, "botchvinik Announcement!!!!  /\/\/\/\/\/\  RJJ /\/\/\/\/\/\ has arrived! !BCS->(gong)")
    def testItShout3(self):
        (w,d) = info_parser.parse_fics_line("--> Mekk manually salutes MAd.")
        self.failUnlessEqual(w, 'it_shout')
        self.failUnlessEqual(d.player, PlayerName('Mekk'))
        self.failUnlessEqual(d.text, "Mekk manually salutes MAd.")
    def testCShout(self):
        (w,d) = info_parser.parse_fics_line("TScheduleBot(TD) c-shouts: Thursday's Scheduled 15 0 SS scheduled tournament. See 'finger TScheduleBot' for more information about this and other scheduled events on FICS.")
        self.failUnlessEqual(w, 'cshout')
        self.failUnlessEqual(d.player, PlayerName('TScheduleBot'))
        self.failUnlessEqual(d.text, "Thursday's Scheduled 15 0 SS scheduled tournament. See 'finger TScheduleBot' for more information about this and other scheduled events on FICS.")
    def testShout(self):
        (w,d) = info_parser.parse_fics_line("Georg(SR)(TM) shouts: To be or not to be")
        self.failUnlessEqual(w, 'shout')
        self.failUnlessEqual(d.player, PlayerName('Georg'))
        self.failUnlessEqual(d.text, "To be or not to be")
    def testStyle12(self):
        (w,d) = info_parser.parse_fics_line("<12> -----r-- --r-p-kp ----Qnp- ----p--- -------- -----PP- P-q---BP ---R-R-K B -1 0 0 0 0 0 164 CamyC android 0 3 0 26 26 112 107 24 Q/a6-e6 (0:01) Qxe6 0 1 215")
        self.failUnlessEqual(w, 'game_move')
        s12 = d.style12
        self.failUnless( isinstance(s12, style12.Style12) )
        #self.failUnlessEqual( s12.FEN(),
    def testQtellTShout1(self):
        (w, d) = info_parser.parse_fics_line(':AGree(TM) t-shouts: Come on! 1 more player for 3 0 tourney and we start: "mam j 24"')
        self.failUnlessEqual(w, "qtell")
        self.failUnlessEqual(d, 'AGree(TM) t-shouts: Come on! 1 more player for 3 0 tourney and we start: "mam j 24"')
        # TODO: think about recognizing this type of qtells
    def testQtellTShout2(self):
        (w, d) = info_parser.parse_fics_line(':mamer(TD) t-shouts: 1 0 r DRR tourney: "tell mamer JoinTourney 19" to join.')
        self.failUnlessEqual(w, "qtell")
        self.failUnlessEqual(d, 'mamer(TD) t-shouts: 1 0 r DRR tourney: "tell mamer JoinTourney 19" to join.')
    def testQtellNormal(self):
        (w, d) = info_parser.parse_fics_line(':Blah blah blah')
        self.failUnlessEqual(w, "qtell")
        self.failUnlessEqual(d, "Blah blah blah")
    def testCompressedMove(self):
        # TODO: more examples of http://www.freechess.org/Help/HelpFiles/iv_compressmove.html
        (w,d) = info_parser.parse_fics_line("<d1> 2 64 Rxc2 e2c2p 1200 203800")
        self.failUnlessEqual(w, 'compressed_move')
        self.failUnlessEqual(d.game_no, 2)
        self.failUnlessEqual(d.half_moves_count, 64)
        self.failUnlessEqual(d.algebraic, 'Rxc2')
        self.failUnlessEqual(d.time_taken, datetime.timedelta(microseconds=1200*1000))
        self.failUnlessEqual(d.time_left, datetime.timedelta(microseconds=203800*1000))
        # TODO: rozpakowac smith move (to jest czteroliterowe skąd-dokąd a potem
        # - opcjonalna dodatkowa literka: pnbrqkEcC (pnbrqk - zbito podaną bierkę,
        #    E - zbito en-passant, c - krótka roszada, C - długa roszada)
        # - opcjonalna literka "promoted to" ( NBRQ)
        # patrz https://www.chessclub.com/chessviewer/smith.html
        self.failUnlessEqual(d.smith, 'e2c2p')
        #self.failUnlessEqual(d.src_square, 'e2')
        #self.failUnlessEqual(d.dst_square, 'c2')
        #self.failUnlessEqual(d.captured, Piece(color=Color('white'), name='pawn'))
        #self.failUnlessEqual(d.en_passant, False)
        #self.failUnlessEqual(d.castling, None)
        # TODO: testy z różnymi smithami
    def testGameStartedIvGameInfo(self):
        (w,d) = info_parser.parse_fics_line('<g1> 1 p=0 t=blitz r=1 u=1,1 it=5,6 i=8,9 pt=0 rt=1586E,2100  ts=1,0')
        # TODO: name (it shows up when game starts or is observed)
        self.failUnlessEqual(w, 'game_joined') # TODO: or maybe game_started_iv ???
        self.failUnlessIsInstance(d, GameJoinInfo)
        self.failUnlessEqual(d.game_no, 1)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.is_rated, True)
        # TODO
        #self.failUnlessEqual(d.white_registered, True)
        #self.failUnlessEqual(d.black_registered, True)
        # TODO
        #self.failUnlessEqual(d.white_clock, GameClock(5,8))
        #self.failUnlessEqual(d.black_clock, GameClock(6,9))
        # TODO
        #self.failUnlessEqual(d.partner_game_no, None)
        self.failUnlessEqual(d.white_rating, 1586)
        self.failUnlessEqual(d.black_rating, 2100)
        # TODO
        #self.failUnlessEqual(d.white_timeseal, True)
        #self.failUnlessEqual(d.black_timeseal, False)

    def testWhisper(self):
        (w,d) = info_parser.parse_fics_line("John(1740)[90] whispers: I like white")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 90)
        self.failUnlessEqual(d.player, PlayerName('John'))
        self.failUnlessEqual(d.rating_value, 1740)
        self.failUnlessEqual(d.text, 'I like white')
        self.failUnlessEqual(d.method, 'whispers')
    def testKibitz(self):
        (w,d) = info_parser.parse_fics_line("John(1740)[90] kibitzes: I like white")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 90)
        self.failUnlessEqual(d.player, PlayerName('John'))
        self.failUnlessEqual(d.rating_value, 1740)
        self.failUnlessEqual(d.text, 'I like white')
        self.failUnlessEqual(d.method, 'kibitzes')
    def testKibitzShortRating(self):
        # Z watchbotowych przeżyć
        (w,d) = info_parser.parse_fics_line("MiloBot(C)( 958)[235] whispers: Hello from Crafty v22.7 !")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 235)
        self.failUnlessEqual(d.player, PlayerName('MiloBot'))
        self.failUnlessEqual(d.rating_value, 958)
        self.failUnlessEqual(d.text, 'Hello from Crafty v22.7 !')
        self.failUnlessEqual(d.method, 'whispers')
        (w,d) = info_parser.parse_fics_line("MiloBot(C)( 958)[235] kibitzes: mated in 1 moves.")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 235)
        self.failUnlessEqual(d.player, PlayerName('MiloBot'))
        self.failUnlessEqual(d.rating_value, 958)
        self.failUnlessEqual(d.text, 'mated in 1 moves.')
        self.failUnlessEqual(d.method, 'kibitzes')
    def testWhisper2(self):
        (w,d) = info_parser.parse_fics_line("Goober(C)(2399)[185] kibitzes: Hello from Crafty v19.19! (2 cpus)")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 185)
        self.failUnlessEqual(d.player, PlayerName('Goober'))
        self.failUnlessEqual(d.rating_value, 2399)
        self.failUnlessEqual(d.text, 'Hello from Crafty v19.19! (2 cpus)')
        self.failUnlessEqual(d.method, 'kibitzes')
    def testKibitz2(self):
        (w,d) = info_parser.parse_fics_line("Mainflame(C)(2322)[185] whispers: d10 +0.27 c3 Be7 dxe5 Nxe4 Nbd2 Nxd2 Bxd2 O-O Bd3 Nc6 O-O d5 egtb: 0 time: 18.70 nps: 132397")
        self.failUnlessEqual(w, 'game_kibitz')
        self.failUnlessEqual(d.game_no, 185)
        self.failUnlessEqual(d.player, PlayerName('Mainflame'))
        self.failUnlessEqual(d.rating_value, 2322)
        self.failUnlessEqual(d.text, 'd10 +0.27 c3 Be7 dxe5 Nxe4 Nbd2 Nxd2 Bxd2 O-O Bd3 Nc6 O-O d5 egtb: 0 time: 18.70 nps: 132397')
        self.failUnlessEqual(d.method, 'whispers')
    def test_announcement(self):
        (w,d) = info_parser.parse_fics_line('    **ANNOUNCEMENT** from relay: FICS is relaying the XLI Rilton Cup - Last Round. To find more about Relay type "tell relay help"')
        self.failUnlessEqual(w, 'announcement')
        self.failUnlessEqual(d.player, PlayerName('relay'))
        self.failUnlessEqual(d.text, 'FICS is relaying the XLI Rilton Cup - Last Round. To find more about Relay type "tell relay help"')
    def testUserConnected(self):
        (w,d) = info_parser.parse_fics_line('[playerbis has connected.]')
        self.failUnlessEqual(w, 'user_connected')
        self.failUnlessEqual(d, PlayerName('playerbis'))
    def testUserDisconnected(self):
        (w,d) = info_parser.parse_fics_line('[playerbis has disconnected.]')
        self.failUnlessEqual(w, 'user_disconnected')
        self.failUnlessEqual(d, PlayerName('playerbis'))
    def testGameStarted(self):
        (w,d) = info_parser.parse_fics_line('{Game 1 (playerbis vs. root) Creating rated standard match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('playerbis'))
        self.failUnlessEqual(d.black_name, PlayerName('root'))
        self.failUnlessEqual(d.game_no, 1)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
    def testGameStartedUnrated(self):
        (w,d) = info_parser.parse_fics_line('{Game 142 (GuestFQJN vs. GuestCFVZ) Creating unrated blitz match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('GuestFQJN'))
        self.failUnlessEqual(d.black_name, PlayerName('GuestCFVZ'))
        self.failUnlessEqual(d.game_no, 142)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
    def testGameStartedBug(self):
        (w,d) = info_parser.parse_fics_line('{Game 155 (spgs vs. Miklo) Creating rated bughouse match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('spgs'))
        self.failUnlessEqual(d.black_name, PlayerName('Miklo'))
        self.failUnlessEqual(d.game_no, 155)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('bughouse'))
    def testGameStartedSuicide(self):
        (w,d) = info_parser.parse_fics_line('{Game 32 (Chussi vs. SquibCakes) Creating rated suicide match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('Chussi'))
        self.failUnlessEqual(d.black_name, PlayerName('SquibCakes'))
        self.failUnlessEqual(d.game_no, 32)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
    def testGameStartedWild4(self):
        (w,d) = info_parser.parse_fics_line('{Game 165 (ThawCY vs. ChessCracker) Creating rated wild/4 match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('ThawCY'))
        self.failUnlessEqual(d.black_name, PlayerName('ChessCracker'))
        self.failUnlessEqual(d.game_no, 165)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('wild/4'))
    def testGameStartedCont(self):
        (w,d) = info_parser.parse_fics_line('{Game 166 (xufei vs. chessactuary) Continuing rated blitz match.}')
        self.failUnlessEqual(w, 'game_started')
        self.failUnlessEqual(d.white_name, PlayerName('xufei'))
        self.failUnlessEqual(d.black_name, PlayerName('chessactuary'))
        self.failUnlessEqual(d.game_no, 166)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
    def testGameFinishedDraw(self):
        (w,d) = info_parser.parse_fics_line('{Game 164 (CamyC vs. android) Neither player has mating material} 1/2-1/2')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 164)
        self.failUnlessEqual(d.white_name, PlayerName('CamyC'))
        self.failUnlessEqual(d.black_name, PlayerName('android'))
        self.failUnlessEqual(d.result, '1/2-1/2')
        self.failUnlessEqual(d.result_desc, 'Neither player has mating material')
        self.failIf(d.early_abort)
    def testGameFinishedForfeit(self):
        (w,d) = info_parser.parse_fics_line('{Game 173 (android vs. CamyC) CamyC forfeits on time} 1-0')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 173)
        self.failUnlessEqual(d.white_name, PlayerName('android'))
        self.failUnlessEqual(d.black_name, PlayerName('CamyC'))
        self.failUnlessEqual(d.result, '1-0')
        self.failUnlessEqual(d.result_desc, 'CamyC forfeits on time')
        self.failIf(d.early_abort)
    def testGameFinishedMate(self):
        (w,d) = info_parser.parse_fics_line('{Game 62 (Rasquinho vs. farwest) Rasquinho checkmated} 0-1')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 62)
        self.failUnlessEqual(d.white_name, PlayerName('Rasquinho'))
        self.failUnlessEqual(d.black_name, PlayerName('farwest'))
        self.failUnlessEqual(d.result, '0-1')
        self.failUnlessEqual(d.result_desc, 'Rasquinho checkmated')
        self.failIf(d.early_abort)
    def testGameFinishedResign(self):
        (w,d) = info_parser.parse_fics_line('{Game 126 (SquibCakes vs. Chussi) Chussi resigns} 1-0')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 126)
        self.failUnlessEqual(d.white_name, PlayerName('SquibCakes'))
        self.failUnlessEqual(d.black_name, PlayerName('Chussi'))
        self.failUnlessEqual(d.result, '1-0')
        self.failUnlessEqual(d.result_desc, 'Chussi resigns')
        self.failIf(d.early_abort)
    def testGameFinishedAdjourn(self):
        (w,d) = info_parser.parse_fics_line('{Game 74 (Christen vs. Rajan) Christen lost connection; game adjourned} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 74)
        self.failUnlessEqual(d.white_name, PlayerName('Christen'))
        self.failUnlessEqual(d.black_name, PlayerName('Rajan'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Christen lost connection; game adjourned')
        self.failIf(d.early_abort)
    def testGameFinishedAbort1(self):
        (w,d) = info_parser.parse_fics_line('{Game 39 (Sillopsism vs. sparpas) Game aborted on move 1} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 39)
        self.failUnlessEqual(d.white_name, PlayerName('Sillopsism'))
        self.failUnlessEqual(d.black_name, PlayerName('sparpas'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Game aborted on move 1')
        self.failUnless(d.early_abort)
    def testGameFinishedCourtesy(self):
        (w,d) = info_parser.parse_fics_line('{Game 78 (msparrow vs. Belofte) Game courtesyadjourned by msparrow} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 78)
        self.failUnlessEqual(d.white_name, PlayerName('msparrow'))
        self.failUnlessEqual(d.black_name, PlayerName('Belofte'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Game courtesyadjourned by msparrow')
        self.failIf(d.early_abort)
    def testGameFinishedForfTime2(self):
        (w,d) = info_parser.parse_fics_line('{Game 143 (samthefam vs. NemSiMing) samthefam forfeits on time} 0-1')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 143)
        self.failUnlessEqual(d.white_name, PlayerName('samthefam'))
        self.failUnlessEqual(d.black_name, PlayerName('NemSiMing'))
        self.failUnlessEqual(d.result, '0-1')
        self.failUnlessEqual(d.result_desc, 'samthefam forfeits on time')
        self.failIf(d.early_abort)
    def testGameFinishedAbort1_1(self):
        (w,d) = info_parser.parse_fics_line('{Game 52 (bububfo vs. Friscopat) Game aborted on move 1} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 52)
        self.failUnlessEqual(d.white_name, PlayerName('bububfo'))
        self.failUnlessEqual(d.black_name, PlayerName('Friscopat'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Game aborted on move 1')
        self.failUnless(d.early_abort)
    def testGameFinishedStalemate(self):
        (w,d) = info_parser.parse_fics_line('{Game 192 (electricrook vs. dalf) Game drawn by stalemate} 1/2-1/2')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 192)
        self.failUnlessEqual(d.white_name, PlayerName('electricrook'))
        self.failUnlessEqual(d.black_name, PlayerName('dalf'))
        self.failUnlessEqual(d.result_desc, 'Game drawn by stalemate')
        self.failUnlessEqual(d.result, '1/2-1/2')
        self.failIf(d.early_abort)
    def testGameFinishedAbortTooFew(self):
        (w,d) = info_parser.parse_fics_line('{Game 52 (bububfo vs. Hono) Hono lost connection and too few moves; game aborted} *')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 52)
        self.failUnlessEqual(d.white_name, PlayerName('bububfo'))
        self.failUnlessEqual(d.black_name, PlayerName('Hono'))
        self.failUnlessEqual(d.result, '*')
        self.failUnlessEqual(d.result_desc, 'Hono lost connection and too few moves; game aborted')
        self.failUnless(d.early_abort)
    def testGameFinishedAdjudicated(self):
        (w,d) = info_parser.parse_fics_line('{Game 47 (MAd vs. pgv) MAd wins by adjudication} 1-0')
        self.failUnlessEqual(w, 'game_finished')
        self.failUnlessEqual(d.game_no, 47)
        self.failUnlessEqual(d.white_name, PlayerName('MAd'))
        self.failUnlessEqual(d.black_name, PlayerName('pgv'))
        self.failUnlessEqual(d.result, '1-0')
        self.failUnlessEqual(d.result_desc, 'MAd wins by adjudication')
        self.failIf(d.early_abort)
        # TODO: flag for adjudication?

    def testObservingFinished(self):
        (w,d) = info_parser.parse_fics_line('Removing game 138 from observation list.')
        self.failUnlessEqual(w, 'observing_finished')
        self.failUnlessEqual(d.game_no, 138)
    def testGameNoteDrawOffer(self):
        (w,d) = info_parser.parse_fics_line('Game 39: Berke offers a draw.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 39)
        self.failUnlessEqual(d.note, 'Berke offers a draw.')
    def testGameNoteDrawDecline(self):
        (w,d) = info_parser.parse_fics_line('Game 39: radioegg declines the draw request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 39)
        self.failUnlessEqual(d.note, 'radioegg declines the draw request.')
    def testGameNotePauseReq(self):
        (w,d) = info_parser.parse_fics_line('Game 4: wivawo requests to pause the game.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'wivawo requests to pause the game.')
    def testGameNotePauseAcc(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Kobac accepts the pause request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Kobac accepts the pause request.')
    def testGameNoteClockPaus(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Game clock paused.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Game clock paused.')
    def testGameNoteUnpauseReq(self):
        (w,d) = info_parser.parse_fics_line('Game 4: wivawo requests to unpause the game.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'wivawo requests to unpause the game.')
    def testGameNoteUnpauseAcc(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Kobac accepts the unpause request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Kobac accepts the unpause request.')
    def testGameNoteClockResum(self):
        (w,d) = info_parser.parse_fics_line('Game 4: Game clock resumed.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.note, 'Game clock resumed.')
    def testGameNoteTakebackReq(self):
        (w,d) = info_parser.parse_fics_line('Game 97: rahulchess requests to take back 1 half move(s).')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 97)
        self.failUnlessEqual(d.note, 'rahulchess requests to take back 1 half move(s).')
    def testGameNoteTakebackAcc(self):
        (w,d) = info_parser.parse_fics_line('Game 97: Memler accepts the takeback request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 97)
        self.failUnlessEqual(d.note, 'Memler accepts the takeback request.')
    def testGameNoteTakebackDecl(self):
        (w,d) = info_parser.parse_fics_line('Game 290: Divljak declines the takeback request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 290)
        self.failUnlessEqual(d.note, 'Divljak declines the takeback request.')
    def testGameNoteAbortReq(self):
        (w,d) = info_parser.parse_fics_line('Game 51: daneg requests to abort the game.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 51)
        self.failUnlessEqual(d.note, 'daneg requests to abort the game.')
    def testGameNoteAbortDecl(self):
        (w,d) = info_parser.parse_fics_line('Game 51: kmhaswad declines the abort request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 51)
        self.failUnlessEqual(d.note, 'kmhaswad declines the abort request.')
    def testGameNoteDrawAccept(self):
        (w,d) = info_parser.parse_fics_line('Game 128: dcwarren accepts the draw request.')
        self.failUnlessEqual(w, 'game_note')
        self.failUnlessEqual(d.game_no, 128)
        self.failUnlessEqual(d.note, 'dcwarren accepts the draw request.')
    def testAnnouncement(self):
        (w,d) = info_parser.parse_fics_line('    **ANNOUNCEMENT** from relay: FICS is relaying the Swedish Championship. To find out which games are being relayed type "tell relay listgames", to observe the top n games type "tell relay observe n". Read news 1153 for the instructions on the "guess the move" no prize competition.')
        self.failUnlessEqual(w, 'announcement')
        self.failUnlessEqual(d.player, PlayerName('relay'))
        self.failUnlessEqual(d.text, 'FICS is relaying the Swedish Championship. To find out which games are being relayed type "tell relay listgames", to observe the top n games type "tell relay observe n". Read news 1153 for the instructions on the "guess the move" no prize competition.')
    def testSeekLineWildFr(self):
        (w,d) = info_parser.parse_fics_line('GuestBCYW (++++) seeking 5 0 unrated wild/fr ("play 36" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.seek_no, 36)
        self.failUnlessEqual(d.player, PlayerName('GuestBCYW'))
        self.failUnlessEqual(d.player_rating_value, 0)
        self.failUnlessEqual(d.game_spec.game_type, GameType('wild/fr'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,0))
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.color, None)
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, False)
    def testSeekLineGuestColor(self):
        (w,d) = info_parser.parse_fics_line('xxxccc (++++) seeking 5 0 unrated blitz [white] ("play 131" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.seek_no, 131)
        self.failUnlessEqual(d.player, PlayerName('xxxccc'))
        self.failUnlessEqual(d.player_rating_value, 0)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,0))
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.color, Color('white'))
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, False)
    def testSeekLineRegisteredManualNoColor(self):
        (w,d) = info_parser.parse_fics_line('Pieraleco (1531) seeking 2 30 rated blitz m ("play 42" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.player, PlayerName('Pieraleco'))
        self.failUnlessEqual(d.player_rating_value, 1531)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(2,30))
        self.failUnlessEqual(d.game_spec.is_rated, True)
        # TODO: private?
        self.failUnlessEqual(d.color, None)
        self.failUnlessEqual(d.seek_no, 42)
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, True)
    def test_seek_line_admin_manual_formula(self):
        (w,d) = info_parser.parse_fics_line('Farad(SR)(TD) (1231E) seeking 1 2 rated suicide m ("play 42" to respond)')
        self.failUnlessEqual(w, 'seek')
        self.failUnlessEqual(d.player, PlayerName('Farad'))
        self.failUnlessEqual(d.player_rating_value, 1231)
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(1,2))
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.color, None)
        self.failUnlessEqual(d.seek_no, 42)
        self.failUnlessEqual(d.using_formula, False)
        self.failUnlessEqual(d.is_manual, True)
    # TODO: manual, formula, ranking, nawiaski w imieniu
    def testManySeeks(self):
        seek_lines = load_parse_data_file("seeks.lines").split("\n")
        private_count = 0
        manual_count = 0
        color_count = { WHITE: 0, BLACK: 0 }
        rated_count = { True: 0, False: 0 }
        for line in seek_lines:
            if not line.strip():
                continue
            (w,d) = info_parser.parse_fics_line(line)
            self.failUnlessEqual(w, "seek", "Failed to parse seek: " + line)
            self.failUnlessIsInstance(d.seek_no, int)
            self.failUnlessIsInstance(d.player, PlayerName)
            self.failUnlessIsInstance(d.player_rating_value, int)
            self.failUnlessIsInstance(d.is_manual, bool)
            self.failUnlessIsInstance(d.using_formula, bool)
            if d.color is not None:
                self.failUnlessIsInstance(d.color, Color)
            self.failUnlessIsInstance(d.game_spec, GameSpec)
            self.failUnlessIsInstance(d.game_spec.game_type, GameType)
            self.failUnlessIsInstance(d.game_spec.is_rated, bool)
            self.failUnlessIsInstance(d.game_spec.is_private, bool)
            self.failUnlessIsInstance(d.game_spec.clock, GameClock)
            if d.game_spec.is_private:
                private_count += 1
            if d.is_manual:
                manual_count += 1
            if d.color is not None:
                color_count[d.color] += 1
            rated_count[d.game_spec.is_rated] += 1
        self.failIfEqual(manual_count, 0, "No manual seek spotted")
        self.failIfEqual(color_count[WHITE], 0, "No white seek spotted")
        self.failIfEqual(color_count[BLACK], 0, "No black seek spotted")
        self.failIfEqual(rated_count[True], 0, "No rated seek spotted")
        self.failIfEqual(rated_count[False], 0, "No unrated seek spotted")
        self.failUnlessEqual(private_count, 0, "Some private seek spotted, should not happen")

        # TODO: check some of those lines
    def testRemovedSeeksOne(self):
        (w,d) = info_parser.parse_fics_line('Ads removed: 37')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(seek_no=37) ] )
    def testRemovedSeeksMore(self):
        (w,d) = info_parser.parse_fics_line('Ads removed: 22 1 119')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(seek_no=x) for x in [22, 1, 119] ] )
    def testSeekIvSeekInfo1(self):
        (w,d) = info_parser.parse_fics_line('<s> 8 w=visar ti=02 rt=2194  t=4 i=0 r=r tp=suicide c=? rr=0-9999 a=t f=t')
        self.failUnlessEqual(w, "seek")
        self.failUnlessEqual(d.seek_no, 8)
        self.failUnlessEqual(d.player, PlayerName('visar'))
        # TODO: ti (titles). This is hex number with or-ed 0x1 - unregistered 0x2 - computer 0x4 - GM 0x8 - IM
        # 0x10 - FM 0x20 - WGM 0x40 - WIM 0x80 - WFM
        self.failUnlessEqual(d.player_rating_value, 2194)
        self.failUnlessEqual(d.game_spec.clock, GameClock(4,0))
        self.failUnlessEqual(d.game_spec.is_rated, True) # r=r rated, r=u unrated
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
        self.failUnlessEqual(d.color, None)   # ?, W, B
        # TODO self.failUnlessEqual(d.rating_min, 0)
        # TODO self.failUnlessEqual(d.rating_max, 9999)
        self.failUnlessEqual(d.is_manual, False) # a=t automatic, a=f manual
        self.failUnlessEqual(d.using_formula, True)
    def testSeekIvSeekInfo2(self):
        (w,d) = info_parser.parse_fics_line('<s> 12 w=saeph ti=00 rt=1407  t=1 i=0 r=r tp=lightning c=? rr=0-9999 a=t f=f  ')
        self.failUnlessEqual(w, "seek")
        # TODO: add fields
    def testSeekIvSeekInfo3(self):
        (w,d) = info_parser.parse_fics_line('<sn> 82 w=Mekk ti=00 rt=1341  t=5 i=2 r=r tp=blitz c=? rr=1401-1403 a=t f=f')
        self.failUnlessEqual(w, "seek")  # TODO: maybe seek own? what is <sn>?
        # TODO: add fields
    def testSeeksClearedIvSeekInfo(self):
        (w,d) = info_parser.parse_fics_line('<sc>')
        self.failUnlessEqual(w, 'seeks_cleared')
        self.failUnlessEqual(d, GenericText('<sc>'))
    def testRemovedSeeksOneIvSeekInfo(self):
        (w,d) = info_parser.parse_fics_line('<sr> 37')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(seek_no=37) ])
    def testRemovedSeeksMoreIvSeekInfo(self):
        (w,d) = info_parser.parse_fics_line('<sr> 22 1 119')
        self.failUnlessEqual(w, 'seek_removed')
        self.failUnlessEqual(d, [ SeekRef(no) for no in [22, 1, 119] ] )
    def testOffersIvPendinfoOfferReceived(self):
        # http://www.freechess.org/Help/HelpFiles/iv_pendinfo.html
        # <pf> index w=name_from t=offer_type p=params
        # TODO: grab sample data and make test
        raise SkipTest
    def testOffersIvPendinfoOfferSent(self):
        # http://www.freechess.org/Help/HelpFiles/iv_pendinfo.html
        #(w,d) = parser.parse_fics_line('<pt> index w=name_to t=offer_type p=params')
        # TODO: grab sample data and make test
        raise SkipTest
    def testOffersIvPendinfoOfferDeclined(self):
        # <pr> index
        # what's that? - offer accepted/declined/withdrawn/removed
        # TODO: grab sample data and make test
        raise SkipTest
    def testAutoLogout(self):
        (w,d) = info_parser.parse_fics_line(
            '**** Auto-logout because you were idle more than 60 minutes. ****')
        #print w
        #print d
        self.failUnlessEqual(w, 'auto_logout')
        self.failUnlessEqual(d, GenericText("Auto-logout because you were idle more than 60 minutes."))

    def testIgnores(self):
        # TODO: move those to reply parsing and treat as they should be treated
        not_used_lines = [
          'Style 12 set.',
          'You are no longer receiving match requests.',
          'Highlight is off.',
          'You will not hear shouts.',
          'You will not hear cshouts.',
          'You will now hear kibitzes.',
          'You will now hear tells from unregistered users.',
          'You will now hear game results.',
          'You will now hear logins/logouts.',
          'Plan variable 1 changed to \'I am a bot\'',
          'Width set to 1024.',
          'startpos set.',
          'graph set.',
          'You will not auto unobserve.',
          'You will not see seek ads',
          ]
        lines = [
            'block set.',
            '  ',
            "\r   \n",
        ]
        for x in lines:
            t = info_parser.parse_fics_line(x)
            self.failUnless(t, "Should ignore: %s" %x)
            self.failUnlessEqual(t[0], 'ignore', "Should ignore: %s" % x)

class ParseUnobserveReplyTestCase(unittest.TestCase):
    def test_unobserve_correct(self):
        info = parse_unobserve_reply(
            "Removing game 124 from observation list.")
        self.failUnlessEqual(info, GameReference(game_no=124))
    def test_unobserve_logic_fail(self):
        for text in [
            "You are not observing game 13.",
            "You are not observing any games.",
            ]:
            self.failUnlessRaises(errors.AttemptToActOnNotUsedGame,
                parse_unobserve_reply, text)
    def test_unobserve_bad_syntax(self):
        for text in [
            "",
            "blah blah",
            "Removing game KROKODYL from observation list.",
            ]:
            self.failUnlessRaises(errors.ReplyParsingException,
                parse_unobserve_reply, text)

class ParseShowListTestCase(unittest.TestCase):
    def test_td(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-td.lines"))
        self.failUnlessEqual(
            info,
            ListContents(
                name='td',
                items=['abuse', 'GameBot', 'Oannes', 'srBOT', 'abuseBOT', 'GameLibraryBot',
                       'observatoer', 'statBot', 'abuseII', 'GameSaver', 'ObserveBot',
                       'STCRobot', 'adminBOT', 'javaboardBOT', 'Observer', 'SuperTD',
                       'Analysisbot', 'KothD', 'OCLbot', 'SupportBot', 'BabasChess',
                       'LectureBot', 'Offender', 'SurveyBot', 'Blackteam', 'Lecturer',
                       'OnlineTours', 'tbot', 'CCBOT', 'Linares', 'OpenLib', 'TeamLeague',
                       'ChannelBot', 'linuxchick', 'pebbo', 'testbot', 'chLog', 'littleWild',
                       'PeterParker', 'Thief', 'compabuseBOT', 'logics', 'PokerBot',
                       'ThiefTest', 'ComputerAbuse', 'MadrookBot', 'PoolBot',
                       'TourneyWatcher', 'Computers', 'mailBOT', 'puzzlebot', 'TScheduleBot',
                       'Correspondence', 'mamer', 'Rachel', 'WatchBot', 'CVLbot', 'mamerPR',
                       'Rebecca', 'WatchBotTest', 'dbslave', 'MasterGameBot', 'relay',
                       'WesBot', 'Elvira', 'MateBot', 'RelayInfo', 'Whiteteam', 'endgamebot',
                       'MuelheimNord', 'RelayScheduleBOT', 'wildBot', 'Event',
                       'NorCalLeague', 'ROBOadmin', 'Wildchess', 'FICSChampionships',
                       'notesBot', 'Sibylle', 'Yafi', 'FicsTeamBot', 'NukeBotX',
                       'SparkysDrone',]
                ))
    def test_computer(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-computers.lines"))
        self.failUnlessEqual(
            info,
            ListContents(
                name='computer',
                items=['Abuyen', 'DeepSjeng', 'Koibito', 'SelfKiller', 'AIchess',
                       'DeepThoughts', 'Kromer', 'ShotgunBlues', 'Alfilchess', 'DeepZ',
                       'kurushi', 'SigmaC', 'AliceC', 'DemolitionChess', 'LancePerkins',
                       'SiliconC', 'Almere', 'DeuteriumCCT', 'leaderbeans', 'Sillycon',
                       'AlmondX', 'DeuteriumEngine', 'LilKikr', 'Singularity', 'AlonzoC',
                       'DirtyChess', 'LittleBugger', 'SjengX', 'Angledust', 'djevans',
                       'LittleLurking', 'Skottel', 'Arandora', 'djunior', 'LittleThought',
                       'SlowBox', 'ArasanX', 'donkeyfactory', 'LochChessMonster',
                       'SlowMachine', 'ARChess', 'DorkyX', 'LuigiBot', 'Snelheid', 'ArShah',
                       'DotNetChess', 'Luminance', 'Sordid', 'ascp', 'DSJeng', 'Lurking',
                       'Sorgenkind', 'atomkraft', 'Ecalevol', 'marquisce', 'Species',
                       'AuraBlue', 'EJD', 'MegaBot', 'SpeckEngine', 'AuraBlueA', 'EnginMax',
                       'megielszmergiel', 'Speyside', 'AuraBlueB', 'exeComp', 'meru',
                       'SpyderChess', 'AuraBlueC', 'FeralChess', 'MiloBot', 'Squirrels',
                       'AuraBlueD', 'FireCompi', 'MiniZerdax', 'sregorg', 'AuraBlueE',
                       'FirstCore', 'Moireabh', 'stayalive', 'Azkikr', 'fjjvh',
                       'MortimerBlackwell', 'strelka', 'babylonbot', 'FunComp', 'MrsLurking',
                       'StTeresa', 'BabyLurking', 'Gamin', 'mscp', 'SuperBooker', 'BertaCCT',
                       'Gaviota', 'myceX', 'SuperCanuck', 'BigDaddy', 'GeidiPrime', 'mycomp',
                       'SuperZerdax', 'BigMomma', 'Gigabot', 'MyrddinComp', 'SupremeBeing',
                       'birdcostello', 'GlaurungC', 'nakshatra', 'Symbolic', 'bistromath',
                       'GnuCheese', 'NightmareX', 'Telepath', 'BlackDemon', 'GNUChessSix',
                       'ntwochess', 'tentacle', 'blik', 'GoldBarMM', 'Obnoxious',
                       'TestOfLogics', 'bobbyfischer', 'GreatPumpkin', 'oldman',
                       'TheConfusedComp', 'BotTheBaron', 'GriffyJr', 'Olympus', 'Thiamath',
                       'BremboCE', 'GriffySr', 'Opossum', 'Thinker', 'BugZH',
                       'GuaraniSchulz', 'Osquip', 'Thukydides', 'callipygian', 'Gunwalloe',
                       'owlce', 'TimeaChess', 'CapivaraLK', 'Hephasto', 'parrot',
                       'TinkerFICS', 'CatNail', 'highrating', 'PawnyX', 'TJchess', 'cchess',
                       'hokuspokus', 'Pentiumpatzer', 'TJChessA', 'ChainReaction',
                       'hokuspokusII', 'PhoenixAsh', 'TJchessB', 'ChangeIsComing', 'Horsian',
                       'plink', 'TogaII', 'ChessCentre', 'Hossa', 'plisk', 'TogaRouter',
                       'ChessMindEngine', 'Humpers', 'Plnik', 'Tosco', 'ChessplayingBot',
                       'HussarFICS', 'Polycephaly', 'TrojanKnight', 'ChessPlusPlus',
                       'Hutnik', 'PopperX', 'TurboGM', 'ChessTraining', 'IFDThor', 'Potajex',
                       'TwistedLogicX', 'Chirone', 'IkarusX', 'Prolegomena', 'twoxone',
                       'chirpy', 'inemuri', 'qgchess', 'umko', 'codpiece', 'Ingoc',
                       'Rakanishu', 'Uniblab', 'Compi', 'Inqstr', 'redqueenchess',
                       'VictoriaBot', 'Compucheck', 'InstanceC', 'resistentialism', 'Vogen',
                       'crafty', 'IronSpike', 'RoboSigma', 'Webkikr', 'CrazyBeukiBot',
                       'JabbaChess', 'Rookie', 'wildbird', 'cubebox', 'JadeiteMech', 'Rueno',
                       'XabacUs', 'DarkAngel', 'javachesscomp', 'SaqqaraX', 'ynode',
                       'DayDreamerX', 'JuniorLurking', 'scaramanga', 'Zawaenn', 'DDD',
                       'KayNineDawg', 'Schizophreniac', 'Zchizophrenic', 'DeepJunior', 'Kec',
                       'Scomb', 'zerowin', 'DeepNightmare', 'knightsmasher', 'searcherFICS',
                       'zzzzzztrainer',]))
    def test_channel(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-channel.lines"))
        self.failUnlessEqual(
            info,
            ListContents(
                name='channel',
                items=['4', '53']))
    def test_empty_notify(self):
        info = parse_showlist_reply(load_parse_data_file("showlist-emptynotify.lines"))
        self.failUnlessEqual(info, ListContents(
            name='notify',
            items=[]
        ))
    def test_syntax_error(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_showlist_reply,
            'Zielony krokodyl.')
    def test_logic_error(self):
        self.failUnlessRaises(
            errors.UnknownList,
            parse_showlist_reply,
            '"xx" does not match any list name.')
    def test_logic_error_checkattr(self):
        try:
            parse_showlist_reply(
                '"xx" does not match any list name.')
            self.fail("parse_showlist_reply failed to throw on unknown list name")
        except errors.UnknownList as e:
            self.failUnlessEqual(e.list_name, "xx")

class ParseFingerReplyTestCase(unittest.TestCase):

    def _load_file(self, name):
        return load_parse_data_file_patching_continuations(name)

    def test_nonexistant(self):
        self.failUnlessRaises(
            errors.UnknownPlayer,
            parse_finger_reply,
            self._load_file("finger-nonexist.lines")
        )
    def test_empty(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_finger_reply,
            "")
    def test_ugly(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_finger_reply,
            "\nblah")
    def test_gmkramnik(self):
        info = parse_finger_reply(
            self._load_file("finger-gmkramnik.lines"))
        self.failUnlessEqual(
            info,
            FingerInfo(name="GMKramnik",
                 results={
                    GameType("Standard"): ResultStats(
                        wins_count=1, draws_count=0, losses_count=0,
                        rating=PlayerRating(value=2800, rd=Decimal('350.0')), best=None),
                    },
                 plan=['This is the demo account to relay the games of GM Kramnik, Vladimir (RUS) fide id. number = 4101588',
                       'FIDE Elo rating : 2800',
                       'Current World Rank: 4',
                       ]))
    def test_mekk(self):
        info = parse_finger_reply(
            self._load_file("finger-mekk.lines"))
        # TODO: replace assert_dicts_equal with object/namedtuples equiv
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="Mekk",
                results={
                     GameType('Atomic'): ResultStats(best=None, wins_count=23, draws_count=1, losses_count=50, rating=PlayerRating(1525, rd=Decimal('159.2')) ),
                     GameType('Blitz'): ResultStats(best=1522, wins_count=3900, draws_count=410, losses_count=5797, rating=PlayerRating(1342, rd=Decimal('42.4'))),
                     GameType('Bughouse'): ResultStats(best=None, wins_count=3, draws_count=0, losses_count=5, rating=PlayerRating(1035, rd=Decimal('350.0'))),
                     GameType('Crazyhouse'): ResultStats(best=1495, wins_count=73, draws_count=0, losses_count=235, rating=PlayerRating(1451, rd=Decimal('99.8'))),
                     GameType('Lightning'): ResultStats(best=1116, wins_count=15, draws_count=1, losses_count=115, rating=PlayerRating(1495, rd=Decimal('233.0'))),
                     GameType('Losers'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=6, rating=PlayerRating(1674, rd=Decimal('350.0'))),
                     GameType('Standard'): ResultStats(best=1935, wins_count=730, draws_count=156, losses_count=913, rating=PlayerRating(1759, rd=Decimal('68.8'))),
                     GameType('Suicide'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=14, rating=PlayerRating(1384, rd=Decimal('278.1'))),
                     GameType('Wild'): ResultStats(best=1875, wins_count=287, draws_count=31, losses_count=457, rating=PlayerRating(1683, rd=Decimal('100.5')))
                 },
                 plan=[
                     'Marcin Kasperski, Warsaw, Poland. http://mekk.waw.pl',
                     'wild fr=normal chess with randomized initial position. Great fun! I can play unrated wild fr game and explain the rules, just ask.',
                     'Please, say "good game" only if it was good game. Auto-greetings are incredibly irritating.',
                     'If I happen to ignore your tells, most likely I am playing from my mobile phone (btw, http://yafi.pl is a great mobile fics client)',
                     'Correspondence chess is great if you have little time, but prefer thinking games. My tips:  http://schemingmind.com for web-based play, http://e4ec.org if you want to stay with email. On schemingmind you can also learn atomic, crazyhouse, wild fr and other variants - without time pressure.',
                     'I wrote and maintain WatchBot. http://mekk.waw.pl/mk/watchbot',
                     'FICS enhancements ideas:  http://mekk.waw.pl/mk/eng/chess/art/ideas_fics',
                     'How to write a FICS bot: http://blog.mekk.waw.pl/archives/7-How-to-write-a-FICS-bot-part-I.html',
                     'Szachowy slownik polsko-angielski: http://mekk.waw.pl/mk/szachy/art/ang_terminologia',
                     'Polski podrecznik FICS: http://mekk.waw.pl/mk/szachy/art/fics_opis',
                 ]))
    def test_mek(self):
        info = parse_finger_reply(
            self._load_file("finger-mek.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(name="Mek",
                 results={
                    GameType('Standard'): ResultStats(rating=PlayerRating(1606, rd=Decimal('350.0')), best=None, wins_count=0, losses_count=1, draws_count=0),
                    },
                 plan=[
                    ]))
    def test_mad(self):
        info = parse_finger_reply(
            self._load_file("finger-mad.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(name="MAd",
                 results={
                     GameType('Blitz'): ResultStats(rating=PlayerRating(1606, rd=Decimal('45.3')), wins_count=10615, losses_count=5217,
                         draws_count=574, best=1722),
                     GameType('Standard'): ResultStats(rating=PlayerRating(1793, rd=Decimal('350.0')), wins_count=35, losses_count=12,
                         draws_count=2, best=None),
                     GameType('Lightning'): ResultStats(rating=PlayerRating(1633, rd=Decimal('350.0')), wins_count=1, losses_count=6,
                         draws_count=0, best=None)},
                 plan=[
                    '''"But I don't want to go among MAd people." Alice remarked "Oh, you can't help that," said the cat: "We are all MAd here, I'm MAd, you're MAd." "How do you know I'm MAd?" said Alice. "You must be." said the cat, "or you wouldn't have come here."''',
                    '''************************************************************************ "Will you tell me something? "Perhaps." "When I dream, sometimes I remember how to fly. You just lift one leg, then you lift the other leg, and you're not standing on anything, and you can fly. And then when I wake up I can't remember how to do it any more." "So?" "So what I want to know is, when I'm asleep, do I really remember how to fly? And forget how when I wake up? Or am I just dreaming I can fly? "When you dream, sometimes you remember. When you wake, you always forget." "But that's not fair..." "No."''',
                    '''************************************************************************* If our game is adjourned I will ask for an abort: since it is a blitz chess game, the possibility that one of the players analyzes the position has to be ruled out. If you insist on playing I'll let you win on time and you'll end up on my noplay. If you refuse to resign when you're lost and I have lot of time I will noplay you too. I don't want to be be bored till I bluder a piece, I'm here to enjoy the game.''',
                    '''************************************************************************* If you know SNOWHITE 7 dwarfs names in your own language please message them to me''',
                    '''************************************************************************* mad@freechess.org MAd was born on Dec 21st 1993''',
                    '''************************************************************************* "Ungluecklich das Land, das Helden noetig hat." (Fortunata la terra che non ha bisogno di eroi)''',
                    '''************************************************************************* MAd is proud to be honourary member of #$%& (Always Right Society of England). MAd is also member of PLO (Punk and Loaded Organization).''',
                    '''************************************************************************* Current BCF: 148''',
                    '''New NMS record 0.000131 - by MAd''',
                    '''************************************************************************** PCA (Pookie Channel Association) president. Message me to join. Members: Seneca, Ovidius, Thanatos, Trixi, Trixi, NOFX, ExGod, knife, MacLoud, Boutros, Westley, TOOTHPICK, jean, RifRaf, Mlausa, Pinocchio, ratemenot, hyjynx, Eeyore (NOW BANNED FROM PCA!), Garion, norpan, Psycho, ARCEE, TheHacker, Jan, Alefith, Tekken, Sheridan, Axel, Chessty, pelicon, seordin, ChessWisdom, AustinPowders, DoctorColossus, PenguinKing, TheGenius, chesswhiz, chessmasterMO, Mackja, munchy''',
                 ]))
    def test_watchbot(self):
        info = parse_finger_reply(
            self._load_file("finger-watchbot.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="WatchBot",
                results=dict(
                ),
                plan=[
                    '''I am a computer bot (automated program). I don't play, I just watch.''',
                    '''My main purpose is to store comments made during the game (whispers/kibitzes) so they can be reviewed by the players after the game. See "http://mekk.waw.pl/mk/watchbot" for details.''',
                    '''.''',
                    '''I handle plenty of commands (in particular you can ask me to send some games via email). Use "tell WatchBot help" or view "http://mekk.waw.pl/mk/watchbot/usage_intro" to learn them.''',
                    '''Or just visit "http://mekk.waw.pl/mk/watchbot" to find, replay, and download the games.''',
                    '''.''',
                    '''This is release c37c7befc1ac, last updated 2011-08-09.''',
                    '''.''',
                    '''I have been written and I am run by Mekk ("finger Mekk").''',
                    '''If I am down or misbehave, my author may be unaware, message Mekk or (preferably) email WatchBotSupport@mekk.waw.pl to report the problem''',
                ]))
    def test_guest(self):
        info = parse_finger_reply(
            self._load_file("finger-guest.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="GuestVNCT",
                results=dict(
                ),
                plan=[
                ]))
    def test_relay(self):
        info = parse_finger_reply(
            self._load_file("finger-relay.lines"))
        assert_dicts_equal(
            self,
            info,
            FingerInfo(
                name="relay",
                results=dict(
                ),
                plan=[
                    '''use "tell relay help commands" to find more about relay commands''',
                    '''use "tell relay observe" to automatically observe the highest rated relayed game''',
                    '''use "tell relay gtm <game_number> <move>" (eg tell relay gtm 54 Nf3) to guess the next move''',
                    '''I will keep the score and you can check how people are doing with "tell relay gtmrank".''',
                    '''Accepted notation is reduced algebraic, thus e4 works but e2e4 does not. Similarly Nxe5 works but NxN does not. To guess castling use o-o or o-o-o but not e1g1.''',
                    '''Use "tell relay notify" if you want to be told what tournaments are being relayed when you login''',
                    '''http://www.freechess.org/Events/Relay/ and http://www.freechess.org/Events/Relay/2010 to see what tournaments are or will be relayed''',
                ]))

class ParseObserveReplyTestCase(unittest.TestCase):
    def test_private(self):
        self.failUnlessRaises(
            errors.AttemptToAccessPrivateGame,
            parse_observe_reply,
            "Sorry, game 125 is a private game")
    def test_already_observed(self):
        self.failUnlessRaises(
            errors.GameAlreadyObserved,
            parse_observe_reply,
            "You are already observing game 77."
        )
    def test_limit(self):
        self.failUnlessRaises(
            errors.LimitExceeded,
            parse_observe_reply,
            "You are already observing the maximum number of games")
    def test_rubbish(self):
        self.failUnlessRaises(
            errors.ReplyParsingException,
            parse_observe_reply,
            "Blah blah")
    def testNormal(self):
        d = parse_observe_reply( load_tstdata_file( 'ficsparserdata', 'observe-normal.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 92)
        self.failUnlessEqual(d.white_name, PlayerName('Motyl'))
        self.failUnlessEqual(d.white_rating_value, 1857)
        self.failUnlessEqual(d.black_name, PlayerName('Aretus'))
        self.failUnlessEqual(d.black_rating_value, 1907)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(15,10))
        is12 = d.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 92 Motyl Aretus 0 15 10 39 39 900 900 1 none (0:00) none 0 0 0")
    def testProblematic(self):
        d = parse_observe_reply( load_tstdata_file( 'ficsparserdata', 'observe-spec-norating.lines')  )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 161)
        self.failUnlessEqual(d.white_name, PlayerName('ilmagicoalverman'))
        self.failUnlessEqual(d.white_rating_value, 1582)
        self.failUnlessEqual(d.black_name, PlayerName('bibibibi'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(15, 0))
        is12 = d.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 161 ilmagicoalverman bibibibi 0 15 0 39 39 900 900 1 none (0:00) none 0 0 0")

    def testProblematic2(self):
        d = parse_observe_reply(load_tstdata_file( 'ficsparserdata', 'observe-spec-shortrating.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 222)
        self.failUnlessEqual(d.white_name, PlayerName('Johnnyp'))
        self.failUnlessEqual(d.white_rating_value, 923)
        self.failUnlessEqual(d.black_name, PlayerName('schakeric'))
        self.failUnlessEqual(d.black_rating_value, 1321)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(20,0))
        is12 = d.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 222 Johnnyp schakeric 0 20 0 39 39 1200 1200 1 none (0:00) none 0 0 0")

    def testProblematic3(self):
        d = parse_observe_reply(load_tstdata_file( 'ficsparserdata', 'observe-spec-shortrating-white.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 221)
        self.failUnlessEqual(d.white_name, PlayerName('GuestMGVG'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_name, PlayerName('Mekk'))
        self.failUnlessEqual(d.black_rating_value, 1371)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,5))

    def testWild4(self):
        d = parse_observe_reply(load_tstdata_file( 'ficsparserdata', 'observe-wild4.lines') )
        self.failUnless(d)
        self.failUnlessEqual(d.game_no, 226)
        self.failUnlessEqual(d.white_name, PlayerName('Raph'))
        self.failUnlessEqual(d.white_rating_value, 1827)
        self.failUnlessEqual(d.black_name, PlayerName('andycappablanca'))
        self.failUnlessEqual(d.black_rating_value, 1878)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('wild/4'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(3,0))

class ParseGamesLineTestCase(unittest.TestCase):

    def testEx1(self):
        (w,d) = parse_games_reply_line('2 (Exam.    0 LectureBot     0 LectureBot) [ uu  0   0] W:  1')
        self.failUnlessEqual(w, 'Examine')
        self.failUnlessEqual(d.game_no, 2)

    def testEx2(self):
        (w,d) = parse_games_reply_line('8 (Exam. 1830 Myopic      1890 BULLA     ) [ br  3   0] W:  1')
        self.failUnlessEqual(w, 'Examine')
        self.failUnlessEqual(d.game_no, 8)

    def testG1(self):
        (w,d) = parse_games_reply_line('4 ++++ yetis       ++++ GuestWWJX  [ bu  5  12]   1:09 -  3:39 (28-26) W: 19')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 4)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('yetis'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestWWJX'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('blitz'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5,12))

    def testG2(self):
        (w,d) = parse_games_reply_line('14 ++++ DeathValzer ++++ GuestMLSG  [ uu  0   0]   0:00 -  0:00 (34-11) B: 26')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 14)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('DeathValzer'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestMLSG'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('u'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('untimed'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(0,0))

    def testG3(self):
        (w,d) = parse_games_reply_line('51 ++++ SupraPhonic ++++ GuestTWMQ  [ Su  3   0]   2:59 -  2:52 (14-15) B:  4')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 51)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('SupraPhonic'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestTWMQ'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('S'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('suicide'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(3, 0))

    def testG4(self):
        (w,d) = parse_games_reply_line('52 ++++ bozziofan   ++++ GuestBFRV  [ su 20   0]  13:33 - 15:41 ( 3-19) W: 39')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 52)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('bozziofan'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestBFRV'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(20, 0))

    def testG5(self):
        (w,d) = parse_games_reply_line('53 ++++ Wampum      1172 nurp       [ bu  5   0]   4:02 -  3:39 (37-34) B: 15')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 53)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('Wampum'))
        self.failUnlessEqual(d.white_rating_value, 0)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('nurp'))
        self.failUnlessEqual(d.black_rating_value, 1172)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5, 0))

    def testG6(self):
        (w,d) = parse_games_reply_line('36 1447 zzzzzztrain ++++ GuestBVXT  [ bu  2  12]   1:36 -  2:25 (35-36) W: 10')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 36)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('zzzzzztrain'))
        self.failUnlessEqual(d.white_rating_value, 1447)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('GuestBVXT'))
        self.failUnlessEqual(d.black_rating_value, 0)
        self.failUnlessEqual(d.game_spec.is_rated, False)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(2, 12))

    def testG7(self):
        (w,d) = parse_games_reply_line('71  832 paratoner    912 stshot     [ br 10   0]   5:47 -  7:28 (14-22) W: 20')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 71)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('paratoner'))
        self.failUnlessEqual(d.white_rating_value,  832)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('stshot'))
        self.failUnlessEqual(d.black_rating_value, 912)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(10, 0))

    def testG8(self):
        (w,d) = parse_games_reply_line('83 1013 origamikid   841 drmksingh  [ br  3   5]   0:23 -  0:44 (27-33) W: 25')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 83)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('origamikid'))
        self.failUnlessEqual(d.white_rating_value, 1013)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('drmksingh'))
        self.failUnlessEqual(d.black_rating_value, 841)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(3, 5))

    def testG9(self):
        (w,d) = parse_games_reply_line('44  913 Veeber      1013 LorenzoDV  [pbr 12   0]   5:13 -  3:01 (17-25) W: 31')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 44)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('Veeber'))
        self.failUnlessEqual(d.white_rating_value,  913)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('LorenzoDV'))
        self.failUnlessEqual(d.black_rating_value, 1013)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(12, 0))

    def testG10(self):
        (w,d) = parse_games_reply_line('34 1118 JaronGroffe  868 sklenar    [ br 10   0]   4:41 -  6:41 (14-11) W: 29')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 34)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('JaronGroffe'))
        self.failUnlessEqual(d.white_rating_value, 1118)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('sklenar'))
        self.failUnlessEqual(d.black_rating_value, 868)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(10, 0))

    def testG11(self):
        (w,d) = parse_games_reply_line('85 1254 rugs         823 MjollnirPa [ br  5   3]   1:37 -  0:35 (29-20) W: 30')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 85)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('rugs'))
        self.failUnlessEqual(d.white_rating_value, 1254)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('MjollnirPa'))
        self.failUnlessEqual(d.black_rating_value, 823)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(5, 3))

    def testG12(self):
        (w,d) = parse_games_reply_line('1 1700 yacc        1542 dontrookba [psr 20  20]  28:42 - 23:38 (17-19) B: 32')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 1)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('yacc'))
        self.failUnlessEqual(d.white_rating_value, 1700)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('dontrookba'))
        self.failUnlessEqual(d.black_rating_value, 1542)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(20, 20))

    def testG13(self):
        (w,d) = parse_games_reply_line('42 1608 monteleo    2545 Topolino   [ sr 15   2]  14:34 - 13:48 (38-35) B:  8')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 42)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('monteleo'))
        self.failUnlessEqual(d.white_rating_value, 1608)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('Topolino'))
        self.failUnlessEqual(d.black_rating_value, 2545)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(15, 2))

    def testG14(self):
        (w,d) = parse_games_reply_line('67 1095 PlatinumKni 1735 LiquidEmpt [pbr  2  12]   3:34 -  2:07 (21-24) W: 34')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 67)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('PlatinumKni'))
        self.failUnlessEqual(d.white_rating_value, 1095)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('LiquidEmpt'))
        self.failUnlessEqual(d.black_rating_value, 1735)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, True)
        self.failUnlessEqual(d.game_spec.game_type, GameType('b'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(2, 12))

    def testG15(self):
        (w,d) = parse_games_reply_line('204 1534 NoSpeedChes 1513 EvilSchmoo [ sr165   0] 2:14:11 -2:37:11 (33-31) B: 21')
        self.failUnlessEqual(w, 'Game')
        self.failUnlessEqual(d.game_no, 204)
        self.failUnlessEqual(d.white_truncated_name, PlayerName('NoSpeedChes'))
        self.failUnlessEqual(d.white_rating_value, 1534)
        self.failUnlessEqual(d.black_truncated_name, PlayerName('EvilSchmoo'))
        self.failUnlessEqual(d.black_rating_value, 1513)
        self.failUnlessEqual(d.game_spec.is_rated, True)
        self.failUnlessEqual(d.game_spec.is_private, False)
        self.failUnlessEqual(d.game_spec.game_type, GameType('s'))
        self.failUnlessEqual(d.game_spec.clock, GameClock(165, 0))

    def testGSetup(self):
        (w,d) = parse_games_reply_line('112 (Setup 1129 Yunoguthi   1129 Yunoguthi ) [ uu  0   0] W:  1')
        self.failUnlessEqual(w, 'Setup')

    def testGSetup2(self):
        (w,d) = parse_games_reply_line('   2 (Setup    0 LectureBot     0 LectureBot) [ uu  0   0] B:  1')
        self.failUnlessEqual(w, 'Setup')

#noinspection PyTypeChecker
class BlockModeFilterTestCase(unittest.TestCase):
    def _callback(self, id, code, text):
        self.failUnlessIsInstance(id, int)
        self.failUnlessIsInstance(code, int)
        self.failUnlessIsInstance(text, str)
        return dict(id = id, code=code, text=text)
    def test_plainline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks("abcdefgh"),
            ("abcdefgh", []))
        self.failIf(flt.prompt_seen())
    def test_promptline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks("fics% abcdefgh"),
            ("abcdefgh", []))
        self.failUnless(flt.prompt_seen())
    def test_emptyline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(""),
            ("", []))
    def test_emptypromptline(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks("fics% "),
            ("", []))
    def test_fullblock(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam") ] ))
    def test_fullblock_and_text(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "ala"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"
                + block_codes.BLOCK_END
                + "ma kota"),
            ("alama kota", [ dict(id=33, code=99, text="param pam pam") ] ))
    def test_two_full_blocks(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "ala"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"
                + block_codes.BLOCK_END
                + "-"
                + block_codes.BLOCK_START + "44"
                + block_codes.BLOCK_SEPARATOR + "2"
                + block_codes.BLOCK_SEPARATOR + "taram pam wam"
                + block_codes.BLOCK_END
                + "ma kota"),
            ("ala-ma kota", [
                dict(id=33, code=99, text="param pam pam"),
                dict(id=44, code=2, text="taram pam wam"),
                ]))
    def test_normal_twoline_block(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam\naj ja ja jaj") ]))
    def test_normal_multiline_block(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "middle"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "  rest  "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam\nmiddle\n  rest  \naj ja ja jaj") ]))
    def test_mixed_multiline_block(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "pre rre"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("pre rre", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "middle"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "  rest  "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END
                + "postttt"),
            ("postttt", [ dict(id=33, code=99, text="param pam pam\nmiddle\n  rest  \naj ja ja jaj") ]))
    def test_multiline_and_normal(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "pre rre"
                + block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam"),
            ("pre rre", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "middle"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "  rest  "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "aj ja ja jaj"
                + block_codes.BLOCK_END
                + "-"
                + block_codes.BLOCK_START + "44"
                + block_codes.BLOCK_SEPARATOR + "2"
                + block_codes.BLOCK_SEPARATOR + "taram pam wam"
                + block_codes.BLOCK_END
                + "postttt"),
            ("-postttt", [
                dict(id=33, code=99, text="param pam pam\nmiddle\n  rest  \naj ja ja jaj"),
                dict(id=44, code=2, text="taram pam wam"),
                ]))
    def test_multiline_with_continuation(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "33"
                + block_codes.BLOCK_SEPARATOR + "99"
                + block_codes.BLOCK_SEPARATOR + "param pam pam "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                r'\     aj ja ja jaj '),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                r'\ho ho'
                + block_codes.BLOCK_END),
            ("", [ dict(id=33, code=99, text="param pam pam aj ja ja jaj ho ho") ]))
    def test_multiline_with_continuation_fingerlike(self):
        flt = BlockModeFilter(block_callback=self._callback)
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_START + "38"
                + block_codes.BLOCK_SEPARATOR + "98"
                + block_codes.BLOCK_SEPARATOR + " 1: Marcin, Warsaw, Poland. http://mekk.waw.pl"),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "2: wild fr=normal chess with randomized initial position. Great fun! I can "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "\\   play unrated wild fr game and explain the rules, just ask."),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "3: Please, say \"good game\" only if it was good game. Auto-greetings are "),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                "\\   incredibly irritating."),
            ("", []))
        self.failUnlessEqual(
            flt.handle_line_noting_callbacks(
                block_codes.BLOCK_END),
            ("", [ dict(id=38, code=98, text=""" 1: Marcin, Warsaw, Poland. http://mekk.waw.pl
2: wild fr=normal chess with randomized initial position. Great fun! I can play unrated wild fr game and explain the rules, just ask.
3: Please, say "good game" only if it was good game. Auto-greetings are incredibly irritating.
""") ]))

#noinspection PyTypeChecker
class ParseReplyCheckErrorsTestCase(unittest.TestCase):
    def _ensure_raw_error(self, got_code, got_text, *expected_classes):
        """
        Woła polecenie, sprawdza czy poleciał wyjątek i czy jest to wyjątek
        jednej z zadanych klas.
        """
        cmd, status, info = parse_fics_reply(got_code, got_text)
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        for expected_class in expected_classes:
            self.failUnlessIsInstance(info, expected_class)
        return info
    def _ensure_error(self, got_code, got_text, *expected_classes):
        """
        Jak _ensure_raw_error ale dorzuca FicsCommandException do sprawdzanych
        wyjątków - tego oczekujemy prawie zawsze
        """
        info = self._ensure_raw_error(got_code, got_text, *expected_classes)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        return info
    def test_bad_handle(self):
        exc = self._ensure_error(48, "'%s' is not a valid handle.", errors.UnknownPlayer)
        self.failUnlessEqual(exc.player_name, "%s")
    def test_bad_handle_normal(self):
        exc = self._ensure_error(48, "There is no player matching the name qzqz.", errors.UnknownPlayer)
        self.failUnlessEqual(exc.player_name, "qzqz")
    def test_bad_command(self):
        self._ensure_error(512, "sk: Command not found.", errors.UnknownFicsCommand)
    def test_bad_seek(self):
        self._ensure_error(155, "No such board: krowa", errors.BadFicsCommandParameters)
    def test_bad_params(self):
        self._ensure_error(513, """Command:  news
Purpose:  list recent news items -OR- display details of a news item
Usage:    news [all|#[-#]]
Examples: news; news all; news 11; news 35-50""", errors.BadFicsCommandParameters)
    def test_ambiguous_command(self):
        self._ensure_error(514, 'Ambiguous command "su". Matches: sublist summon',
                           errors.AmbiguousFicsCommand, errors.UnknownFicsCommand)
    def test_assess_not_playing(self):
        self._ensure_error(15, 'You are not playing a game.', errors.AttemptToActOnNotPlayedGame)
    def test_guest_channel_tell(self):
        self._ensure_error(132, 'Only registered users may send tells to channels other than 4, 7 and 53.',
                           errors.InsufficientPermissions, errors.TrueAccountRequired)
    def test_noblock_marker(self):
        self._ensure_raw_error(519, '', errors.MissingBlockMarkers, errors.FicsProtocolError)
    def test_e2e4(self):
        self._ensure_error(518, 'You are not playing or examining a game.',
                           errors.AttemptToActOnNotPlayedGame)
    def test_wrong_params_addlist(self):
        self._ensure_error(513, """Command:  addlist
Purpose:  add information to a list
Usage:    addlist list information
Alt:      +list information
Examples: addlist noplay Friar; +noplay Friar 
""", errors.BadFicsCommandParameters)
    def test_very_long_message(self):
        # message veeerylongstring resulted in
        # fics% ^U0^V519^V^W
        # ^U100^V97^VLogging you out.
        self._ensure_error(520, "",
                           errors.FicsCommandException, errors.BadFicsCommandSyntax)
    def test_guest_message(self):
        raise SkipTest
        self._ensure_error(74, '''Only registered players can use the messages command.
''',
                           errors.TrueAccountRequired)

#noinspection PyTypeChecker
class ParseReplyTestCase(unittest.TestCase):
    def test_handle(self):
        cmd, status, info = parse_fics_reply(
            48,
            """-- Matches: 100 player(s) --
MAd             MADADDS         MADAGASCAROV    madalasriharsha madam           madamdede       Madamspank      madandy         MadArab         madas           madatchess      madaxe          MadBadCat       madbarber       madbishopmelun
mada            madadh          MadagascarX     madalin         MADAMADA        madamebutterfly madamus         madangry        Madaranipuni    madasabadger    MADatlas        madaxeman       MadBadger       madbawl         MadBison
madaboutchess   MadaElshereif   Madahda         madalina        MadaMadaDane    MadameJohn      madamx          Madani          madarasharingan madasafish      madattack       madaxy          MadBadRambo     MadBeans
Madaboutcycling Madafaka        madairman       MadalinaMAnusca madamadamada    MadameSparkle   madamxx         madAnne         madarbozorg     Madasawheel     madatter        madaz           madbalger       MadBiker
MadAboutH       madafakaru      Madak           Madaline        madaman         madami          madan           madantzoy       MadArmenian     madashell       madaus          Madazo          Madball         madbikerpa
madaboutyou     madafakarul     madakram        Madalitso       Madamax         madamimadam     madana          MADAR           Madart          madasigid       MadAussie       MadAzz          madballster     madbiotic
madachab        madagascar      madalasridhar   madalyne        Madamboevarix   madamsm         MADANDAN        Madara          madartink       madasmsm        madawg          madB            madbananas      MadBishop
""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "handles")
        self.failUnlessIsInstance(info, ListContents)
        self.failUnlessEqual(len(info.items), 100)
        self.failUnlessEqual(info.items[0], PlayerName('MAd'))
        self.failUnlessEqual(info.items[0].name, 'MAd')
        self.failUnlessEqual(info.items[1], PlayerName('MADADDS'))
        self.failUnlessEqual(info.items[-1], PlayerName('MadBishop'))
    def test_date(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_DATE,
            """Local time     - Tue Jan  3, 02:29 EURCST 2012
Server time    - Tue Jan  3, 00:29 PST 2012
GMT            - Tue Jan  3, 08:29 GMT 2012""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "date")
        self.failUnlessEqual(info, FicsDateInfo(
            local_zone_name = "EURCST",
            server_zone_name = "PST",
            gmt_zone_name = "GMT",
            server=datetime.datetime(2012,1,3,0,29,0),
            local=datetime.datetime(2012,1,3,2,29,0),
            gmt=datetime.datetime(2012,1,3,8,29,0),
        ))
    def test_observe_correct(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_OBSERVE,
            load_parse_data_file("observe-normal.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "observe")
        self.failUnlessEqual(info.game_no, 92)
        self.failUnlessEqual(info.white_name, PlayerName('Motyl'))
        self.failUnlessEqual(info.white_rating_value, 1857)
        self.failUnlessEqual(info.black_name, PlayerName('Aretus'))
        self.failUnlessEqual(info.black_rating_value, 1907)
        self.failUnlessEqual(info.game_spec.is_rated, True)
        self.failUnlessEqual(info.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(info.game_spec.clock,
                             GameClock(base_in_minutes=15,inc_in_seconds=10))
        self.failUnlessEqual(info.game_spec.is_private, False)
        is12 = info.initial_style12
        self.failUnless(isinstance(is12, style12.Style12))
        self.failUnlessEqual(str(is12), "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 92 Motyl Aretus 0 15 10 39 39 900 900 1 none (0:00) none 0 0 0")
    def test_observe_private(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_OBSERVE,
            "Sorry, game 125 is a private game")
        self.failIf(status)
        self.failUnlessEqual(cmd, "observe")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.FicsCommandExecutionException)
        self.failUnlessIsInstance(info, errors.AttemptToAccessPrivateGame)
        # TODO: test exception class and info
    def test_observe_bad_style12(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_OBSERVE,
            """You are now observing game 92.
Game 92: Motyl (1857) Aretus (1907) rated standard 15 10

<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 92 Motyl Aretus 0 15 10 39 39 900 900 1 none (-:00) none 0 0 0
""")
        self.failIf(status)
        self.failUnlessEqual(cmd, "observe")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsClientException)
        self.failUnlessIsInstance(info, errors.BadStyle12Format)
        # TODO:
        #self.failUnlessIsInstance(info, errors.FicsCommandException)
        #self.failUnlessIsInstance(info, errors.FicsCommandExecutionException)
        #self.failUnlessIsInstance(info, errors.AttemptToAccessPrivateGame)
    def test_unobserve_correct(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_UNOBSERVE,
            "Removing game 124 from observation list.")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "unobserve")
        self.failUnlessEqual(info, GameReference(game_no=124))
    def test_unobserve_logic_fail(self):
        for line in [
            "You are not observing game 13.",
            "You are not observing any games.",
        ]:
            cmd, status, info = parse_fics_reply(
                block_codes.BLKCMD_UNOBSERVE,
                line)
            self.failIf(status)
            self.failUnlessEqual(cmd, "unobserve")
            self.failUnlessIsInstance(info, errors.AttemptToActOnNotUsedGame)
    def test_unobserve_bad_syntax(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_UNOBSERVE,
            "Blah.")
        self.failIf(status)
        self.failUnlessEqual(cmd, "unobserve")
        self.failUnlessIsInstance(info, errors.ReplyParsingException)
    def test_games_correct(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            load_parse_data_file("games.lines")
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "games")
        games = info.games
        examines = info.examines
        setups = info.setups
        self.failUnlessIsInstance(games, list)
        self.failUnlessIsInstance(examines, list)
        self.failUnlessIsInstance(setups, list)
        # TODO: check funny mismatch between actual count in games output
        #       and count reported by FICS in summary (in the sample
        #       we use here there are 260 games, 8 examines and 1 setup,
        #       and FICS summarizes it as 267 games)
        self.failUnlessEqual(len(games), 260, "Games count mismatch")
        self.failUnlessEqual(len(examines), 8)
        self.failUnlessEqual(len(setups), 1)
        for g in games:
            self.failUnlessIsInstance(g, PlayedGame)
            self.failUnlessIsInstance(g.game_no, int)
            self.failUnlessIsInstance(g.white_truncated_name, PlayerName)
            self.failUnlessIsInstance(g.black_truncated_name, PlayerName)
            self.failUnlessIsInstance(g.white_rating_value, int)
            self.failUnlessIsInstance(g.black_rating_value, int)
            self.failUnlessIsInstance(g.game_spec, GameSpec)
            self.failUnlessIsInstance(g.game_spec.is_private, bool)
            self.failUnlessIsInstance(g.game_spec.is_rated, bool)
            self.failUnlessIsInstance(g.game_spec.game_type, GameType)
            self.failUnlessIsInstance(g.game_spec.clock, GameClock)
        for g in examines:
            self.failUnlessIsInstance(g, ExaminedGame)
            self.failUnlessIsInstance(g.game_no, int)
        for g in setups:
            self.failUnlessIsInstance(g, SetupGame)
            self.failUnlessIsInstance(g.game_no, int)
        self.failUnlessEqual(
            examines[0],
            ExaminedGame(game_no=1)
        )
        self.failUnlessEqual(
            examines[3],
            ExaminedGame(game_no=155)
        )
        self.failUnlessEqual(
            setups[0],
            SetupGame(game_no=233)
        )
        # TODO: functions to decode short player name into long one
        self.failUnlessEqual(
            games[0],
            PlayedGame(
                game_no=8,
                white_truncated_name=PlayerName('GuestCNQG'), white_rating_value=0,
                black_truncated_name=PlayerName('GuestBFQS'), black_rating_value=0,
                game_spec=GameSpec(
                    game_type=GameType('s'),
                    is_private=False, is_rated=False,
                    clock=GameClock(10,10))))
        self.failUnlessEqual(
            games[94],
            PlayedGame(
                game_no=239,
                white_truncated_name=PlayerName('Waltherion'), white_rating_value=1133,
                black_truncated_name=PlayerName('LordoftheP'), black_rating_value=1200, 
                game_spec=GameSpec(
                    game_type=GameType('b'),
                    is_private=True, is_rated=True,
                    clock=GameClock(5,0))))
        self.failUnlessEqual(
            games[110],
            PlayedGame(
                game_no=146,
                white_truncated_name=PlayerName('Niloz'), white_rating_value=1262,
                black_truncated_name=PlayerName('papier'), black_rating_value=1220,
                game_spec=GameSpec(
                    game_type=GameType('b'),
                    is_private=False, is_rated=True,
                    clock=GameClock(3, 12))))
        self.failUnlessEqual(
            games[75],
            PlayedGame(
                game_no=60,
                white_truncated_name=PlayerName('asturia'), white_rating_value=1840,
                black_truncated_name=PlayerName('GuestNVLL'), black_rating_value=0,
                game_spec=GameSpec(
                    game_type=GameType('s'),
                    is_private=False, is_rated=False,
                    clock=GameClock(15, 0))))
        self.failUnlessEqual(
            games[250],
            PlayedGame(
                game_no=77,
                white_truncated_name=PlayerName('twobi'), white_rating_value=1891,
                black_truncated_name=PlayerName('FiNLiP'), black_rating_value=2074,
                game_spec=GameSpec(
                    game_type=GameType('L'),
                    is_private=False, is_rated=True,
                    clock=GameClock(3, 0))))

        # line-11
    def test_games_empty(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            "")
        self.failIf(status)
        self.failUnlessEqual(cmd, "games")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)
    def test_games_ugly(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            """
  1 (Exam.    0 Spiro          0 Najdorf   ) [ uu  0   0] W:  3
 34 ++++ xmattbbb    ++++ GuestSGYZ  [ bu  2  12]   2:22 -  2:55 (33-35) W: 10
 some ugly text
 162 1563 sgmza       1611 seva       [ br  5   0]   2:20 -  2:55 (35-21) B: 19

  3 games displayed.""")
        self.failIf(status)
        self.failUnlessEqual(cmd, "games")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)
    def test_games_truncated_no_summary(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_GAMES,
            """
 34 ++++ xmattbbb    ++++ GuestSGYZ  [ bu  2  12]   2:22 -  2:55 (33-35) W: 10
 162 1563 sgmza       1611 seva       [ br  5   0]   2:20 -  2:55 (35-21) B: 19""")
        self.failIf(status)
        self.failUnlessEqual(cmd, "games")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)

    def test_finger_empty(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            "")
        self.failIf(status)
        self.failUnlessEqual(cmd, "finger")
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.ReplyParsingException)
    def test_finger_badname(self):
        for error_note, player_name in [
            ("'thebestplayerinthe' is not a valid handle.", "thebestplayerinthe"),
            ("There is no player matching the name guestzzzz.", "guestzzzz"),
        ]:
            cmd, status, info = parse_fics_reply(
                block_codes.BLKCMD_FINGER,
                error_note)
            self.failIf(status)
            self.failUnlessEqual(cmd, "finger")
            self.failUnlessIsInstance(info, Exception)
            self.failUnlessIsInstance(info, errors.FicsCommandException)
            self.failUnlessIsInstance(info, errors.UnknownPlayer)
            self.failUnlessEqual(info.player_name, player_name)
    def test_finger_simple(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            load_parse_data_file("finger-mek.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "finger")
        assert_dicts_equal(self, info, FingerInfo(
            name="Mek",
            results={
                GameType('Standard'): ResultStats(rating=PlayerRating(1606, rd=Decimal('350.0')), best=None, wins_count=0, losses_count=1, draws_count=0 ),
                },
            plan=[
            ]))
    def test_finger_complicated(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            load_parse_data_file_patching_continuations("finger-mekk.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "finger")
        assert_dicts_equal(self, info, FingerInfo(
            name="Mekk",
            results={
                GameType('Atomic'): ResultStats(best=None, wins_count=23, draws_count=1, losses_count=50, rating=PlayerRating(1525, rd=Decimal('159.2'))),
                GameType('Blitz'): ResultStats(best=1522, wins_count=3900, draws_count=410, losses_count=5797, rating=PlayerRating(1342, rd=Decimal('42.4'))),
                GameType('Bughouse'): ResultStats(best=None, wins_count=3, draws_count=0, losses_count=5, rating=PlayerRating(1035, rd=Decimal('350.0'))),
                GameType('Crazyhouse'): ResultStats(best=1495, wins_count=73, draws_count=0, losses_count=235, rating=PlayerRating(1451, rd=Decimal('99.8'))),
                GameType('Lightning'): ResultStats(best=1116, wins_count=15, draws_count=1, losses_count=115, rating=PlayerRating(1495, rd=Decimal('233.0'))),
                GameType('Losers'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=6, rating=PlayerRating(1674, rd=Decimal('350.0'))),
                GameType('Standard'): ResultStats(best=1935, wins_count=730, draws_count=156, losses_count=913, rating=PlayerRating(1759, rd=Decimal('68.8'))),
                GameType('Suicide'): ResultStats(best=None, wins_count=1, draws_count=0, losses_count=14, rating=PlayerRating(1384, rd=Decimal('278.1'))),
                GameType('Wild'): ResultStats(best=1875, wins_count=287, draws_count=31, losses_count=457, rating=PlayerRating(1683, rd=Decimal('100.5')))
            },
            plan=[
                'Marcin Kasperski, Warsaw, Poland. http://mekk.waw.pl',
                'wild fr=normal chess with randomized initial position. Great fun! I can play unrated wild fr game and explain the rules, just ask.',
                'Please, say "good game" only if it was good game. Auto-greetings are incredibly irritating.',
                'If I happen to ignore your tells, most likely I am playing from my mobile phone (btw, http://yafi.pl is a great mobile fics client)',
                'Correspondence chess is great if you have little time, but prefer thinking games. My tips:  http://schemingmind.com for web-based play, http://e4ec.org if you want to stay with email. On schemingmind you can also learn atomic, crazyhouse, wild fr and other variants - without time pressure.',
                'I wrote and maintain WatchBot. http://mekk.waw.pl/mk/watchbot',
                'FICS enhancements ideas:  http://mekk.waw.pl/mk/eng/chess/art/ideas_fics',
                'How to write a FICS bot: http://blog.mekk.waw.pl/archives/7-How-to-write-a-FICS-bot-part-I.html',
                'Szachowy slownik polsko-angielski: http://mekk.waw.pl/mk/szachy/art/ang_terminologia',
                'Polski podrecznik FICS: http://mekk.waw.pl/mk/szachy/art/fics_opis',
                ]))
    def test_finger_guest(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_FINGER,
            load_parse_data_file_patching_continuations("finger-guest.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "finger")
        assert_dicts_equal(self, info, FingerInfo(
            name="GuestVNCT",
            results=dict(),
            plan=[
            ]))

    def test_seek_empty(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SEEK,
            "Your seek has been posted with index 95."
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "seek")
        self.failUnlessEqual(info, SeekRef(95))
    def test_seek_seen(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SEEK,
            """Your seek has been posted with index 25."
(3 player(s) saw the seek.)"""
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "seek")
        self.failUnlessEqual(info, SeekRef(25))
    def test_seek_updated(self):
        # TODO: check this syntax (not sure whether first line may happen alone)
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SEEK, # ??? TODO: spr czy to ten kod
            """Updating seek ad 35; rating range now 1340-1344.

Your seek has been posted with index 35.
(1 player(s) saw the seek.)"""
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "seek")
        self.failUnlessEqual(info, SeekRef(35))
    def test_sought(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SOUGHT,
            """ 90 2663 stayalive(C)        3   0 unrated suicide                0-9999
115 2555 Sordid(C)           3   0 unrated atomic                 0-9999 f
119 ++++ GuestQDXP           5   0 unrated blitz      [white]     0-9999 m
136 ++++ GuestKNGV           2   0 unrated lightning              0-9999 f
146 ++++ GuestYGSC          20  30 unrated standard               0-9999 m
153 ++++ DeepTougtII         3   0 unrated blitz                  0-9999 f
11 ads displayed."""
        )
        self.failUnless(status)
        self.failUnlessEqual(cmd, "sought")
        assert_tables_equal(self, info, [
                Seek(seek_no=90,
                     player=PlayerName('stayalive'), 
                     player_rating_value=2663, 
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('suicide'),
                                        clock=GameClock(3, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=115,
                     player=PlayerName('Sordid'), 
                     player_rating_value=2555, 
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('atomic'),
                                        clock=GameClock(3, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=119,
                     player=PlayerName('GuestQDXP'), 
                     player_rating_value=0, 
                     is_manual=True,
                     using_formula=False,
                     color=Color("white"),
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(5, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=136,
                     player=PlayerName('GuestKNGV'), 
                     player_rating_value=0, 
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('lightning'),
                                        clock=GameClock(2, 0),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=146,
                     player=PlayerName('GuestYGSC'), 
                     player_rating_value=0, 
                     is_manual=True,
                     using_formula=False,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('standard'),
                                        clock=GameClock(20, 30),
                                        is_rated=False,
                                        is_private=False)),
                Seek(seek_no=153,
                     player=PlayerName('DeepTougtII'), 
                     player_rating_value=0, 
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(3, 0),
                                        is_rated=False,
                                        is_private=False)),
                ])

    def test_sought_sb(self):
        cmd, status, info = parse_fics_reply(
            block_codes.BLKCMD_SOUGHT,
            """ 22 1298  Brewwhaha           3   3 rated   blitz                  0-9999 f
 61 1679  Frankkenstein      20   5 rated   standard            1650-9999 
 63 1977  antoni              6   0 rated   blitz                  0-9999 m
106 1719  ifufocop            3   0 rated   crazyhouse          1300-1670 
114 1776  Embedics            3  12 rated   wild/fr                0-9999 
115 1298  SylvainSLA          8  10 rated   blitz                  0-9999 
180 1243  taniuzhka           4   0 unrated blitz               1000-1999 mf
8 ads displayed.
""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "sought")
        assert_tables_equal(self, info, [
                Seek(seek_no=22,
                     player=PlayerName('Brewwhaha'), 
                     player_rating_value=1298, 
                     is_manual=False,
                     using_formula=True,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(3, 3),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=61,
                     player=PlayerName('Frankkenstein'), 
                     player_rating_value=1679, 
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     # TODO
                     # min_rating=1650
                     # max_rating=9999
                     game_spec=GameSpec(game_type=GameType('standard'),
                                        clock=GameClock(20, 5),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=63,
                     player=PlayerName('antoni'), 
                     player_rating_value=1977, 
                     is_manual=True,
                     using_formula=False,
                     color=None,
                     # TODO
                     # min_rating=1650
                     # max_rating=9999
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(6, 0),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=106,
                     player=PlayerName('ifufocop'), 
                     player_rating_value=1719, 
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     # TODO
                     #min_rating=1300,
                     #max_rating=1670,
                     game_spec=GameSpec(game_type=GameType('crazyhouse'),
                                        clock=GameClock(3, 0),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=114,
                     player=PlayerName('Embedics'), 
                     player_rating_value=1776, 
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     # TODO
                     #min_rating=0,
                     #max_rating=9999,
                     game_spec=GameSpec(game_type=GameType('wild/fr'),
                                        clock=GameClock(3, 12),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=115,
                     player=PlayerName('SylvainSLA'), 
                     player_rating_value=1298, 
                     is_manual=False,
                     using_formula=False,
                     color=None,
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(8, 10),
                                        is_rated=True,
                                        is_private=False)),
                Seek(seek_no=180,
                     player=PlayerName('taniuzhka'), 
                     player_rating_value=1243, 
                     is_manual=True,
                     using_formula=True,
                     color=None,
                     # TODO
                     # min_rating=1000
                     # max_rating=1999
                     game_spec=GameSpec(game_type=GameType('blitz'),
                                        clock=GameClock(4, 0),
                                        is_rated=False,
                                        is_private=False)),
  ])

    def test_channel_subscribed(self):
        cmd, status, info = parse_fics_reply(
            12, '[1] added to your channel list.')
        self.failUnless(status)
        self.failUnlessEqual(cmd, "addlist")
        self.failUnlessEqual(info,
                             ChannelRef(channel=1))

    # TODO: tests for more commands

#noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker
class GameInfoTestCase(unittest.TestCase):

    def test_simple(self):
        text = """Game 295: Game information.
  anandkvs (2063) vs donnadistruttiva (1960) rated Standard game.
  Time controls: 5400 30
  Time of starting: Sat Sep 15, 23:34 PDT 2012
  White time 1:25:27    Black time 1:23:58
  The clock is not paused
  16 halfmoves have been made.
  Fifty move count started at halfmove 13 (97 halfmoves until a draw).
  White may castle both kingside and queenside.
  Black may castle both kingside and queenside.
  Double pawn push didn't occur.
"""
        cmd, status, info = parse_fics_reply(
            46, text)
        self.failUnless(status)
        self.failUnlessEqual(cmd, "ginfo")
        self.failUnlessIsInstance(info, GameInfo)
        self.failUnlessIsInstance(info.game_no, int)
        self.failUnlessIsInstance(info.white_name, PlayerName)
        self.failUnlessIsInstance(info.black_name, PlayerName)
        self.failUnlessIsInstance(info.white_rating_value, int)
        self.failUnlessIsInstance(info.black_rating_value, int)
        self.failUnlessIsInstance(info.game_spec, GameSpec)
        self.failUnlessIsInstance(info.game_spec.is_private, bool)
        self.failUnlessIsInstance(info.game_spec.is_rated, bool)
        self.failUnlessIsInstance(info.game_spec.game_type, GameType)
        self.failUnlessIsInstance(info.game_spec.clock, GameClock)
        self.failUnlessEqual(info.game_no, 295)
        self.failUnlessEqual(info.white_name, 'anandkvs')
        self.failUnlessEqual(info.black_name, 'donnadistruttiva')
        self.failUnlessEqual(info.white_rating_value, 2063)
        self.failUnlessEqual(info.black_rating_value, 1960)
        self.failUnlessEqual(info.game_spec.is_private, False)
        self.failUnlessEqual(info.game_spec.is_rated, True)
        self.failUnlessEqual(info.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(info.game_spec.clock, GameClock(90,30))
        self.failUnlessEqual(info.start_time, datetime.datetime(2012, 9, 15, 23, 34, 0))

    def test_simple_eurcst(self):
        text = """Game 295: Game information.
  anandkvs (2063) vs donnadistruttiva (1960) rated Standard game.
  Time controls: 5400 30
  Time of starting: Sat Sep 15, 23:34 EURCST 2012
  White time 1:25:27    Black time 1:23:58
  The clock is not paused
  16 halfmoves have been made.
  Fifty move count started at halfmove 13 (97 halfmoves until a draw).
  White may castle both kingside and queenside.
  Black may castle both kingside and queenside.
  Double pawn push didn't occur.
"""
        cmd, status, info = parse_fics_reply(
            46, text)
        self.failUnless(status)
        self.failUnlessEqual(cmd, "ginfo")
        self.failUnlessIsInstance(info, GameInfo)
        self.failUnlessIsInstance(info.game_no, int)
        self.failUnlessIsInstance(info.white_name, PlayerName)
        self.failUnlessIsInstance(info.black_name, PlayerName)
        self.failUnlessIsInstance(info.white_rating_value, int)
        self.failUnlessIsInstance(info.black_rating_value, int)
        self.failUnlessIsInstance(info.game_spec, GameSpec)
        self.failUnlessIsInstance(info.game_spec.is_private, bool)
        self.failUnlessIsInstance(info.game_spec.is_rated, bool)
        self.failUnlessIsInstance(info.game_spec.game_type, GameType)
        self.failUnlessIsInstance(info.game_spec.clock, GameClock)
        self.failUnlessEqual(info.game_no, 295)
        self.failUnlessEqual(info.white_name, 'anandkvs')
        self.failUnlessEqual(info.black_name, 'donnadistruttiva')
        self.failUnlessEqual(info.white_rating_value, 2063)
        self.failUnlessEqual(info.black_rating_value, 1960)
        self.failUnlessEqual(info.game_spec.is_private, False)
        self.failUnlessEqual(info.game_spec.is_rated, True)
        self.failUnlessEqual(info.game_spec.game_type, GameType('standard'))
        self.failUnlessEqual(info.game_spec.clock, GameClock(90,30))
        self.failUnlessEqual(info.start_time, datetime.datetime(2012,9,15,23,34,0))


    def test_examine(self):
        cmd, status, info = parse_fics_reply(
            46, """Game 95: Game information.

  MAd is examining MAd vs pgv.
  59 halfmoves have been made.
  Fifty move count started at halfmove 59 (100 moves until a draw).
  White may castle both kingside and queenside.
  Black may not castle.
  Double pawn push didn't occur.
""")
        self.failUnless(status)
        self.failUnlessEqual(cmd, "ginfo")
        self.failUnlessIsInstance(info, ExaminedGameExt)
        self.failUnlessEqual(info.examiner,"MAd")
        self.failUnlessEqual(info.white,"MAd")
        self.failUnlessEqual(info.black,"pgv")
        self.failUnlessEqual(info.game_no,95)

    def test_wrong(self):
        cmd, status, info = parse_fics_reply(
            46, "The current range of game numbers is 1 to 780.\n")
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.NoSuchGame)

    def test_wrong_observe(self):
        cmd, status, info = parse_fics_reply(
            80, "There is no such game.\n")
        self.failIf(status)
        self.failUnlessIsInstance(info, Exception)
        self.failUnlessIsInstance(info, errors.FicsCommandException)
        self.failUnlessIsInstance(info, errors.NoSuchGame)

    def test_who_1(self):
        raise SkipTest
        info = parse_who_reply(
            load_parse_data_file("who.lines"))
        raise NotImplementedError() # Testy co ma wyjść

    def test_who_2(self):
        raise SkipTest
        cmd, status, info = parse_fics_reply(
            146, load_parse_data_file("who.lines"))
        self.failUnless(status)
        self.failUnlessEqual(cmd, "who")
        raise NotImplementedError() # Testy co ma wyjść

class NotificationTestCase(unittest.TestCase):

    def test_arrival(self):
        w, d = info_parser.parse_fics_line(
            'Notification: Mekk has arrived.')
        self.failUnlessEqual(w, 'watched_user_connected')
        self.failUnlessEqual(d, PlayerName('Mekk'))

    def test_departure(self):
        w, d = info_parser.parse_fics_line(
            'Notification: Mekk has departed.')
        self.failUnlessEqual(w, 'watched_user_disconnected')
        self.failUnlessEqual(d, PlayerName('Mekk'))

    def test_arrival_nt(self):
        w, d = info_parser.parse_fics_line(
            'Notification: FiNLiP has arrived and isn\'t on your notify list.')
        self.failUnlessEqual(w, 'watching_user_connected')
        self.failUnlessEqual(d, PlayerName('FiNLiP'))

    def test_departure_nt(self):
        w, d = info_parser.parse_fics_line(
            'Notification: FiNLiP has departed and isn\'t on your notify list.')
        self.failUnlessEqual(w, 'watching_user_disconnected')
        self.failUnlessEqual(d, PlayerName('FiNLiP'))

# Notification: FiNLiP has arrived and isn't on your notify list.


    def test_auto_logout(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            '''**** Auto-logout because you were idle more than 60 minutes. ****''')
        

class ExamineTestCase(unittest.TestCase):

    def test_mex(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'puzzlebot is now an examiner of game 212.')
    def test_stop(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'puzzlebot stopped examining game 212.')
    def test_noex(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'Game 419 (which you were observing) has no examiners.')

    def test_move(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'Game 212: chudzida moves: Qg5')
    def test_move2(self):
        raise SkipTest
        w, d = info_parser.parse_fics_line(
            'Game 212: chudzida moves: e6')


if __name__ == "__main__":
    # ładuje moduły psujące debugging przez łdowanie decorators
    #import nose
    #nose.main()
    import unittest
    unittest.main()

# TODO: reply to tell:
# Your communication has been queued for 1 second(s).

# TODO: consider handling those:
#
# (intro)
#
# You have 16 messages (0 unread).
# Present company includes: MAd TScheduleBot Valiantangel WatchBot.
# You have 3 adjourned games.
#
#

