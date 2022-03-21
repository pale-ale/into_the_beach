class InputAcceptor:
    def __init__(self):
        self._child_input_listeners:"list[InputAcceptor]" = []
    
    def register_input_listeners(self, *listeners:"InputAcceptor"):
        for l in listeners:
            self._child_input_listeners.append(l)

    def remove_input_listeners(self, *listeners:"InputAcceptor"):
        for l in listeners:
            self._child_input_listeners.remove(l)

    def handle_key_event(self, event:any) -> bool:
        """
        Passes on key events to children. If they did not handle the event, attempt to handle it.
        @event: pygame's keyevent
        @return: whether the event was handled or not. If it was handled, it will be discarded immediately.
        """
        for listener in reversed(self._child_input_listeners):
            if listener.handle_key_event(event): #if the listener handles the event, we discard it right away
                return True
        return False
