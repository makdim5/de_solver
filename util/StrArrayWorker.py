DEVIDER = "^"


class StrArrayWorker:
    @staticmethod
    def convert_list_str_to_string(list_numbers):
        result = ""
        for item in list_numbers:
            result += str(item) + DEVIDER

        return result[:len(result) - 2]

    @staticmethod
    def convert_string_to_list_str(string):
        result = []

        index = 0
        while index < len(string):
            simple_str = ""
            while index < len(string) and string[index] != DEVIDER:
                simple_str += string[index]
                index += 1
            index += 1
            result.append(simple_str)

        return result

# simple = NumberArrayWorker.convert_list_number_to_string([5.6, 7.888565626, 898.56565])
#
# print(simple)
#
# list = NumberArrayWorker.convert_string_to_list_number(simple)
#
# print(list, list[2]+1)