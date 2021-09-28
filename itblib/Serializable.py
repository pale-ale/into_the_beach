

class Serializable:
    """The core concept of obtaining and applying a game state.
    The server calls extract_data() on it's own grid, which recursively
    extracts every relevant bit of information the clients would need.
    Once the extracted information is received by the clients, 
    they apply it to their own grid with insert_data()."""

    def __init__(self, serializable_fields:"list[str]") -> None:
        self.serializable_fields = serializable_fields[:]
    
    def insert_data(self, data:dict):
        for p in self.serializable_fields:
            if p in data.keys():
                if isinstance(data[p], (bool, int, float, str)):
                    setattr(self, p, data[p])

    def extract_data(self, custom_fields:"dict[str,any]"={}) -> dict:
        data = {}
        for p in self.serializable_fields:
            if p in custom_fields.keys():
                data[p] = custom_fields[p]
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