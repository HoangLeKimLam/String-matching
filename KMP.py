def compute_lps(pattern):
    """
    Hàm tính bảng LPS (Longest Prefix Suffix)

    LPS[i] = độ dài prefix dài nhất của pattern
             cũng là suffix của pattern[0..i]

    Ví dụ:
    pattern = "ABABAC"

    index : 0 1 2 3 4 5
    char  : A B A B A C
    LPS   : 0 0 1 2 3 0

    Mục đích của LPS:
    Khi mismatch xảy ra, ta biết phải quay về vị trí nào trong pattern
    mà không cần so sánh lại từ đầu.
    """

    m = len(pattern)

    lps = [0] * m   # khởi tạo mảng LPS toàn 0

    length = 0      # độ dài prefix-suffix hiện tại
    i = 1           # bắt đầu từ ký tự thứ 2

    while i < m:

        # nếu ký tự trùng -> mở rộng prefix-suffix
        if pattern[i] == pattern[length]:

            length += 1
            lps[i] = length

            i += 1

        else:
            # nếu mismatch và length != 0
            # quay lại prefix nhỏ hơn
            if length != 0:

                length = lps[length - 1]

            else:
                # không có prefix nào
                lps[i] = 0
                i += 1

    return lps
def kmp_search(text, pattern):
    """
    Thuật toán KMP tìm pattern trong text.

    Ý tưởng:
    - so sánh từ trái sang phải
    - khi mismatch -> dùng LPS để dịch pattern
    - KHÔNG quay lại text
    """

    n = len(text)
    m = len(pattern)

    # bước 1: tính bảng LPS của pattern
    lps = compute_lps(pattern)

    result = []  # lưu các vị trí match

    i = 0  # con trỏ text
    j = 0  # con trỏ pattern

    while i < n:

        # nếu ký tự text và pattern trùng nhau
        if text[i] == pattern[j]:

            i += 1
            j += 1

        # nếu match hết pattern
        if j == m:

            # tìm thấy pattern
            result.append(i - j)

            # tiếp tục tìm pattern tiếp theo
            j = lps[j - 1]

        # nếu mismatch
        elif i < n and text[i] != pattern[j]:

            # nếu đã match được một phần pattern
            if j != 0:

                # dùng LPS để nhảy trong pattern
                j = lps[j - 1]

            else:
                # nếu mismatch ngay đầu pattern
                # chỉ cần tăng con trỏ text
                i += 1

    return result
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"

positions = kmp_search(text, pattern)

print("Pattern xuất hiện tại vị trí:", positions)