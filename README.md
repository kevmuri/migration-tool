# migration-tool
To use the migration tool, format your CSV with two columns:
    - A: The source directory of your files
    - B: The destination directory of your files

At this time the tool does not copy files for you, but rather generates a robocopy .bat script at the destination specified with the same name as the given CSV. This is done so for the purpose of spotchecking and editing.

The tool will create logs named for the destination directory of each robocopy line. This is done so for multiple sources that may share a destination. The number should correspond to the CSV line.