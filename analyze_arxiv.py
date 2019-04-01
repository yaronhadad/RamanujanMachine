import requests
import tarfile
import os
import re


arxiv_prefix = "https://arxiv.org/e-print/"

# Extract content of tex files from a compressed tar.gz file
def extract_tex(input_file):
	print("Extracting TAR: {}".format(input_file))
	tex = None
	tar = tarfile.open(input_file, "r:gz")

	# Find the tex file
	for member in tar.getmembers():
		if member.name.lower().endswith('tex'):
			with tar.extractfile(member) as m:
				tex = m.read()

	return tex.decode('utf-8')

def tex_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".tex":
            yield tarinfo

def download_arxiv_source(arxiv_id):
	print("Downloading paper id: {}".format(arxiv_id))

	url = arxiv_prefix + arxiv_id
	r = requests.get(url)

	# Saving received content as a tar.gz file in the papers folder
	file_name = "papers/{}.tar.gz".format(arxiv_id)

	with open(file_name,'wb') as f: 
	    f.write(r.content)

	return (file_name)

def get_equations(arxiv_id, show_equations=True, show_inline_equations=False):
	# Download file
	file_name = download_arxiv_source(arxiv_id)
		
	# Untar
	tex = extract_tex(file_name)

	# Search equations
	equations = re.findall(r"\\begin\{equation\}(?s)(.*?)\\end\{equation\}", tex)
	inline_equations = re.findall("\\$.*?(?<!\\\\)\\$", str(tex))

	print("Detected {} equations".format(len(equations)))

	# Print equations
	if show_equations:
		for equation in equations:
			print(equation)

	# Print inline equations
	if show_inline_equations:
		for equation in inline_equations:
			print(equation)


def main():
	arxiv_ids = ["1503.01150", "1809.06633"]
	# arxiv_id = "1903.08964"

	# Search arXiv
	print("Search arXiv - to do")

	for arxiv_id in arxiv_ids:
		get_equations(arxiv_id)


if __name__ == "__main__":
	main()
