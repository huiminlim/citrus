class Session:
    def __init__(self, session_name, session_relative_workspace_path, session_relative_private_path):
        self.session_name = session_name
        self.session_relative_workspace_path = session_relative_workspace_path
        self.session_relative_private_path = session_relative_private_path

    # Method returns the relative path from exe is called
    # e.g. workspace/timestamp
    def get_relative_workspace_path(self):
        return self.session_relative_workspace_path

    # Method returns the relative path to private cache folder from exe is called
    # e.g. workspace/timestamp/cache
    def get_relative_private_path(self):
        return self.session_relative_private_path