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

    def add(self, key, value, strict=False):
        '''
        Adds data to the map of values for the DockerOpts file.
        Supports single values, or "multiopt variables". If you
        have a flag only option, like --tlsverify, set the value
        to None. To preserve the exact value, pass strict

        eg:
        opts.add('label', 'foo')
        opts.add('label', 'foo, bar, baz')
        opts.add('flagonly', None)
        opts.add('cluster-store', 'consul://a:4001,b:4001,c:4001/swarm', strict=True)
        '''
        if strict:
            self.data['{}-strict'.format(key)] = value

        if value:
            values = [x.strip() for x in value.split(',')]
            # handle updates
            if key in self.data and self.data[key] is not None:
                item_data = self.data[key]
                for c in values:
                    c = c.strip()
                    if c not in item_data:
                        item_data.append(c)
                self.data[key] = item_data
            else:
                # handle new
                self.data[key] = values
        else:
            # handle flagonly
            self.data[key] = None
        self.__save()

    def exists(self, key):
        '''
        Predicate method to determine if the backing dictionary has a flag for
        the requested key.


        eg:
        opts.exists('foo')
        > True
        '''
        found = False
        if key in self.data:
            found = True
        if '{}-strict'.format(key) in self.data.keys():
            found = True

        return found

    def pop(self, key):
        '''
        Completely remove a flag from the DockerOpts manager including any
        associated values. Assuming the data is currently:
        {'foo': ['bar', 'baz']}

        d.pop('foo')
        > {}

        :params key:
        '''

        self.data.pop(key)
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
                # handle flagonly
                flags.append("--{}".format(key))
            elif '-strict' in key:
                # handle strict values
                proper_key = key.rstrip('-strict')
                flags.append("--{}={}".format(proper_key, self.data[key]))
            else:
                # handle multiopt and typical flags
                for item in self.data[key]:
                    flags.append("--{}={}".format(key, item))
        return ' '.join(flags)
