from pathlib import Path


from app.utils.path_validation import validate_input_log_path


class FileService:
    """
    Coordinates safe input-log file validation.
    """

    def validate_input_file(
        self,
        filename: str | Path
    ) -> Path:
        """
        Validates and resolves an input log file.

        Args:
            filename (str | Path): Input log filename or path to validate.

        Returns:
            Path: Validated path inside the approved input log directory.
        """

        return validate_input_log_path(
            filename
        )
