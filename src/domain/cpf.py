import re


def normalize_cpf(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def is_valid_cpf(value: str) -> bool:
    cpf = normalize_cpf(value)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_digit(base: str, factor: int) -> str:
        total = sum(int(digit) * (factor - index) for index, digit in enumerate(base))
        mod = total % 11
        return "0" if mod < 2 else str(11 - mod)

    return cpf[-2:] == calc_digit(cpf[:9], 10) + calc_digit(cpf[:10], 11)
