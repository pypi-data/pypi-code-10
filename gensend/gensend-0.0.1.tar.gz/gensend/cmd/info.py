from ..patterns import PatternList
from ..providers import ProviderList, DefaultProviders
from ..send import Sender


class InfoCommand(object):
    def __call__(self, ns):
        return ns.formatter.iterout(self.execute(ns))

    def execute(self, ns):
        providers = ProviderList() + DefaultProviders
        patterns = PatternList(ns.commands[:-1])
        sender = None

        if len(ns.commands[-1:]):
            sender = Sender(ns.commands[-1:].pop())

        if ns.providers:
            providers += ProviderList.from_str(ns.providers)
        if ns.patterns:
            patterns += PatternList.from_path(ns.patterns)

        for n in ns.__dict__.items():
            yield ['arg', n[0], n[1]]
        for provider in providers:
            yield ['provider', provider]
        for pattern in patterns:
            yield ['pattern', pattern]
        yield ['sender', sender]
