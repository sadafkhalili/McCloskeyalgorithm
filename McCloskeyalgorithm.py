
import copy
from itertools import permutations


def count_different_bits(a, b):
    """
    تعداد بیت‌های متفاوت بین دو رشته باینری را محاسبه می‌کند
    """
    count = 0

    for i in range(len(a)):
        if a[i] != b[i]:
            count += 1

    return count


def merge_minterms(a, b):
    """
    دو مین‌ترم را با جایگزینی بیت‌های متفاوت با '-' ادغام می‌کند
    """
    result = ""

    for i in range(len(a)):
        if a[i] == b[i]:
            result += a[i]
        else:
            result += "-"

    return result


def find_next_column(minterms_dict, used_flags):
    """
    ستون بعدی در جدول کوارین-مک کلاکی را پیدا می‌کند
    با ترکیب مین‌ترم‌هایی که فقط در یک بیت تفاوت دارند
    """
    result = {}
    keys = list(minterms_dict.keys())

    # مقداردهی اولیه فلگ‌های استفاده
    for key in keys:
        used_flags[key] = False

    # بررسی تمام جفت‌های ممکن از مین‌ترم‌ها
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if count_different_bits(minterms_dict[keys[i]], minterms_dict[keys[j]]) == 1:
                new_key = keys[i] + "-" + keys[j]
                result[new_key] = merge_minterms(minterms_dict[keys[i]], minterms_dict[keys[j]])
                used_flags[keys[i]] = True
                used_flags[keys[j]] = True

    return result


def find_essential_prime_implicants(prime_implicants, minterms):
    """
    ضروری‌ترین پی‌آی‌ها را با استفاده از روش پتریک پیدا می‌کند
    """
    best_solution = None

    # بررسی تمام ترکیبات ممکن از پی‌آی‌ها
    for i in range(len(prime_implicants)):
        for combination in permutations(prime_implicants, i + 1):
            remaining_minterms = minterms[:]
            
            # حذف مین‌ترم‌های پوشش داده شده توسط این ترکیب
            for item in combination:
                for minterm in item.split("-"):
                    if int(minterm) in remaining_minterms:
                        remaining_minterms.remove(int(minterm))

            # اگر تمام مین‌ترم‌ها پوشش داده شدند
            if len(remaining_minterms) == 0:
                if best_solution is None or len(combination) < len(best_solution):
                    best_solution = combination

    return list(best_solution) if best_solution else []


def main():
    """
    تابع اصلی برای ساده‌سازی توابع بولین با استفاده از روش کوارین-مک کلاکی
    """
    # دریافت ورودی‌ها از کاربر
    variables = input("متغیرها را وارد کنید (با کاما جدا شده): ").replace(" ", "").split(",")
    n = len(variables)
    minterms = list(map(int, input("مین‌ترم‌ها را وارد کنید (با کاما جدا شده): ").replace(" ", "").split(",")))

    # تبدیل مین‌ترم‌ها به فرم باینری
    minterms_binary = {}
    for minterm in minterms:
        binary_str = bin(minterm)[2:]
        minterms_binary[str(minterm)] = (n - len(binary_str)) * '0' + binary_str

    # ایجاد جدول کوارین-مک کلاکی
    all_columns = [minterms_binary]
    used_implicants = {}

    # پیدا کردن تمام ستون‌های جدول
    next_column = find_next_column(all_columns[-1], used_implicants)
    while next_column:
        all_columns.append(next_column)
        next_column = find_next_column(all_columns[-1], used_implicants)

    # استخراج پی‌آی‌های اولیه (Prime Implicants)
    prime_implicants = [minterm for minterm in used_implicants if not used_implicants[minterm]]

    # ایجاد جدول پوشش برای پیدا کردن EPIها
    coverage_table = [[0 for _ in range(len(minterms))] for _ in range(len(prime_implicants))]

    for i in range(len(prime_implicants)):
        for minterm in prime_implicants[i].split("-"):
            coverage_table[i][minterms.index(int(minterm))] = 1

    # پیدا کردن Essential Prime Implicants (EPI)
    essential_pi = []
    remaining_minterms = copy.deepcopy(minterms)

    for i in range(len(minterms)):
        covering_pi = []

        for j in range(len(prime_implicants)):
            if coverage_table[j][i] == 1:
                covering_pi.append(j)

        # اگر فقط یک PI این مین‌ترم را پوشش دهد، EPI است
        if len(covering_pi) == 1:
            essential_pi.append(prime_implicants[covering_pi[0]])
            for minterm in prime_implicants[covering_pi[0]].split("-"):
                if int(minterm) in remaining_minterms:
                    remaining_minterms.remove(int(minterm))

    # حذف EPIها از لیست PIهای اصلی
    for epi in essential_pi:
        prime_implicants.remove(epi)

    # پیدا کردن PIهای باقیمانده ضروری
    final_pi = find_essential_prime_implicants(prime_implicants, remaining_minterms)
    all_essential_pi = essential_pi + final_pi

    # تبدیل به فرم نهایی تابع بولین
    result_terms = []
    for pi in all_essential_pi:
        binary_format = None

        # پیدا کردن فرمت باینری مربوط به این PI
        for column in all_columns:
            if pi in column:
                binary_format = column[pi]
                break

        if binary_format:
            term = ""
            for i in range(len(binary_format)):
                if binary_format[i] == '0':
                    term += variables[i] + "'"  # مکمل متغیر
                elif binary_format[i] == '1':
                    term += variables[i]        # متغیر اصلی

            result_terms.append(term)

    # چاپ نتیجه نهایی
    print(" + ".join(result_terms))


if __name__ == '__main__':
    main()