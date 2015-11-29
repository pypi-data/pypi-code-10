from io import IOBase
from rambutan3.check_args.annotation.INSTANCE_OF_WITH_PREDICATE import INSTANCE_OF_WITH_PREDICATE
from rambutan3.string.RMessageText import RMessageText


__predicate_func = lambda x: x.writable()
__predicate_description = RMessageText('writable()')

OUTPUT_STREAM = INSTANCE_OF_WITH_PREDICATE(__predicate_func, __predicate_description, IOBase)
