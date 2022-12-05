import os
import csv

def check_if_file_exists(file_path: str) -> bool:
	if not os.path.exists(file_path):
		return False
	return True

def read_file_content(file_path: str) -> str:
	if not check_if_file_exists(file_path):
		raise Exception(f"File: \"{file_path}\" does not exist!\nCheck the file and try again.")
	with open(file_path, "r") as f:
		content = f.read()
		f.close()
		return content

def write_file(file_path: str, content: str, mode: str) -> bool:
	try:
		target_file = open(file=file_path, mode=mode)
		target_file.write(content)
		target_file.close()
		return True
	except IOError:
		print ("Could not open file: \"{file_path}\"!")
		return False

def read_csv_file(file_path: str, line: int) -> list:
	if not check_if_file_exists(file_path):
		raise Exception(f"File: \"{file_path}\" does not exist!\nCheck the file and try again.")
	with open(file_path) as csv_obj:
		csv_reader = csv.reader(csv_obj, delimiter=',')
		header = next(csv_reader, None)
		row = []
		if header is not None:
			csv_reader = list(csv_reader)
			row = csv_reader[line]
			return row
		return row

def create_dir_if_not_exist(path: str):
	if check_if_file_exists(path):
		return
	os.makedirs(path)