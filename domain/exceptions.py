class FileAlreadyExists(Exception):

    def __init__(self, folder_name, file_name):
        self.folder_name = folder_name
        self.file_name = file_name
        super().__init__(f"{self.file_name} exits in {self.folder_name}")


class FolderAlreadyExists(Exception):

    def __init__(self, folder_name):
        self.folder_name = folder_name
        super().__init__(f"{self.folder_name} already exists.")
