from itblib.Log import log

class Serializable:
    """The core concept of obtaining and applying a game state.
    The server calls extract_data() on it's own grid, which recursively
    extracts every relevant bit of information the clients would need.
    Once the extracted information is received by the clients, 
    they apply it to their own grid with insert_data()."""

    def __init__(self, serializable_fields:"list[str]") -> None:
        self.serializable_fields = serializable_fields[:]
    
    def insert_data(self, data:dict, exclude:"list[str]"):
        """Insert data from the dict into an object, configuring it."""
        for serializable_property in self.serializable_fields:
            if serializable_property in data.keys() and not serializable_property in exclude:
                setattr(self, serializable_property, data[serializable_property])

    def extract_data(self, custom_fields:"dict[str,any]"=None) -> dict:
        """Extract data of given fields into a smiple dict for easy data transfer."""
        data = {}
        for serializable_property in self.serializable_fields:
            if custom_fields and serializable_property in custom_fields.keys():
                data[serializable_property] = custom_fields[serializable_property]
            elif serializable_property in self.__dict__:
                serializable_object = self.__dict__[serializable_property]
                if isinstance(serializable_object, Serializable):
                    data[serializable_property] = serializable_object.extract_data()
                elif isinstance(serializable_object, (bool, int, float, str)):
                    data[serializable_property] = serializable_object
                else:
                    log(f"Serializable: Property '{serializable_property}' has to be extracted by yourself.\
                        Just override this method.", 2)
            else:
                log(f"Serializable: Property '{serializable_property}' not found.", 2)
        return data
