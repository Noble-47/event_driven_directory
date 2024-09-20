class EventHandler:

    def __init__(self):
        self.dispatcher = {}

    def add_handler(self, event:str) -> callable:
        handlers = self.dispatcher.get(event, None)
        if handlers is None:
            handlers = []
            self.dispatcher[event] = handlers
        def decorator(func:callable):
            handlers.append(func)
            return func
        return decorator

    def handle(self, event):
        event_name = event.name
        handlers = self.dispatcher.get(event_name)
        event_kwargs = event.asdict()
        if handlers:
           [handler(**kwargs) for handler in handlers] 
