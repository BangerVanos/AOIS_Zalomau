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
        binary_number = binary_number[:1] + "0" * (16 - len(binary_number)) + binary_number[1:]
        return binary_number

    @classmethod
    def translate_to_decimal(cls, binary_number: str) -> int:
        number = 0
        for i in range(1, len(binary_number)):
            number += 2 ** (len(binary_number) - 1 - i) * int(binary_number[i])
        return number * (-1) if binary_number[0] == "1" else number

    @classmethod
    def is_binary_number_positive(cls, binary_number: str) -> bool:
        return True if binary_number[0] == "0" else False

    @classmethod
    def binary_abs(cls, binary_number: str) -> str:
        return "0" + binary_number[1:]

    @classmethod
    def is_binary_module_greater_than(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        for i in range(1, len(compared_binary_one)):
            if compared_binary_one[i] == "1" and compared_binary_two[i] == "0":
                return True
            elif compared_binary_one[i] == "0" and compared_binary_two[i] == "1":
                return False
        return False

    @classmethod
    def is_binary_greater_than(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        if compared_binary_one[0] == "0" and compared_binary_two[0] == "1":
            return True
        elif compared_binary_one[0] == "1" and compared_binary_two[0] == "0":
            return False
        elif compared_binary_one[0] == "0" and compared_binary_two[0] == "0":
            return cls.is_binary_module_greater_than(compared_binary_one, compared_binary_two)
        else:
            return not cls.is_binary_module_greater_than(compared_binary_one, compared_binary_two)

    @classmethod
    def binary_number_round(cls, binary_number: str, round_factor: int) -> str:
        if round_factor == 15:
            return binary_number
        if binary_number[round_factor + 1:] == "0":
            return binary_number[:round_factor] + "0" * (len(binary_number) - round_factor)
        else:
            return cls.binary_numbers_sum(binary_number[:round_factor]
                                          + "0" * (len(binary_number) - round_factor),
                                          "0" * (round_factor - 1) + "1" + "0" * (len(binary_number) - round_factor))

    @classmethod
    def binary_numbers_sum(cls, binary_first_number: str, binary_second_number: str) -> str:
        if cls.is_binary_number_positive(binary_first_number) and cls.is_binary_number_positive(binary_second_number):
            return "0" + cls.__binary_summation(binary_first_number, binary_second_number)
        binary_first_number_converted: str = binary_first_number if binary_first_number[0] == "0" \
            else cls.twos_complement(binary_first_number)
        binary_second_number_converted: str = binary_second_number if binary_second_number[0] == "0" \
            else cls.twos_complement(binary_second_number)
        return cls.twos_complement(cls.__binary_summation(binary_first_number_converted,
                                                          binary_second_number_converted))

    @classmethod
    def binary_numbers_sum_from_int(cls, first_number: int, second_number: int) -> str:
        binary_first_number: str = cls.translate_to_binary(first_number)
        binary_second_number: str = cls.translate_to_binary(second_number)
        return cls.binary_numbers_sum(binary_first_number, binary_second_number)

    @classmethod
    def binary_numbers_substr(cls, first_number: int, second_number: int) -> str:
        return cls.binary_numbers_sum_from_int(first_number, -second_number)

    @classmethod
    def __binary_summation(cls, binary_first: str, binary_second: str) -> str:
        additional_one: bool = False
        binary_result = ""
        for i in range(len(binary_first) - 1, -1, -1):
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
        return cls.__binary_summation(binary_number, cls.translate_to_binary(1))

    @classmethod
    def binary_numbers_product(cls, first_number: int, second_number: int) -> str:
        binary_first_number: str = cls.translate_to_binary(first_number)
        binary_second_number: str = cls.translate_to_binary(second_number)
        sign: str = "0" if binary_first_number[0] == binary_second_number[0] else "1"
        return sign + cls.__binary_modules_product(binary_first_number, binary_second_number)

    @classmethod
    def __binary_modules_product(cls, binary_first: str, binary_second: str) -> str:
        binary_result: str = "0" * len(binary_first)
        for i in range(len(binary_first) - 1, 0, -1):
            if binary_first[i] == "1":
                shifted_sum: str = binary_second[(len(binary_first) - 1 - i):] + "0" * (len(binary_first) - 1 - i)
                binary_result = cls.__binary_summation(binary_result, shifted_sum)
        return binary_result

    @classmethod
    def binary_numbers_division(cls, dividend: int, divider: int) -> str:
        binary_dividend: str = cls.translate_to_binary(dividend)
        binary_divider: str = cls.translate_to_binary(divider)
        sign: str = "0" if binary_dividend[0] == binary_divider[0] else "1"
        remainder: str = cls.binary_numbers_substr(abs(dividend), abs(divider))
        if remainder[0] == "0":
            raise ValueError
        result: str = "0" * 16
        for i in range(9):
            remainder = remainder[0] + remainder[2:] + "0"
            binary_divider = "0" + binary_divider[1:] if remainder[0] == "1" else "1" + binary_divider[1:]
            remainder = cls.binary_numbers_sum(remainder, binary_divider)
            list_result: list = list(result)
            list_result[i] = "0" if remainder[0] == "1" else "1"
            result = ''.join(list_result)
        result = cls.binary_number_round(result, 6)
        return sign + "0." + result

    @classmethod
    def fixed_point_to_decimal(cls, fixed_point_number: str) -> float:
        fraction: str = fixed_point_number[3:]
        result: float = 0
        for i in range(len(fraction)):
            result += int(fraction[i]) * (2 ** (-(i + 1)))
        return -result if fixed_point_number[0] == "1" else result

    @classmethod
    def translate_to_floating_point(cls, number: int, exponent: str) -> tuple[str]:
        binary_number = "0" * 9 + cls.translate_to_binary(abs(number))
        sign = "1" if number < 0 else "0"
        digit_moves_amount = cls.translate_to_decimal(exponent)

    @classmethod
    def floating_point_summary(cls, first_number: int, second_number: int) -> str:
        exponent_1 = "00000100"
        exponent_2 = "00000101"
        binary_first = "0" * 9 + cls.translate_to_binary(first_number)
        binary_second = "0" * 9 + cls.translate_to_binary(second_number)




print(BinaryCalculator.fixed_point_to_decimal(BinaryCalculator.binary_numbers_division(14, 23)))
print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_sum_from_int(23, -11)))
print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(14, 23)))
print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(-14, 23)))
print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(14, -23)))
print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(-14, -23)))
