

class Serializable:
    """The core concept of obtaining and applying a game state.
    The server calls extract_data() on it's own grid, which recursively
    extracts every relevant bit of information the clients would need.
    Once the extracted information is received by the clients, 
    they apply to their own grid with insert_data()."""
    
    def insert_data(self, data):
        pass

    def extract_data(self, properties:"list[str]", custom:"dict[str,object]"={}) -> dict:
        data = {}
        for p in properties:
            if p in custom.keys():
                data[p] = custom[p]
            elif p in self.__dict__.keys():
                o = self.__dict__[p]
                if isinstance(o, Serializable):
                    data[p] = o.extract_data()
                elif isinstance(o, (bool, int, float, str)):
                    data[p] = o
                else:
                    print(f"Serializable: Property '{p}' has to be extracted by yourself. Just override this method.")
            else:
                print(f"Serializable: Property '{p}' not found.")
        return data