from collections import deque


class Node:
    def __init__(self):
        self.children = {}   # các cạnh ký tự
        self.fail = None     # failure link
        self.output = []     # các pattern kết thúc tại node


class AhoCorasick:

    def __init__(self, patterns):

        self.root = Node()

        # xây trie từ các pattern
        for pattern in patterns:
            self.add_pattern(pattern)

        # xây failure links
        self.build_failure_links()


    def add_pattern(self, pattern):

        node = self.root

        for char in pattern:

            # tạo node mới nếu cần
            if char not in node.children:
                node.children[char] = Node()

            node = node.children[char]

        # đánh dấu kết thúc pattern
        node.output.append(pattern)


    def build_failure_links(self):

        queue = deque()

        # node con của root có fail = root
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:

            current = queue.popleft()

            for char, child in current.children.items():

                queue.append(child)

                fail_node = current.fail

                # tìm failure link phù hợp
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail

                if fail_node:
                    child.fail = fail_node.children[char]
                else:
                    child.fail = self.root

                # kế thừa output
                child.output += child.fail.output


    def search(self, text):

        node = self.root
        results = []

        for i, char in enumerate(text):

            # follow failure link nếu không có cạnh
            while node and char not in node.children:
                node = node.fail

            if not node:
                node = self.root
                continue

            node = node.children[char]

            # nếu có pattern kết thúc
            for pattern in node.output:
                results.append((i - len(pattern) + 1, pattern))

        return results
patterns = ["he", "she", "hers", "his"]

texts = [
    "ahishers",
    "she is here",
    "hershey chocolate"
]

ac = AhoCorasick(patterns)

for idx, text in enumerate(texts):

    matches = ac.search(text)

    print(f"\nText {idx+1}: {text}")

    for pos, pat in matches:
        print(f"Pattern '{pat}' found at position {pos}")