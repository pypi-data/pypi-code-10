from sys import argv


class ParamSeeker:
    def __init__(self, prefix='--', prefix_short='-'):
        """Things you should know, prefix and prefix_short are used to get the argument
        change the two param cautiously !!
        It is not recommended to make change !!
        :param prefix   (string)    define the full argument start
        :param prefix_short (string)    define the short term of the argument
        """
        self.args = argv[1:]
        self.arg_len = len(self.args)
        self.collection = {}
        self.prefix = prefix
        self.prefix_short = prefix_short
        self.usage_desc = ''
        self.desc = ''
        self.no_head_bind = {}
        self.has_input = False

    def set_usage_desc(self, desc):
        """
        :param desc (string)
                descriptions for the current usage declare
                display auto decided
                example:
                    app.set_usage_desc(desc="youdao [option] word")

        """
        self.usage_desc += '\t' + desc + '\n'

    def set_desc(self, desc):
        """
        :param desc (string)
                description for the whole project
                multiple use will merge
                example:
                    app.set_desc("tell you what does the word mean")

        """
        self.desc = desc

    def __param_desc_full(self):
        result = ''
        for group in self.collection:
            result += group.strip() + ' options:\n'
            for args in self.collection[group]:
                result += self.__param_desc(args)
        return result

    @staticmethod
    def __param_desc(args):
        """I don't want users to care about this part"""
        result = ''
        if args['short']:
            result += args['short'] + ', '
        result += args['param'] + '\t'
        result += args['desc']
        result += '\n'
        return result

    def print_help(self, redundancy=None):
        """Print help menu
            :param redundancy (you won't use)   just as a redundancy :) No used
        """
        return """Usage: \n{usage}\n{total_desc}\n\n{param_desc}""".format(
            usage=self.usage_desc,
            total_desc=self.desc,
            param_desc=self.__param_desc_full())

    def get_full_param(self, param=None, single_param=True, is_mark=False):
        """Get the target according to the full require
            :param param          (string)    actually this is the param head (too lazy to change the name orz)
                                    example:
                                        $ youdao --word linux

                                        Here '--word' is what I mean the 'param' , the full state
                                        if the param is None, it will return first several param
                                        in the console

                                        $ youdao linux

                                        Then, 'linux' will be seen as a no param head param,
                                        only one method is allowed to be attached to it,
                                        if more than one method is given, merge you will know


            :param single_param   (bool)      whether or not continues to see the following as the param
                                    example:
                                        $ youdao --word linux is best

                                        Here if the 'single_param' is True:
                                            which actually means:
                                                $ youdao --word 'linux is best'
                                        else:
                                            which just mean:
                                                $ youdao --word 'linux'

            :param is_mark         (bool)       whether the param head used ad a mark only
                                            example:
                                                $ youdao linux --trans

                                            Here '--trans' is used as a mark only, which means its existence
                                             is what I care
        """
        if is_mark and param in argv[1:]:
            return True
        result = ''
        if not param:
            for i in argv[1:]:
                if not i.startswith(self.prefix) and not i.startswith(self.prefix_short):
                    result += i + ' '
                else:
                    break
            return result.strip()
        if param not in argv:
            return False

        last = argv[argv.index(param):]
        if len(last) > 1:
            if single_param:
                return argv[argv.index(param) + 1]
            for i in argv[argv.index(param) + 1:]:
                if not i.startswith(self.prefix) and not i.startswith(self.prefix_short):
                    result += i + ' '
                else:
                    break
            return result.strip()
        return False

    def get_short_param(self, short_param=None, single_param=True, is_mark=False):
        if is_mark and short_param in argv[1:]:
            return True
        if short_param not in argv:
            return False

        last = argv[argv.index(short_param):]
        if len(last) > 1:
            if single_param:
                return argv[argv.index(short_param) + 1]
            result = ''
            for single in argv[argv.index(short_param) + 1:]:
                if not single.startswith(self.prefix) and not single.startswith(self.prefix_short):
                    result += single + ' '
                else:
                    break
            return result.strip()
        return False

    def seek(self, param='', short='', nullable=False, extra={}):
        """A decorator used to bind the param and its dealing method

                @app.seek('human', extra={'param_short':'h'})
                def human(wanted):
                    return 'this is human readable result'

                    Here the param 'wanted' will be the argument from the console,
                you can deal with it with your own 'human' method

        example:
                    if param='human'
                    then extra may be like:
                    {
                        'group':'General',
                        'desc':'human readable feed back',
                        'single_param':False
                    }

        :param param (string)
                the argument(s) you want to get by
        :param short (string)
                short term of your argument
        :param nullable (bool)
                whether or not allow ZERO argument which means the param is
                used as a mark
        :param extra (dict)
                extra info to confirm your desire
                options:
                    :arg group          (string)    which group to belong
                    :arg desc           (string)    description of the param
                    :arg single_param   (bool)      whether the wanted result single argument or multiple
                                                    $ youdao -w linux is fine -c ok

                                                    if single_param:
                                                        which means
                                                        $ youdao -w linux -c ok
                                                    else:
                                                        which means as it receives
        """
        def seek_wrap(wrapped):
            result = self.get_full_param(param=param,
                                         single_param=extra.get('single_param', False),
                                         is_mark=nullable) \
                     or self.get_short_param(short_param=short,
                                             single_param=extra.get('single_param', False),
                                             is_mark=nullable)
            # deal with param without head
            if not param:
                self.no_head_bind['wanted'] = result
                self.no_head_bind['bind_method'] = wrapped
                return wrapped
            target = {
                'param': param,
                'short': short,
                'desc': extra.get('desc', ''),
                'wanted': result
            }
            if not result and nullable:
                print(self.__param_desc(target))
                print(self.print_help())
            group = extra.get('group', 'General')

            target['bind_method'] = wrapped

            if group not in self.collection:
                self.collection[group] = []
            self.collection[group].append(target)
            return wrapped
        return seek_wrap

    def bind_help(self):
        result = self.get_full_param(param='--help',
                                     single_param=True,
                                     is_mark=True)
        target = {
            'param': '--help',
            'short': '-h',
            'desc': 'help',
            'wanted': result,
            'bind_method': self.print_help
        }
        if 'General' not in self.collection:
            self.collection['General'] = []
        self.collection['General'].append(target)

    @staticmethod
    def execute(func, args):
        return func(args)

    def run(self, continuous=True):
        """The whole application entry point

        :param continuous   (bool)      continuously execute all the binding methods
                                    then show all the result in the console or execute
                                    and show the result once
                                        if in your method, `print` is deployed more than `return`
                                    well, continuous=False is recommended, but somehow
                                    if you mix them in your method ... the result is not
                                    easy to control, if you can, never mind :)

            The whole process is like:
                1. check the binding list, if None, exit at once
                2. bind the help method, you may not able to set help param manually now
                3. run !
        """

        if not self.collection and not self.no_head_bind:
            print("No binding is detected !!!")
            exit(1)
        self.bind_help()

        result = ''
        no_head = self.no_head_bind
        if no_head and no_head['wanted']:
            result += self.execute(no_head['bind_method'], no_head['wanted'])
            if result:
                self.has_input = True
        # print(self.collection)
        for group in self.collection.values():
            for bind in group:
                if bind['wanted']:
                    self.has_input = True
                    temp_result = self.execute(bind['bind_method'], bind['wanted'])
                    if not continuous:
                        print(temp_result)
                    else:
                        result += str(temp_result)
        if result:
            print(result)
        if not self.has_input:
            print(self.print_help())

