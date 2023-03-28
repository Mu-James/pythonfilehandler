from pathlib import Path
import filecmp
import shutil

class FileHandler():
    def __init__(self, directory_path_tuple_input: list[Path]):
        self._directory_path_tuple = directory_path_tuple_input
        
        self._path_list1 = self._get_files_from_directory(self._directory_path_tuple[0])
        self._path_list2 = self._get_files_from_directory(self._directory_path_tuple[1])
        
        self._shared_files_list = self._get_shared_files(self._path_list1, self._path_list2)
        self._total_shared_files = len(self._shared_files_list)
        
        self._unique_files_list = self._get_unique_files()
        self._total_unique_files = len(self._unique_files_list)

    def _get_files_from_directory(self, directory_path: Path) -> list[Path]:
        file_path_list = []
        for file_path in directory_path.iterdir():
            if file_path.is_file() == True:
                file_path_list.append(file_path)

        return file_path_list

    def _get_shared_files(self, path_list1: list[Path], path_list2: list[Path]) -> list[Path]:
        shared_file_list = []
        
        for file1 in path_list1:
            for file2 in path_list2:
                if filecmp.cmp(file1, file2, shallow = False) == True:
                    shared_file_list.append(file1.name)

        filecmp.clear_cache()
        return shared_file_list

    def _get_unique_files(self) -> list[Path]:
        unique_file_list = []

        for file1 in self._path_list1:
            if file1.name not in self._shared_files_list and file1.name not in unique_file_list:
                unique_file_list.append(file1)
    
        for file2 in self._path_list2:
            if file2.name not in self._shared_files_list and file2.name not in unique_file_list:
                unique_file_list.append(file2)

        return unique_file_list

    def _create_new_directory(self, base_directory_path: Path, new_directory_name: str) -> None:
        Path(str(base_directory_path) + '\\' + new_directory_name).mkdir(parents=True, exist_ok=True)

    def copy_shared_files_to_new_dir(self, base_directory_path: Path, new_directory_name: str) -> None:
        new_directory_path = Path(str(base_directory_path) + '\\' + new_directory_name)
        self._create_new_directory(base_directory_path, new_directory_name)
        for file in self._shared_files_list:
            shutil.copy(file, new_directory_path)
        
    def copy_unique_files_to_new_dir(self, base_directory_path: Path, new_directory_name: str) -> None:
        new_directory_path = Path(str(base_directory_path) + '\\' + new_directory_name)
        self._create_new_directory(base_directory_path, new_directory_name)
        for file in self._unique_files_list:
            shutil.copy(file, new_directory_path)

    def generate_shared_files_report(self, destination_directory_path: Path) -> None:
        try:
            with open(str(destination_directory_path) + '\\Shared Files Report.txt', 'w', encoding='utf-8') as report:
                report.write('Total Number of Files: ' + str(self._total_shared_files) + '\n')
                for file in self._shared_files_list:
                    report.write(str(file) + '\n')
        except:
            pass

    def generate_unique_files_report(self, destination_directory_path: Path) -> None:
        try:
            with open(str(destination_directory_path) + '\\Unique Files Report.txt', 'w', encoding='utf-8') as report:
                report.write('Total Number of Files: ' + str(self._total_unique_files) + '\n')
                for file in self._unique_files_list:
                    report.write(str(file) + '\n')                
        except:
            pass        
        
def get_file_directory_input() -> tuple:
    first_directory_path = input('Enter first file directory: ')
    second_directory_path = input('Enter second file directory: ')

    return _create_directory_path_tuple(first_directory_path, second_directory_path)

def _create_directory_path_tuple(path_str1: str, path_str2: str) -> tuple[Path]:
    try:
        path_tuple = (Path(path_str1), Path(path_str2))
        return path_tuple
    except:
        return None

def check_file_directory_input(path_tuple: tuple[Path]) -> bool:
    is_directory_tuple = False
    
    try:
        for path in path_tuple:
            check_convert = path
            if check_convert.is_dir() and check_convert.exists() == True:
                is_directory_tuple = True
            else:
                is_directory_tuple = False
    except:
        is_director_tuple = False

    return is_directory_tuple

#def get_unique_files(path_list1: list[Path], path_list2: list[Path]) -> list[Path]:  
#    unique_file_list = list(set(path_list1).symmetric_difference(set(path_list2)))
#    return unique_file_list
    
def file_handler() -> None:

    directory_path_tuple = get_file_directory_input()
    if check_file_directory_input(directory_path_tuple) == True:
        file_handler_obj = FileHandler(directory_path_tuple)
        file_handler_obj.generate_unique_files_report(Path(# Path File Here))
            
if __name__ == '__main__':
    file_handler()
