# Variant 7


class BinaryCalculator:
    """Calculator, which translates two given integer decimal numbers to binary form
    and performs operations on them. Each number contains 16 bits,
    (most significant for sign) which means numbers lie in [-2^15; 2^15-1] interval"""

    @classmethod
    def translate_to_binary(cls, number: int, bit_amount: int = 16) -> str:
        binary_number: str = ""
        minus_bit = "1" if number < 0 else "0"
        number = abs(number)
        while number != 0:
            binary_number = str(number % 2) + binary_number
            number = number // 2
        binary_number = minus_bit + binary_number
        binary_number = binary_number[:1] + "0" * (bit_amount - len(binary_number)) + binary_number[1:]
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
        for i in range(len(compared_binary_one)):
            if compared_binary_one[i] == "1" and compared_binary_two[i] == "0":
                return True
            elif compared_binary_one[i] == "0" and compared_binary_two[i] == "1":
                return False
        return False

    @classmethod
    def are_binary_numbers_equal(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        for i in range(len(compared_binary_one)):
            if compared_binary_one[i] != compared_binary_two[i]:
                return False
        return True

    @classmethod
    def is_binary_greater_than(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        if compared_binary_one[0] == "0" and compared_binary_two[0] == "1":
            return True
        elif compared_binary_one[0] == "1" and compared_binary_two[0] == "0":
            return False
        elif compared_binary_one[0] == "0" and compared_binary_two[0] == "0":
            return cls.is_binary_module_greater_than(compared_binary_one[1:], compared_binary_two[1:])
        else:
            return not cls.is_binary_module_greater_than(compared_binary_one[1:], compared_binary_two[1:])

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
            return cls.__binary_summation(binary_first_number, binary_second_number)
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
        if len(binary_first) < len(binary_second):
            binary_first = "0" * (len(binary_second)-len(binary_first)) + binary_first
        else:
            binary_second = "0" * (len(binary_first)-len(binary_second)) + binary_second
        additional_one: bool = False
        binary_result = ""
        for i in range(len(binary_first) - 1, -1, -1):
            if binary_first[i] == ".":
                binary_result = "." + binary_result
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
        reversed_digits: dict = {"0": "1", "1": "0", ".": "."}
        if binary_number[0] == "0":
            return binary_number
        ones_complement = "1" + "".join([reversed_digits[i] for i in binary_number[1:]])
        return ones_complement

    @classmethod
    def twos_complement(cls, binary_number: str) -> str:
        if binary_number[0] == "0":
            return binary_number
        binary_number = cls.ones_complement(binary_number)
        return cls.__binary_summation(binary_number, cls.translate_to_binary(1, bit_amount=len(binary_number)))

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
        for i in range(12):
            remainder = remainder[0] + remainder[2:] + "0"
            binary_divider = "0" + binary_divider[1:] if remainder[0] == "1" else "1" + binary_divider[1:]
            remainder = cls.binary_numbers_sum(remainder, binary_divider)
            list_result: list = list(result)
            list_result[i] = "0" if remainder[0] == "1" else "1"
            result = ''.join(list_result)
        result = cls.binary_number_round(result, 9)
        return sign + "0." + result

    @classmethod
    def fixed_point_to_decimal(cls, fixed_point_number: str) -> float:
        fraction: str = fixed_point_number[3:]
        result: float = 0
        for i in range(len(fraction)):
            result += int(fraction[i]) * (2 ** (-(i + 1)))
        return -result if fixed_point_number[0] == "1" else result

    @classmethod
    def translate_to_floating_point(cls, number: int) -> list[str, str, str]:
        sign = "1" if number < 0 else "0"
        binary_number = cls.translate_to_binary(number)[1:]
        digit_order: int = binary_number.find("1") + 1
        exponent: str = cls.__binary_summation(cls.translate_to_binary(127, 8),
                                               cls.translate_to_binary(digit_order, bit_amount=8))
        mantissa = binary_number[digit_order:] + "0" * (23 - digit_order)
        return [sign, exponent, mantissa]

    @classmethod
    def __move_the_mantissa(cls, mantissa: str, mantissa_moves: int) -> str:
        return "0" * mantissa_moves + mantissa[mantissa_moves:]

    @classmethod
    def floating_point_summary(cls, first_number: int, second_number: int) -> list[str, str, str]:
        floating_first: list[str, str, str] = cls.translate_to_floating_point(first_number)
        floating_second: list[str, str, str] = cls.translate_to_floating_point(second_number)
        if cls.is_binary_module_greater_than(floating_first[1], floating_second[1]):
            point_moves: int = 0
            while not cls.are_binary_numbers_equal(floating_first[1], floating_second[1]):
                floating_second[1] = cls.__binary_summation(floating_second[1], "00000001")
                point_moves += 1
            floating_second[2] = cls.__move_the_mantissa(floating_second[2], point_moves)
        else:
            point_moves: int = 0
            while not cls.are_binary_numbers_equal(floating_first[1], floating_second[1]):
                floating_first[1] = cls.__binary_summation(floating_first[1], "00000001")
                point_moves += 1
            floating_first[2] = cls.__move_the_mantissa(floating_first[2], point_moves)
        new_mantissa = cls.binary_numbers_sum(floating_first[0] + floating_first[2],
                                              floating_second[0] + floating_second[2])
        return [new_mantissa[0], floating_second[1], new_mantissa[1:]]

    @classmethod
    def floating_point_to_decimal(cls, floating_point_number: list[str, str, str]):
        decimal_degree: int = cls.translate_to_decimal("0" + floating_point_number[1]) - 127
        digit_degree = 0
        result: float = 0
        for digit in floating_point_number[2]:
            result += int(digit)*2**(digit_degree - 1)
            digit_degree -= 1
        module: float = (result + 1) * (2**decimal_degree)
        return (-1) * module if floating_point_number[0] == "1" else module


# print(BinaryCalculator.fixed_point_to_decimal(BinaryCalculator.binary_numbers_division(14, 23)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_sum_from_int(23, -11)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_sum_from_int(-23, -11)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_sum_from_int(23, 11)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_sum_from_int(-23, -11)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(14, 23)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(-14, 23)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(14, -23)))
# print(BinaryCalculator.translate_to_decimal(BinaryCalculator.binary_numbers_product(-14, -23)))
print(BinaryCalculator.floating_point_to_decimal(BinaryCalculator.floating_point_summary(1441, 2301)))
