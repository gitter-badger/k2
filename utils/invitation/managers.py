
def used(self):
        return self.get_query_set().exclude(registrant=None)