def build_bad_char_table(pattern):
    """
    Xây dựng bảng bad character.
    Bảng này lưu vị trí xuất hiện cuối cùng của mỗi ký tự trong pattern.
    
    Ví dụ:
    pattern = "ABCA"
    
    bảng sẽ là:
    A -> 3
    B -> 1
    C -> 2
    
    Mục đích:
    Khi mismatch xảy ra, ta biết ký tự đó xuất hiện cuối ở đâu trong pattern
    để dịch pattern xa nhất có thể.
    """
    
    bad_char = {}  # dictionary lưu vị trí cuối của mỗi ký tự
    
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i  # ghi đè để luôn giữ vị trí xuất hiện cuối
    
    return bad_char


def boyer_moore_search(text, pattern):
    
    n = len(text)      # độ dài text
    m = len(pattern)   # độ dài pattern
    
    # xây dựng bảng bad character
    bad_char = build_bad_char_table(pattern)
    
    result = []  # lưu các vị trí tìm thấy pattern
    
    s = 0  # s = shift (vị trí pattern đang đặt trên text)
    
    # chỉ chạy khi pattern còn nằm trọn trong text
    while s <= n - m:
        
        # bắt đầu so sánh từ ký tự cuối của pattern
        j = m - 1
        
        # so sánh từ phải sang trái
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        # nếu j < 0 nghĩa là đã match toàn bộ pattern
        if j < 0:
            
            # lưu vị trí tìm được
            result.append(s)
            
            # dịch pattern để tiếp tục tìm lần sau
            
            if s + m < n:
                # dùng bad character rule để quyết định nhảy
                s += m - bad_char.get(text[s + m], -1)
            else:
                # nếu đã gần cuối text thì chỉ cần nhảy 1
                s += 1
        
        else:
            # mismatch xảy ra tại vị trí j
            
            mismatch_char = text[s + j]  # ký tự gây mismatch
            
            # tìm vị trí xuất hiện cuối của ký tự này trong pattern
            last_occurrence = bad_char.get(mismatch_char, -1)
            
            # tính số bước nhảy theo bad character rule
            shift = j - last_occurrence
            
            # đảm bảo luôn nhảy ít nhất 1 bước
            s += max(1, shift)
    
    return result
text = "HERE IS A SIMPLE EXAMPLE"
pattern = "EXAMPLE"

positions = boyer_moore_search(text, pattern)

print("Pattern xuất hiện tại vị trí:", positions)