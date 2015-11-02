import youtube_dl

ydl = youtube_dl.YoutubeDL()

url = input('Enter URL of playlist (any url will do) : \n')
# url = 'https://www.youtube.com/watch?v=InF16sp7J0M&index=2&list=PL2YL6eYKGUsDp9lQxgjmUrrbL6ng_g7aV' # test playlist
res = ydl.extract_info(url, download=False)

if 'entries' in res:
	res = res['entries']

s = ''

for i in res:
	print( len(i['requested_formats']) )
	s = s + str(i['playlist_index']) + '\n' + i['title'] + '\n' + i['webpage_url'] + '\n'
	print( i['playlist_index'])
	print( i['title'] )
	print( i['webpage_url'] )


fp = open('output.txt', 'w')
fp.write(s)
fp.close()