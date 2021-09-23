DEVIDER = "^"


class NumberArrayWorker:
    @staticmethod
    def convert_list_number_to_string(list_numbers):
        result = ""
        for item in list_numbers:
            result += str(item) + DEVIDER

        return result[:len(result) - 2]

    @staticmethod
    def convert_string_to_list_number(string):
        result = []
        if "j" in string:
            string += ")"
        index = 0
        while index < len(string):
            simple_str = ""
            while index < len(string) and string[index] != DEVIDER:
                simple_str += string[index]
                index += 1
            index += 1
            if simple_str != "":
                if "j" in simple_str:
                    result.append(complex(simple_str))
                else:
                    result.append(float(simple_str))

        return result
