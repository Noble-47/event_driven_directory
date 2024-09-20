from abc import ABC, abstractmethod

class CloudStorageService:

    @abstractmethod
    def upload_file(self, file_content, file_name):
        pass

    @abstractmethod
    def get_file_url(self, file_name):
        pass

    @abstractmethod
    def delete_file(self, file_name):
        pass
