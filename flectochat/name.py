


class Name:

    def __init__(self, name, signature):
        self.name = name
        self.signature = signature


class Address:

    def __init__(self, address, timestamp, signature):
        self.address = address
        self.timestamp = timestamp
        self.signature = signature


class Storage:

    def __init__(self):
        self.names = []
        self.addresses = []
        self.known = {}

    def add_name(self, name):
        self.names.append(name)
        self.update_known(name, None)

    def add_address(self, address):
        self.names.append(address)
        self.update_known(None, address)

    def update_known(self, new_name, new_address):

        self.known = {}
        for name in self.names:
            for address in self.addresses:

                if self.matching(name, address):
                    self.add_known(name, address)

    def matching(self, name, address):
        # TODO implement, this for testing
        return name.signature == address.signature

    def add_known(self, name, address):
        # if its missing or its newer
        if name not in self.known or self.known[name].timestamp < address.timestamp:
            self.known[name] = address
