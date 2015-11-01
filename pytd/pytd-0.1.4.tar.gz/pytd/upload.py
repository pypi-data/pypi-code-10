import io
import gzip
import time
import uuid
import msgpack

import logging
logger = logging.getLogger(__name__)

def frame_chunks(frame, chunksize):
    def _chunk_records(chunk):
        for _, row in chunk.iterrows():
            row.dropna(inplace=True)
            yield dict(row)
    # split frame into chunks
    for i in range((len(frame) - 1) // chunksize + 1):
        chunk = frame[i * chunksize : i * chunksize + chunksize]
        yield _chunk_records(chunk)


class StreamingUpload(object):
    def __init__(self, context, database, table):
        self.context = context
        self.database = database
        self.table = table

    def _gzip(self, data):
        buff = io.BytesIO()
        with gzip.GzipFile(fileobj=buff, mode='wb') as f:
            f.write(data)
        return buff.getvalue()

    def _upload(self, data):
        client = self.context.client
        data_size = len(data)
        unique_id = uuid.uuid4()
        start_time = time.time()
        elapsed = client.import_data(self.database, self.table, 'msgpack.gz', data, data_size, unique_id)
        end_time = time.time()
        logger.info('uploaded %d bytes in %.2f secs (elapsed %.3f)', data_size, end_time - start_time, elapsed)

    def upload_frame(self, frame, chunksize=100000):
        for chunk in frame_chunks(frame, chunksize):
            packer = msgpack.Packer(autoreset=False)
            for record in chunk:
                packer.pack(record)
            self._upload(self._gzip(packer.bytes()))
