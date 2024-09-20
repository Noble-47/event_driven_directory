from dataclasses import dataclass, asdict


@dataclass
class Event:

    def __post_init__(self, event_id: int | None = None):
        self.event_id = event_id
        self.name = self.__class__.__name__

    def asdict(self):
        return asdict(self)


@dataclass
class AddedPrefixToFolderName(Event):
    folder_id: int
    prefix: str


@dataclass
class MovedFolder(Event):
    folder_id: int
    to: int


@dataclass
class CreatedFolder(Event):
    parent_id: int
    new_folder_name: str


@dataclass
class AddedFolder(Event):
    folder_id: int
    added: int


@dataclass
class DeletedFolder(Event):
    folder_id: int
    folder_name: str


@dataclass
class AddedFile(Event):
    file_name: str
    file_url: str
    folder_id: int


@dataclass
class FoundFile(Event):
    file_name: str
    file_url: str
    folder_id: int


@dataclass
class RemovedFile(Event):
    file_name: str
    file_url: str
    folder_id: int
