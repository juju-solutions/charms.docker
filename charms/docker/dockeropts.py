from charmhelpers.core import unitdata


class DockerOpts:
    '''
    DockerOptsManager - A Python class for managing the DEFAULT docker
    options on a daemon dynamically. As a docker daemon integrates with more
    services it becomes quickly unweidly to just "template and go" for this
    solution. Having a data bag to stuff in options/multioptions and render to
    a template is a far nicer solution.

    THe underlying data-provider is backed by a SQLITE database on each unit,
    tracking the dictionary, provided from the 'charmhelpers' python package.

    Summary:
    opts = DockerOpts()
    opts.add('bip', '192.168.22.2')
    opts.to_s()
    '''

    def __init__(self, opts_path=None):
        self.db = unitdata.kv()
        if not self.db.get('docker_opts'):
            self.data = {}
        else:
            self.data = self.db.get('docker_opts')

    def __save(self):
        self.db.set('docker_opts', self.data)

    def add(self, key, value):
        '''
        Adds data to the map of values for the DockerOpts file.
        Supports single values, or "multiopt variables". If you
        have a flag only option, like --tlsverify, set the value
        to None.

        eg:
        opts.add('label', 'foo')
        opts.add('label', 'foo, bar, baz')
        opts.add('flagonly', None)
        '''
        if value:

            values = [x.strip() for x in value.split(',')]
            if key in self.data:
                item_data = self.data[key]
                for c in values:
                    c = c.strip()
                    if c not in item_data:
                        item_data.append(c)
                self.data[key] = item_data
            else:
                self.data[key] = values
        else:
            self.data[key] = None

        self.__save()

    def remove(self, key, value):
        '''
        Remove a flag value from the DockerOpts manager
        Assuming the data is currently {'foo': ['bar', 'baz']}

        d.remove('foo', 'bar')
        > {'foo': ['baz']}

        :params key:
        :params value:
        '''
        self.data[key].remove(value)
        self.__save()

    def to_s(self):
        '''
        Render the flags to a single string, prepared for the Docker
        Defaults file. Typically in /etc/default/docker

        d.to_s()
        > "--foo=bar --foo=baz"
        '''
        flags = []
        for key in self.data:
            if self.data[key] == None:
                flags.append("--{}".format(key))
            else:
                for item in self.data[key]:
                    flags.append("--{}={}".format(key, item))
        return ' '.join(flags)
