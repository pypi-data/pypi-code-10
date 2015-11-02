from pathlib import Path


def run():
	print('Running' if __name__ == '__main__' else 'Imported', Path(__file__).name)
	print(Path(__file__))
	with open("playlist_dl.py") as f:
		code = compile(f.read(), "playlist_dl.py", 'exec')
		exec(code)

if __name__ == '__main__':
	run()