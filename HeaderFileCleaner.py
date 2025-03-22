import os
import glob

class HeaderFileCleaner:
    """
    A class to remove all .h files from specified folders.
    """
    
    def __init__(self, folders):
        """
        Initializes the HeaderFileCleaner with a list of folder paths.
        
        :param folders: List of folder paths where .h files should be removed.
        """
        self.folders = folders

    def remove_header_files(self):
        """
        Removes all .h files from the specified folders.
        """
        for folder in self.folders:
            if not os.path.exists(folder):
                print(f"Warning: Folder '{folder}' does not exist.")
                continue

            header_files = glob.glob(os.path.join(folder, "*.h"))  # Find all .h files
            for file in header_files:
                try:
                    os.remove(file)
                    print(f"Deleted: {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
            
            cpp_files = glob.glob(os.path.join(folder, "*.cpp"))  # Find all .cpp files
            for file in cpp_files:
                try:
                    os.remove(file)
                    print(f"Deleted: {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")


