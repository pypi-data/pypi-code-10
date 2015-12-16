import os.path


class EventFile:
    """docstring for EventFile"""
    def __init__(self, filename):
        if os.path.isfile(filename):
            self.source = os.path.abspath(filename)
            self.ext = os.path.splitext(filename)
            self.raw = self._read()
        else:
            raise FileNotFoundError('Event file not found', filename)

    def _sniff(self, firstline):
        """Sniff the file type (creating software)"""
        if self.ext == '.evt' and firstline.startwith('Tmu'):
            self.filetype = 'BESA'
            return
        if self.ext == '.ev2':
            self.filetype = 'Neuroscan_2'
            return
        raise ValueError('Undetected type', 'Extension:' + self.ext,
                         'First Line: ' + firstline)

    def _check(self):
        """Test for consistency (all rows ahve same number of columns """
        for d in self.data:
            if len(d) != len(self.header):
                raise ValueError('Line has unexected number of elements: ', d)

    def _splitBESA(self, lines):
        """Split lines in a BESA specific way"""
        self.header = [h.trim() for h in lines[0].split('\t')]
        line2 = [d.trim() for d in lines[1].split('\t')]
        if line2[1] == '41':
            self.extra = line2
            self.timestamp = line2[2]
            lines = lines[2:]
        else:
            lines = lines[1:]
        self.data = [[d.trim() for d in l.split('\t')] for l in lines]

    def _splitNS2(self, lines):
        """split lines in a Neuroscan ev2 specific way"""
        header = 'EvtNum,EvtCode,RespCode,RespAcc,RespLatency,EvtTime'
        self.header = header.split(',')
        self.data = [[d.trim() for d in l.split()] for l in lines]

    def _split(self, lines):
        """Split lines in a fileformat dependant way and extract header"""
        self.extra = ''
        if self.filetype == 'BESA':
            self._splitBESA(lines)
        elif self.filetype == 'Neuroscan_2':
            self._splitNS2(lines)
        else:
            raise NotImplementedError('Cannot find split method for ',
                                      self.filetype)

    def _read(self):
        """Read the text from the event file into memoryi, sniffing file type
        as we go
        """
        with open(self.source, 'r') as ef:
            lines = ef.read().splitlines()
        self._sniff(lines[0])
        self._split(lines)
        self._check()


def load(filepath):
    """Load and return an EventFile object"""
    return EventFile(filepath)
