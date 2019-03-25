import requests
import tarfile
import os
import re


# Extract content of tex files from a compressed tar.gz file
def extract_tex(input_file):
    tar = tarfile.open(input_file, "r:gz")

    # Find the tex file
    tex = None

    for member in tar.getmembers():
        if member.name.lower().endswith('tex'):
            with tar.extractfile(member) as m:
                tex = m.read()

    return tex.decode('utf-8')

def tex_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".tex":
            yield tarinfo

def main():
	arxiv_id = "1903.08964"
	arxiv_prefix = "https://arxiv.org/e-print/"

	# Search arXiv
	print("Search arXiv - to do")

	# Download file
	print("Downloading paper id: {}".format(arxiv_id))
	url = arxiv_prefix + arxiv_id
	r = requests.get(url)

	# Saving received content as a tar.gz file in the papers folder
	file_name = "papers/{}.tar.gz".format(arxiv_id)

	with open(file_name,'wb') as f: 
	    f.write(r.content)
	
	# Untar
	tex = extract_tex(file_name)

	# Search equations
	equations = re.findall(r"\\begin\{equation\}(?s)(.*?)\\end\{equation\}", tex)
	inline_equations = re.findall("\\$.*?(?<!\\\\)\\$", str(tex))

	# Print equations
	for equation in equations:
		print(equation)


if __name__ == "__main__":
	main()
