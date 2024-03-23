import time

from io.handlers.exceptions import LoadException
from io.handlers.typing import T, U
from utils.logging import get_logger


logger = get_logger(__name__)


class MediaHandler:
    """
    A class that handles media files, including loading, archiving, and saving.

    Args:
        data_location (str): The location of the data.
        writer (V): The writer object used for writing data.
        loader (U): The loader object used for loading data.

    Attributes:
        data_location (str): The location of the data.
        archive_location (str): The location where archived media files are stored.
        _writer (T): The writer object used for writing data.
        _loader (U): The loader object used for loading data.
    """

    def __init__(self, data_location: str, writer: T, loader: U) -> None:
        self.data_location = data_location
        self.archive_location = f"{self.data_location}/archive"
        self._writer = writer
        self._loader = loader

    def load(self, name: str, **kwargs) -> list:
        """
        Load media files from a specific path.

        Args:
            name (str): The name of the media file.
            **kwargs: Additional keyword arguments to be passed to the loader.

        Returns:
            list: The loaded media files.

        Raises:
            LoaderException: If the loader cannot handle the specified path or if no data is loaded.
        """
        path = f"{self.data_location}/{name}"
        # ensure loader can handle path
        if not self._loader.can_handle(path):
            raise LoadException(path=path)

        # load the data
        logger.info(f"Loading media files from path: {path}")
        loaded_data = self._loader.load(path=path, **kwargs)

        # raise if no data loaded
        if len(loaded_data) == 0:
            raise LoadException(path=path)

        logger.info(f"Loaded {len(loaded_data)} media files from path: {path}")
        return loaded_data

    def handle_archive(self, name: str) -> str | None:
        """
        Handle archiving of media files.

        Args:
            name (str): The name of the media file.

        Returns:
            str | None: The path of the archived media file, or None if no archiving is performed.

        Raises:
            None
        """
        src = f"{self.data_location}/{name}"

        # archive if exists, else no-op
        if self._writer.exists(src):
            # timestamp filename in archive location
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            dest = f"{self.archive_location}/{timestamp}-{name}"

            # copy to archive
            self._writer.copy(src, dest)

            # delete original
            self._writer.delete(src)
            logger.info(f"Archived previous media files to {dest}")

            return dest

        logger.debug(f"No file to archive at path: {src}")

    def save_dict(self, data: dict, name: str, **kwargs):
        """
        Save a dictionary of media files to a specific path.

        Args:
            data (dict): The dictionary of media files to be saved.
            name (str): The name of the media file.
            **kwargs: Additional keyword arguments to be passed to the writer.

        Returns:
            None

        Raises:
            None
        """
        path = f"{self.data_location}/{name}"
        logger.info(f"Saving media files to path: {path}")

        self._writer.write(path, data, **kwargs)