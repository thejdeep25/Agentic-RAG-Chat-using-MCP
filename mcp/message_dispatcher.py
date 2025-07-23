# This module is the "post office" for agent messages.
# It makes sure every message gets to the right agent, just like a good mail sorter!

class MCPMessage:
    def __init__(self, sender, receiver, type, trace_id, payload):
        """
        A message object for agents to communicate.
        Includes sender, receiver, message type, a trace ID for tracking, and the actual data (payload).
        """
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.trace_id = trace_id
        self.payload = payload

class MCPDispatcher:
    def __init__(self):
        """
        Sets up the dispatcher with a place to keep track of all agent handlers.
        """
        self.handlers = {}

    def register_agent(self, agent_name, handler_func):
        """
        Register an agent so it can receive messages.
        """
        self.handlers[agent_name] = handler_func

    def send_message(self, message: MCPMessage):
        """
        Deliver a message to the right agent. If the agent isn't found, print a warning.
        """
        handler = self.handlers.get(message.receiver)
        if handler:
            handler(message)
        else:
            print(f"No handler found for {message.receiver}")
