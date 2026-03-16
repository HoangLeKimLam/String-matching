from collections import deque


class Node:
    def __init__(self):
        self.children = {}   # các cạnh đi xuống trie
        self.fail = None     # failure link
        self.output = []     # các pattern kết thúc tại node này


class AhoCorasick:

    def __init__(self, patterns):

        self.root = Node()

        # bước 1: xây trie từ các pattern
        for pattern in patterns:
            self.add_pattern(pattern)

        # bước 2: xây failure links
        self.build_failure_links()


    def add_pattern(self, pattern):
        """
        Thêm một pattern vào trie.
        Mỗi ký tự tạo một node nếu chưa tồn tại.
        """

        node = self.root

        for char in pattern:

            # nếu chưa có cạnh ký tự này thì tạo node mới
            if char not in node.children:
                node.children[char] = Node()

            node = node.children[char]

        # node cuối đánh dấu pattern kết thúc
        node.output.append(pattern)


    def build_failure_links(self):
        """
        Xây failure link bằng BFS.
        Failure link giống ý tưởng LPS của KMP:
        nếu mismatch thì quay về prefix dài nhất.
        """

        queue = deque()

        # các node con trực tiếp của root
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        # BFS qua trie
        while queue:

            current = queue.popleft()

            for char, child in current.children.items():

                queue.append(child)

                # tìm failure link cho child
                fail_node = current.fail

                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail

                if fail_node:
                    child.fail = fail_node.children[char]
                else:
                    child.fail = self.root

                # kế thừa output
                child.output += child.fail.output


    def search(self, text):
        """
        Duyệt text chỉ 1 lần để tìm tất cả pattern.
        """

        node = self.root
        results = []

        for i, char in enumerate(text):

            # nếu không có cạnh thì follow failure link
            while node and char not in node.children:
                node = node.fail

            if not node:
                node = self.root
                continue

            node = node.children[char]

            # nếu node có pattern kết thúc
            for pattern in node.output:
                results.append((i - len(pattern) + 1, pattern))

        return results
patterns = ["he", "she", "hers", "his"]

text = "ahishers"

ac = AhoCorasick(patterns)

matches = ac.search(text)

for pos, pat in matches:
    print(f"Pattern '{pat}' found at position {pos}")