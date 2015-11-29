""" 중복된 리스트를 화면에 출력할 수 있는 모듈입니다.
    다양한 데이터 구조에 응용이 가능합니다. """


def print_lol(the_list, indent=False,level=0):
        """이 함수는 the_list라는 이름의 인자를 갖고 있으며, 파이썬 리스트를 받습니다.
이 리스트는 리스트도 항목으로 포함할 수 있습니다. 매 라인마다 리스트에 있는 항목이 하나씩
재귀적으로 화면에 출력됩니다. 두 번째 인자 indent는 중첩된 리스트의 항목들에 대해서
indentation을 사용할 것인지 아닌지를 결정하며, default value는 False 입니다.세 번째 인자
level은 중첩된 리스트에서 탭을 추가하기 위해 사용되며, default value는 0 입니다."""
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t", end='')
                        print(each_item)
