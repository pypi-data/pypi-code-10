from collections import defaultdict
import inspect


class Trans:
    arg_dict = defaultdict(list)
    arg_man_dict = defaultdict(list)

    command = ''
    p_file_list = []

    def add(self, key, value, *n_subargs, **others):
        # Adding mapping
        val = [value, n_subargs[0] if len(n_subargs) is 1 and n_subargs[0] > 0 else 0]
        if key in self.arg_dict:
            self.arg_dict[key].append(val)
        else:
            self.arg_dict[key] = val

        # Adding man
        if 'man' in others:
            if self.arg_man_dict[key] is None:
                self.arg_man_dict[key] = others['man']
            else:
                self.arg_man_dict[key].append(others['man'])
        else:
            self.arg_man_dict[key].append(str(key) + " - No usage info...")

    def help_message(self):
        for man in self.arg_man_dict:
            if self.arg_man_dict[man] is not None:
                for man_line in self.arg_man_dict[man]:
                    print "\t", man_line

    def walk(self, args):
        it = iter(args)
        for arg in it:
            if arg in self.arg_dict:
                mapped = self.arg_dict[arg]
                n = mapped[1]
                if inspect.ismethod(mapped[0]):
                    args = ()
                    for i in range(n):
                        args += (next(it),)
                    mapped[0](*args)
                else:
                    self.command += ' ' + mapped[0]
                    if n > 0:
                        for i in range(n):
                            self.command += next(it) if mapped[0].endswith('=') else ' ' + next(it)
            else:
                self.p_file_list.append(arg)
