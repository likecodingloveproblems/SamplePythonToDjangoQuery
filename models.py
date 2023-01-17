class Manager:
    commands = list()

    def all(self):
        self.commands.append("all")
        return self

    def filter(self, *args, **kwargs):
        self.commands.append({"filter": {"args": args, "kwargs": kwargs}})
        return self

    def alias(self, *args, **kwargs):
        self.commands.append({"alias": {"args": args, "kwargs": kwargs}})
        return self


class Driver:
    objects = Manager()
