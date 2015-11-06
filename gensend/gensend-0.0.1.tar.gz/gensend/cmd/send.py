from ..gen import Generator
from ..patterns import PatternList
from ..providers import ProviderList, DefaultProviders
from ..send import Sender


class SendCommand(object):
    def __call__(self, ns):
        return ns.formatter.iterout(self.execute(ns))

    def execute(self, ns):
        assert 0 != len(ns.commands), \
            'Usage is: gensend send "pattern1" "pattern2" "...pattern%{INT}" ' \
            '"scheme://netloc/path;parameters?query#fragment"'

        providers = ProviderList() + DefaultProviders
        generator = Generator()
        patterns = PatternList(ns.commands[:-1])
        sender = Sender(ns.commands[-1:].pop())

        if ns.providers:
            providers += ProviderList.from_str(ns.providers)
        if ns.patterns:
            patterns += PatternList.from_path(ns.patterns)
        if not ns.noseed:
            generator.seed_providers(ns.seed)
        generator.add_providers(providers)

        with sender.session() as s:
            for generatable in generator.generate(patterns, rounds=ns.number):
                data = generatable()
                s.send(data)
                yield data
