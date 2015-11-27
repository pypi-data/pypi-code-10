""" 중복된 리스트를 화면에 출력할 수 있는 모듈입니다.
    다양한 데이터 구조에 응용이 가능합니다. """

def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
