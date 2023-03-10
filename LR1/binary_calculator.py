# Variant 7
import random
from typing import Union


class BinaryCalculator:
    """Calculator, which translates two given integer|float decimal numbers to binary form
    and performs operations on them. Each integer number contains 16 bits,
    (most significant bit is for sign) which means such numbers lie in [-2^15; 2^15-1] interval.
    Floating point numbers are presented in single-precision (32 bits), just like float type"""

    @classmethod
    def convert_int_to_binary(cls, number: int, bit_amount: int = 16) -> str:
        """Convert given integer number two binary form. Only 16 binary integer numbers supported,
        so please, don't use it for huge numbers"""
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
    def convert_float_to_binary(cls, number: float, bit_amount: int = 16) -> str:
        """Convert float decimal number to binary point form. Whole part and fraction are separated by dot"""
        minus_bit = "1" if number < 0 else "0"
        number = abs(number)
        whole_part = int(number)
        fraction: float = number - float(whole_part)
        binary_number: str = cls.convert_int_to_binary(whole_part)[1:]
        if binary_number.find("1") == -1:
            binary_number = minus_bit + "0."
        else:
            binary_number = minus_bit + binary_number[binary_number.find("1"):] + "."
        for i in range(bit_amount - len(binary_number) - 1):
            fraction *= 2
            binary_number += "0" if int(fraction) == 0 else "1"
            fraction = fraction - float(int(fraction))
        return binary_number

    @classmethod
    def convert_to_decimal(cls, binary_number: str) -> int:
        """Convert binary integer number to decimal form"""
        number = 0
        for i in range(1, len(binary_number)):
            number += 2 ** (len(binary_number) - 1 - i) * int(binary_number[i])
        return (1 - 2 * int(binary_number[0])) * number

    @classmethod
    def is_binary_number_positive(cls, binary_number: str) -> bool:
        """Returns True if number is greater or equal to zero. False otherwise.
        Number is represented in binary form"""
        return True if binary_number[0] == "0" else False

    @classmethod
    def binary_abs(cls, binary_number: str) -> str:
        """Returns |binary_number| (that's module, if you don't know)"""
        return "0" + binary_number[1:]

    @classmethod
    def is_binary_module_greater_than(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        """Returns True if |compared_binary_one| > |compared_binary_two|. False otherwise. Both numbers are represented
        in binary form"""
        for i in range(len(compared_binary_one)):
            if compared_binary_one[i] == "1" and compared_binary_two[i] == "0":
                return True
            elif compared_binary_one[i] == "0" and compared_binary_two[i] == "1":
                return False
        return False

    @classmethod
    def are_binary_numbers_equal(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        """Returns True if compared_binary_one equals to compared_binary_two. False otherwise.
         Both numbers are represented in binary form"""
        for i in range(len(compared_binary_one)):
            if compared_binary_one[i] != compared_binary_two[i]:
                return False
        return True

    @classmethod
    def is_binary_greater_than(cls, compared_binary_one: str, compared_binary_two: str) -> bool:
        """Returns True if compared_binary_one > compared_binary_two. False otherwise. Both numbers are represented
        in binary form"""
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
        """Rounding of binary number. Add one to rounded digit if there is at least single one after it.
        Adds zero otherwise"""
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
        """Binary numbers addition. Sign is taken into account. Method converts number to twos complement if it is
        negative"""
        if cls.is_binary_number_positive(binary_first_number) and cls.is_binary_number_positive(binary_second_number):
            return cls.__unsigned_binary_addition(binary_first_number, binary_second_number)
        binary_first_number_converted: str = binary_first_number if binary_first_number[0] == "0" \
            else cls.twos_complement(binary_first_number)
        binary_second_number_converted: str = binary_second_number if binary_second_number[0] == "0" \
            else cls.twos_complement(binary_second_number)
        return cls.twos_complement(cls.__unsigned_binary_addition(binary_first_number_converted,
                                                                  binary_second_number_converted))

    @classmethod
    def binary_numbers_sum_from_int(cls, first_number: int, second_number: int) -> str:
        """Just give it two integer numbers, and it will return you binary form of addition.
        Don't forget to convert it to decimal form after"""
        binary_first_number: str = cls.convert_int_to_binary(first_number)
        binary_second_number: str = cls.convert_int_to_binary(second_number)
        return cls.binary_numbers_sum(binary_first_number, binary_second_number)

    @classmethod
    def binary_numbers_subtraction(cls, first_number: int, second_number: int) -> str:
        """Subtraction is just addition, but sign of second operand becomes opposite"""
        return cls.binary_numbers_sum_from_int(first_number, -second_number)

    @classmethod
    def __unsigned_binary_addition(cls, binary_first: str, binary_second: str) -> str:
        """'Stupid' addition of binary numbers. No matter which sign is"""
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
        """Ones complement for signed addition (subtraction). Useless for positive numbers as you get
        same number in such case"""
        reversed_digits: dict = {"0": "1", "1": "0", ".": "."}
        if binary_number[0] == "0":
            return binary_number
        ones_complement = "1" + "".join([reversed_digits[i] for i in binary_number[1:]])
        return ones_complement

    @classmethod
    def twos_complement(cls, binary_number: str) -> str:
        """Twos complement. Used for signed addition (subtraction). Useless for positive numbers
        as you get same number in such case"""
        if binary_number[0] == "0":
            return binary_number
        binary_number = cls.ones_complement(binary_number)
        return cls.__unsigned_binary_addition(binary_number,
                                              cls.convert_int_to_binary(1, bit_amount=len(binary_number)))

    @classmethod
    def modified_twos_complement(cls, binary_number: str) -> str:
        """Modified twos complement for mantissa addition"""
        if binary_number[0] == "0":
            return "0" + binary_number
        binary_number = cls.ones_complement(binary_number)
        return "1" + cls.__unsigned_binary_addition(binary_number,
                                                    cls.convert_int_to_binary(1, bit_amount=len(binary_number)))

    @classmethod
    def binary_numbers_product(cls, first_number: int, second_number: int) -> str:
        """Signed binary numbers product. Actually, this method only specifies sign of the production and
        then makes unsigned product."""
        binary_first_number: str = cls.convert_int_to_binary(first_number)
        binary_second_number: str = cls.convert_int_to_binary(second_number)
        sign: str = "0" if binary_first_number[0] == binary_second_number[0] else "1"
        return sign + cls.__binary_modules_product(binary_first_number, binary_second_number)

    @classmethod
    def __binary_modules_product(cls, binary_first: str, binary_second: str) -> str:
        """Unsigned binary numbers product"""
        binary_result: str = "0" * len(binary_first)
        for i in range(len(binary_first) - 1, 0, -1):
            if binary_first[i] == "1":
                shifted_sum: str = binary_second[(len(binary_first) - 1 - i):] + "0" * (len(binary_first) - 1 - i)
                binary_result = cls.__unsigned_binary_addition(binary_result, shifted_sum)
        return binary_result

    @classmethod
    def binary_numbers_division(cls, dividend: int, divider: int) -> str:
        """Divide number_1 by number_2, represented in binary form. Works only if |number_1| < |number_2|.
        ValueError otherwise"""
        binary_dividend: str = cls.convert_int_to_binary(dividend)
        binary_divider: str = cls.convert_int_to_binary(divider)
        sign: str = "0" if binary_dividend[0] == binary_divider[0] else "1"
        remainder: str = cls.binary_numbers_subtraction(abs(dividend), abs(divider))
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
        # result = cls.binary_number_round(result, 9)
        return sign + "0." + result

    @classmethod
    def fixed_point_to_decimal(cls, fixed_point_number: str) -> float:
        """Convert fixed point number to decimal form"""
        fraction: str = fixed_point_number[3:]
        result: float = 0
        for i in range(len(fraction)):
            result += int(fraction[i]) * (2 ** (-(i + 1)))
        return -result if fixed_point_number[0] == "1" else result

    @classmethod
    def convert_to_floating_point(cls, number: Union[int, float]) -> list[str, str, str]:
        """Convert decimal number to floating point form"""
        if number == 0:
            return ["0", "01111111", "0" * 23]
        sign = "1" if number < 0 else "0"
        if isinstance(number, int):
            binary_number = cls.convert_int_to_binary(number)[1:]
            digit_order: int = len(binary_number) - (binary_number.find("1") + 1)
        else:
            binary_number = cls.convert_float_to_binary(number, bit_amount=32)[1:]
            digit_order = binary_number.find(".") - (binary_number.find("1") + 1)
            digit_order += 1 if digit_order < 0 else 0
            binary_number_list: list = list(binary_number)
            binary_number_list.pop(binary_number_list.index("."))
            binary_number = "".join(binary_number_list)
        exponent: str = cls.binary_numbers_sum(cls.convert_int_to_binary(127, 9),
                                               cls.convert_int_to_binary(digit_order, bit_amount=9))[1:]
        mantissa = binary_number[binary_number.find("1"):]
        if len(mantissa) < 23:
            mantissa += "0" * (23 - len(mantissa))
        else:
            mantissa = mantissa[:23]
        return [sign, exponent, mantissa]

    @classmethod
    def __move_the_mantissa(cls, mantissa: str, mantissa_moves: int) -> str:
        """Move the mantissa after exponent normalizing"""
        if mantissa_moves == 0:
            return mantissa
        return "0" * mantissa_moves + mantissa[:-mantissa_moves]

    @classmethod
    def __mantissa_addition(cls, floating_first: list[str, str, str],
                            floating_second: list[str, str, str]) -> list[str, str, str]:
        """Addition of floating point numbers mantissas"""
        first_mantissa = cls.modified_twos_complement(floating_first[0] + floating_first[2])
        second_mantissa = cls.modified_twos_complement(floating_second[0] + floating_second[2])
        order: str = floating_first[1]
        new_mantissa = cls.__unsigned_binary_addition(first_mantissa, second_mantissa)
        if new_mantissa[:2] in ("10", "01"):
            order = cls.__unsigned_binary_addition(order, "00000001")
            new_mantissa = new_mantissa[0] + new_mantissa[:len(new_mantissa)-1]
        sign: str = "0" if new_mantissa[:2] == "00" else "1"
        new_mantissa = cls.twos_complement(new_mantissa[1:])[1:]
        new_floating_point = [sign, order, new_mantissa]
        return new_floating_point

    @classmethod
    def __exponent_normalizing(cls, floating_first: list[str, str, str], floating_second: list[str, str, str]) -> tuple:
        """Make exponents of two floating point numbers equal"""
        if cls.is_binary_module_greater_than(floating_first[1], floating_second[1]):
            point_moves: int = 0
            while not cls.are_binary_numbers_equal(floating_first[1], floating_second[1]):
                floating_second[1] = cls.__unsigned_binary_addition(floating_second[1], "00000001")
                point_moves += 1
            floating_second[2] = cls.__move_the_mantissa(floating_second[2], point_moves)
        else:
            point_moves: int = 0
            while not cls.are_binary_numbers_equal(floating_first[1], floating_second[1]):
                floating_first[1] = cls.__unsigned_binary_addition(floating_first[1], "00000001")
                point_moves += 1
            floating_first[2] = cls.__move_the_mantissa(floating_first[2], point_moves)
        return floating_first, floating_second

    @classmethod
    def floating_point_summary(cls, first_number: Union[int, float],
                               second_number: Union[int, float]) -> list[str, str, str]:
        """Addition of two floating point numbers"""
        floating_first: list[str, str, str] = cls.convert_to_floating_point(first_number)
        floating_second: list[str, str, str] = cls.convert_to_floating_point(second_number)
        floating_first, floating_second = cls.__exponent_normalizing(floating_first, floating_second)
        new_floating_point = cls.__mantissa_addition(floating_first, floating_second)
        return new_floating_point

    @classmethod
    def floating_point_to_decimal(cls, floating_point_number: list[str, str, str]):
        """Convert floating point form to decimal number"""
        decimal_degree: int = cls.convert_to_decimal("0" + floating_point_number[1]) - 127
        digit_degree = 0
        mantissa_result: float = 0
        for digit in floating_point_number[2]:
            mantissa_result += int(digit)*2**digit_degree
            digit_degree -= 1
        return (1 - 2 * int(floating_point_number[0])) * mantissa_result * 2**decimal_degree


def get_two_random_ints() -> tuple[int, int]:
    return random.randint(-127, 128), random.randint(-127, 128)


def get_two_random_floats() -> tuple[float, float]:
    return random.choice([-1, 1])*round(random.randint(-127, 128)*random.random(), 4),\
        random.choice([-1, 1])*round(random.randint(-127, 128)*random.random(), 4)


def test_addition() -> None:
    print("-"*62)
    print("|\tADDITION"+" "*(60 - len("|\tADDITION") - 1)+"|")
    random_ints: tuple[int, int] = get_two_random_ints()
    result: Union[int, float] = BinaryCalculator.convert_to_decimal(
        BinaryCalculator.binary_numbers_sum_from_int(random_ints[0], random_ints[1]))
    result_str: str = f"|\t{random_ints[0]} + {random_ints[1]} = {result}"
    print(result_str+" "*(60 - len(result_str) - 1)+"|")
    print("-" * 62)


def test_subtraction() -> None:
    print("-" * 62)
    print("|\tSUBTRACTION" + " " * (60 - len("|\tSUBTRACTION") - 1) + "|")
    random_ints: tuple[int, int] = get_two_random_ints()
    result: Union[int, float] = BinaryCalculator.convert_to_decimal(
        BinaryCalculator.binary_numbers_subtraction(random_ints[0], random_ints[1]))
    result_str: str = f"|\t{random_ints[0]} - {random_ints[1]} = {result}"
    print(result_str + " " * (60 - len(result_str) - 1) + "|")
    print("-" * 62)


def test_multiplication() -> None:
    print("-" * 62)
    print("|\tMULTIPLICATION" + " " * (60 - len("|\tMULTIPLICATION") - 1) + "|")
    random_ints: tuple[int, int] = get_two_random_ints()
    result: Union[int, float] = BinaryCalculator.convert_to_decimal(
        BinaryCalculator.binary_numbers_product(random_ints[0], random_ints[1]))
    result_str: str = f"|\t{random_ints[0]} * {random_ints[1]} = {result}"
    print(result_str + " " * (60 - len(result_str) - 1) + "|")
    print("-" * 62)


def test_division() -> None:
    print("-" * 62)
    print("|\tDIVISION (works if |x1| < |x2|)" + " " * (60 - len("|\tDIVISION (works if |x1| < |x2|)") - 1) + "|")
    random_ints: tuple[int, int] = (random.randint(-10, 10), random.randint(25, 50))
    result: Union[int, float] = BinaryCalculator.fixed_point_to_decimal(
        BinaryCalculator.binary_numbers_division(random_ints[0], random_ints[1])
    )
    result_str: str = f"|\t{random_ints[0]} / {random_ints[1]} ~ {result}"
    print(result_str + " " * (60 - len(result_str) - 1) + "|")
    print("-" * 62)


def test_floating_point_addition() -> None:
    print("-" * 62)
    print("|\tFLOATING POINT ADDITION" + " " * (60 - len("|\tFLOATING POINT ADDITION") - 1) + "|")
    random_floats: tuple[float, float] = get_two_random_floats()
    result = BinaryCalculator.floating_point_to_decimal(
        BinaryCalculator.floating_point_summary(random_floats[0], random_floats[1])
    )
    result_str: str = f"|\t{random_floats[0]} + {random_floats[1]} ~ {result}"
    print(result_str + " " * (60 - len(result_str) - 1) + "|")
    print("-" * 62)


if __name__ == "__main__":
    # You don't rule the situation, ha-ha. Look at the tests. Just run that file using python command.
    # Make sure you've got python interpreter for that. Try that several times and you will see different situations
    test_addition()
    test_subtraction()
    test_multiplication()
    test_division()
    test_floating_point_addition()
