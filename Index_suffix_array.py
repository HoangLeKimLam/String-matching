
# ==========================================================
# BUILD SUFFIX ARRAY (O(n log n) – prefix doubling)
# ==========================================================

def build_suffix_array(text):
    """
    Xây suffix array bằng thuật toán prefix-doubling.
    Độ phức tạp: O(n log n)

    Ý tưởng:
    - ban đầu xếp hạng suffix theo ký tự đầu
    - mỗi vòng lặp tăng gấp đôi độ dài prefix dùng để so sánh
    - khi prefix >= n thì suffix đã được sắp xếp hoàn chỉnh
    """

    n = len(text)

    # rank[i] lưu thứ hạng hiện tại của suffix bắt đầu tại i
    rank = [ord(c) for c in text]

    # suffix array ban đầu là các vị trí trong text
    sa = list(range(n))

    k = 1

    while k < n:

        # sắp xếp suffix theo:
        # (rank prefix đầu, rank prefix tiếp theo)
        sa.sort(key=lambda x: (rank[x], rank[x + k] if x + k < n else -1))

        new_rank = [0] * n

        for i in range(1, n):

            prev = sa[i - 1]
            curr = sa[i]

            prev_key = (rank[prev], rank[prev + k] if prev + k < n else -1)
            curr_key = (rank[curr], rank[curr + k] if curr + k < n else -1)

            # nếu hai suffix giống nhau ở prefix 2k
            if prev_key == curr_key:
                new_rank[curr] = new_rank[prev]
            else:
                new_rank[curr] = new_rank[prev] + 1

        rank = new_rank
        k *= 2

    return sa


# ==========================================================
# SEARCH PATTERN BẰNG BINARY SEARCH TRÊN SUFFIX ARRAY
# ==========================================================

def search_pattern(text, pattern, sa):
    """
    Tìm tất cả vị trí xuất hiện của pattern trong text
    bằng binary search trên suffix array
    """

    n = len(text)
    m = len(pattern)

    left = 0
    right = n - 1

    results = []

    while left <= right:

        mid = (left + right) // 2
        start = sa[mid]

        substring = text[start:start + m]

        if substring == pattern:

            results.append(start)

            # tìm thêm các match bên trái
            i = mid - 1
            while i >= 0 and text[sa[i]:sa[i] + m] == pattern:
                results.append(sa[i])
                i -= 1

            # tìm thêm các match bên phải
            i = mid + 1
            while i < n and text[sa[i]:sa[i] + m] == pattern:
                results.append(sa[i])
                i += 1

            break

        elif substring < pattern:
            left = mid + 1
        else:
            right = mid - 1

    return sorted(results)


# ==========================================================
# DEMO TRƯỜNG HỢP 4
# NHIỀU TEXT + NHIỀU PATTERN
# ==========================================================

texts = [
    "banana",
    "ananas",
    "bandana"
]

patterns = [
    "ana",
    "ban",
    "na"
]

# nối tất cả text thành một chuỗi lớn
# dùng ký tự đặc biệt làm phân tách
combined_text = "#".join(texts)

print("Combined text:", combined_text)

# xây suffix array cho toàn bộ dữ liệu text
sa = build_suffix_array(combined_text)

print("Suffix Array:", sa)


# truy vấn nhiều pattern
for pattern in patterns:

    positions = search_pattern(combined_text, pattern, sa)

    print(f"\nPattern '{pattern}' found at positions:", positions)