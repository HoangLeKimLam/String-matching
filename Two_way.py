def max_suffix(s):
    """
    Tìm max suffix để xác định critical position.
    
    Hàm này được dùng trong thuật toán Crochemore–Perrin
    để xác định vị trí phân tách pattern.
    """

    n = len(s)

    ms = -1      # vị trí max suffix
    j = 0
    k = 1
    p = 1       # period tạm thời

    while j + k < n:

        if s[j + k] == s[ms + k]:
            if k == p:
                j += p
                k = 1
            else:
                k += 1

        elif s[j + k] > s[ms + k]:
            j += k
            k = 1
            p = j - ms

        else:
            ms = j
            j = ms + 1
            k = p = 1

    return ms, p
def critical_factorization(pattern):
    """
    Tìm critical position và period của pattern.
    """

    ms1, p1 = max_suffix(pattern)
    ms2, p2 = max_suffix(pattern[::-1])

    # chọn vị trí lớn hơn
    if ms1 > ms2:
        return ms1 + 1, p1
    else:
        return ms2 + 1, p2
def two_way_search(text, pattern):
    
    n = len(text)
    m = len(pattern)

    # tìm vị trí critical và period
    pos, period = critical_factorization(pattern)

    result = []

    i = 0  # vị trí trên text

    while i <= n - m:

        j = pos

        # so sánh phần right của pattern
        while j < m and pattern[j] == text[i + j]:
            j += 1

        if j < m:
            # mismatch ở phần right
            i += j - pos + 1
            continue

        # nếu phần right match → kiểm tra phần left
        j = pos - 1

        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            # tìm thấy pattern
            result.append(i)

        # dịch pattern theo period
        i += period

    return result
text = "HERE IS A SIMPLE EXAMPLE"
pattern = "EXAMPLE"

print(two_way_search(text, pattern))