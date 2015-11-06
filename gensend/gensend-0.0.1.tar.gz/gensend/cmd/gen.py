from ..gen import Generator
from ..patterns import PatternList
from ..providers import ProviderList, DefaultProviders


class GenCommand(object):
    def __call__(self, ns):
        return ns.formatter.iterout(self.execute(ns))

    def execute(self, ns):
        providers = ProviderList() + DefaultProviders
        generator = Generator()
        patterns = PatternList(ns.commands[:])

        if ns.providers:
            providers += ProviderList.from_str(ns.providers)
        if ns.patterns:
            patterns += PatternList.from_path(ns.patterns)
        if not ns.noseed:
            generator.seed_providers(ns.seed)

        assert len(patterns) and len(providers), \
            'Usage is: gensend gen "pattern1" "pattern2" "...pattern%{INT}"'

        generator.add_providers(providers)

        for generatable in generator.generate(patterns, rounds=ns.number):
            yield generatable()
