from django.db import connection, transaction
from django.db.utils import ProgrammingError
from datetime import date


def get_next_id(sequence, settings):

  def getnext(sequence):
    cursor.execute("SELECT nextval('{}')".format(sequence))
    row = cursor.fetchone()
    return row

  cursor = connection.cursor()
  sid = transaction.savepoint()
  try:
    row = getnext(sequence)
    transaction.savepoint_commit(sid)
  except ProgrammingError:
    transaction.savepoint_rollback(sid)
    ## Sequence probably doesn't exist, lets create it
    cursor.execute("CREATE SEQUENCE {}".format(sequence))
    row = getnext(sequence)

  today = date.today()

  fmt = getattr(settings, '{}_FORMAT'.format(sequence.upper()), '{id}')
  return fmt.format(id=row[0], year=today.strftime('%y'), YEAR=today.strftime('%Y'), month=today.strftime('%m'))
