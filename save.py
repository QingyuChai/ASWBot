import rethinkdb as r

__version__ = "1.0.2"
__doc__ = """
Database stuff
"""

class SaveID:
    """Don't worry about this either"""

    def __init__(self):
        self.c = r.connect()
        self.c.use('Facebook')
        self.cog = "Users"
        self.table = r.table(self.cog)

    def insert_user(self,
                    user_id : str):
        self.table.insert({'user_id' : user_id}).run(self.c)

    def check_user(self,
                   user_id : str):
        if (self.table.filter(r.row['user_id'] == user_id)\
                .count().run(self.c)) == 0:
            return False
        else:
            return True

    def save_id(self,
                user_id):
        if not self.check_user(user_id):
            self.insert_user(user_id)
        return



class LoadCommand:
    """Don't worry about this"""

    def __init__(self):
        self.c = r.connect()
        self.c.use("Facebook")
        self.cog = "Modules"
        self.table = r.table(self.cog)

    def get_commands(self):
        coms = self.table.pluck('commands').run(c)
        commands = []
        for sublist_com in coms:
            for com in sublist_com:
                commands.append(com)

    def add_module(self,
                   module : str,
                   coms):
        module = module.lower()
        if not self.check_module(module):
            self.insert_module(module)
            self.add_commands(module,
                              coms)
        return

    def add_commands(self,
                     module,
                     coms):
        self.table(r.row['name'] == module)\
            .update({
                "commands" : coms
            }).run(self.c)


    def reload_module(self,
                      module : str,
                      coms):
        module = module.lower()
        self.remove_module(module,
                           coms)
        self.add_module(module,
                        coms)

    def remove_module(self,
                      module : str,
                      coms):
        if not self.check_module(module):
            return
        self.table(r.row['name'] == module)\
            .delete().run(self.c)

    def insert_module(self,
                      module : str):
        self.table.insert({'name' : module}).run(self.c)

    def check_module(self,
                     module : str):
        if (self.table.filter(r.row['name'] == module)\
                .count().run(self.c)) == 0:
            return False
        else:
            return True

    def save_id(self, user_id):
        if not self.check_user(user_id):
            self.insert_user(user_id)
