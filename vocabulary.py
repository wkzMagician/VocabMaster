#我想要写一个个人向的的背英语单词的小程序，有以下功能：
#1.可以写入单词，（若干个）中文释义，以及（若干个）例句等等
#2.能够打印指定前缀，后缀的所有单词
#TODO 3.可以打印指定中文的单词词条
#TODO 4.指定单词。打印出所有含有该单词的例句
#TODO 5.可以查询单词，如果没有存储：询问是否存储. 如果有存储，要显示历史被查询过的次数
#TODO 6.可以根据所指的前缀和后缀随机地挑选单词词条
#TODO 7.所有的单词词条必须可以存储在文件中，并且方便读写
#TODO 8.可以对指定的单词进行中文以及例句的更改、增加、删除
#TODO 9.可以删除单词

import json

class TrieNode:
    def __init__(self):
        self.children = {} # 存储子节点
        self.word = None  # 存储完整单词
        self.translation = None # 存储中文释义
        self.examples = [] # 存储例句
        self.search_count = 0 # 存储查询次数

class TriedTree:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str, translation: str, examples: str):
        node = self.root
        # 遍历单词的每一个字母
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char] # 进入子节点

        if node.word is not None:
            return False
        else:
            node.word = word
            node.translation = translation
            node.examples = examples
            return True

    def search_word(self, query: str):
        node = self.root
        # 遍历查询单词的每一个字母
        for char in query:
            if char not in node.children:
                return None
            node = node.children[char]

        if node.word is not None: # 如果查询到了单词
            node.search_count += 1
            return node

        return None
    
    def find_prefix(self, prefix: str):
        # 找到前缀
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def to_dict(self, node: TrieNode = None):
        # 递归地将Trie转换为字典
        # 用来保存到JSON文件
        if node is None:
            node = self.root

        result = {
            'word': node.word,
            'translation': node.translation,
            'examples': node.examples,
            'search_count': node.search_count,
            'children': {}
        }

        for char, child_node in node.children.items():
            result['children'][char] = self.to_dict(child_node)

        return result

    def save_to_json(self, filename: str):
        # 将Trie保存到JSON文件
        data = self.to_dict()
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def load_from_json(self, filename: str):
        # 从JSON文件加载Trie
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.root = self.from_dict(data)
        except FileNotFoundError:
            # Handle the case where the file does not exist yet
            pass

    def from_dict(self, data: dict):
        # 递归地从字典加载Trie
        node = TrieNode()
        node.word = data['word']
        node.translation = data['translation']
        node.examples = data['examples']
        node.search_count = data['search_count']

        for char, child_data in data['children'].items():
            node.children[char] = self.from_dict(child_data)

        return node

class VocabularyTrie:
    def __init__(self, filename: str):
        # 前缀树以及后缀树
        self.prefix_trie = TriedTree()
        self.suffix_trie = TriedTree()
        self.load_from_json(filename)

    def save_to_json(self, filename: str):
        # 将前缀树和后缀树保存到JSON文件
        data = {
            'prefix_trie': self.prefix_trie.to_dict(),
            'suffix_trie': self.suffix_trie.to_dict()
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def load_from_json(self, filename: str):
        # 从JSON文件加载前缀树和后缀树
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.prefix_trie.root = self.prefix_trie.from_dict(data['prefix_trie'])
                self.suffix_trie.root = self.suffix_trie.from_dict(data['suffix_trie'])
        except FileNotFoundError:
            # Handle the case where the file does not exist yet
            pass

    def add_word(self, word: str, translation: str, examples: str):
        # 向前缀树和后缀树添加单词
        flag: bool = self.prefix_trie.add_word(word, translation, examples)
        self.suffix_trie.add_word(word[::-1], translation, examples) # 反转单词后添加
        return flag

    def search_word(self, query: str):
        # 查询单词， 默认用前缀树查询
        return self.prefix_trie.search_word(query)
    
    def find_prefix(self, prefix: str):
        # 在前缀树中查找前缀
        return self.prefix_trie.find_prefix(prefix)
    
    def find_suffix(self, suffix: str):
        # 在后缀树中查找后缀
        return self.suffix_trie.find_prefix(suffix[::-1])
    
    def get_words(self, node: TrieNode = None):
        if node is None: # 如果没有指定节点，则从前缀树根节点开始
            node = self.prefix_trie.root
        # 递归地获取所有单词
        words = []
        if node.word is not None:
            words.append(node.word)
        for child_node in node.children.values():
            words += self.get_words(child_node)
        return words
    
    def find_prefix_and_suffix(self, prefix: str, suffix: str):
        # 在前缀树和后缀树中查找前缀和后缀
        prefix_node = self.find_prefix(prefix)
        suffix_node = self.find_suffix(suffix)
        prefix_words = self.get_words(prefix_node)
        suffix_words = self.get_words(suffix_node)
        # 颠倒后缀树中的单词
        suffix_words = [word[::-1] for word in suffix_words]
        return list(set(prefix_words) & set(suffix_words))
 