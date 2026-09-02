from pathlib import Path


from app.utils.path_validation import validate_export_path


class ExportService:
    """
    Coordinates safe report-export operations.
    """

    def __init__(
        self,
        reporter
    ):
        """
        Initialises the analysis service.

        Args:
            reporter: Log reporter providing structured analysis results.

        Returns:
            None
        """

        self.reporter = reporter

    def validate_export_file(
            self,
            filename: str | Path
    ) -> Path:
        """
        Validates and resolves a report export filename.

        Args:
            filename (str | Path): Requested report export filename.

        Returns:
            Path: Validated path inside the approved reports directory.
        """

        return validate_export_path(
            filename
        )
