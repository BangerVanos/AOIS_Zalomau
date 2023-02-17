# Variant 7


class BinaryCalculator:
    """Calculator, which translates two given integer decimal numbers to binary form
    and performs operations on them. Each number contains 16 bits,
    (most significant for sign) which means numbers lie in [-2^15; 2^15-1] interval"""

    @classmethod
    def translate_to_binary(cls, number: int) -> str:
        binary_number: str = ""
        minus_bit = "1" if number < 0 else "0"
        number = abs(number)
        while number != 0:
            binary_number = str(number % 2) + binary_number
            number = number // 2
        binary_number = minus_bit + binary_number
        binary_number = binary_number[:1] + "0"*(16-len(binary_number)) + binary_number[1:]
        return binary_number

    @classmethod
    def translate_to_decimal(cls, binary_number: str) -> int:
        number = 0
        for i in range(1, 16):
            number += 2**(15-i)*int(binary_number[i])
        return number*(-1) if binary_number[0] == "1" else number

    @classmethod
    def is_binary_number_positive(cls, binary_number: str) -> bool:
        return True if binary_number[0] == "0" else False

    @classmethod
    def binary_numbers_sum(cls, first_number: int, second_number: int) -> str:
        binary_first_number: str = cls.translate_to_binary(first_number)
        binary_second_number: str = cls.translate_to_binary(second_number)
        if cls.is_binary_number_positive(binary_first_number) and cls.is_binary_number_positive(binary_second_number):
            return "0" + cls.__binary_modules_sum(binary_first_number, binary_second_number)
        binary_first_number = binary_first_number if binary_first_number[0] == "0" \
            else cls.twos_complement(binary_first_number)
        binary_second_number = binary_second_number if binary_second_number[0] == "0" \
            else cls.twos_complement(binary_second_number)
        sign: str = "0"
        if ((not cls.is_binary_number_positive(binary_first_number) and
                not cls.is_binary_number_positive(binary_second_number))
                or (not cls.is_binary_number_positive(binary_second_number)
                    and abs(first_number) < abs(second_number))):
            sign = "1"
        return cls.twos_complement(sign + cls.__binary_modules_sum(binary_first_number, binary_second_number))

    @classmethod
    def binary_numbers_diff(cls, first_number: int, second_number: int) -> str:
        return cls.binary_numbers_sum(first_number, -second_number)

    @classmethod
    def __binary_modules_sum(cls, binary_first: str, binary_second: str) -> str:
        additional_one: bool = False
        binary_result = ""
        for i in range(15, 0, -1):
            if binary_first[i] == "0" and binary_second[i] == "0":
                binary_result = "1" + binary_result if additional_one else "0" + binary_result
                additional_one = False
            elif ((binary_first[i] == "1" and binary_second[i] == "0")
                  or (binary_first[i] == "0" and binary_second[i] == "1")):
                if additional_one:
                    binary_result = "0" + binary_result
                else:
                    binary_result = "1" + binary_result
            else:
                binary_result = "1" + binary_result if additional_one else "0" + binary_result
                additional_one = True
        return binary_result

    @classmethod
    def ones_complement(cls, binary_number: str) -> str:
        if binary_number[0] == "0":
            return binary_number
        ones_complement = "1" + "".join(["1" if i == "0" else "0" for i in binary_number[1:]])
        return ones_complement

    @classmethod
    def twos_complement(cls, binary_number: str) -> str:
        if binary_number[0] == "0":
            return binary_number
        binary_number = cls.ones_complement(binary_number)
        return "1" + cls.__binary_modules_sum(binary_number, cls.translate_to_binary(1))

    @classmethod
    def binary_numbers_product(cls, first_number: int, second_number: int) -> str:
        binary_first_number = cls.translate_to_binary(first_number)
        binary_second_number = cls.translate_to_binary(second_number)
        sign: str = "0" if binary_first_number[0] == binary_second_number[0] else "1"
        return sign + cls.__binary_modules_product(binary_first_number, binary_second_number)

    @classmethod
    def __binary_modules_product(cls, binary_first: str, binary_second: str) -> str:
        binary_result: str = "0" * 15
        for i in range(15, 0, -1):
            if binary_first[i] == "1":
                shifted_sum: str = binary_second[(15-i):] + "0" * (15 - i)
                binary_result = cls.__binary_modules_sum("0" + binary_result, shifted_sum)
        return binary_result

