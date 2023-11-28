#我想要写一个个人向的的背英语单词的小程序，有以下功能：
#1.可以写入单词，（若干个）中文释义，以及（若干个）例句等等
#2.能够打印指定前缀，后缀的所有单词
#TODO 3.可以打印指定中文的单词词条
#TODO 4.指定单词。打印出所有含有该单词的例句
#5.可以查询单词，如果没有存储：询问是否存储. 如果有存储，要显示历史被查询过的次数
#TODO 6.可以根据所指的前缀和后缀随机地挑选单词词条
#7.所有的单词词条必须可以存储在文件中，并且方便读写
#TODO 8.可以对指定的单词进行中文以及例句的更改、增加、删除
#TODO 9.可以删除单词

from vocabulary import VocabularyTrie, TrieNode

# 菜单类

class Menu:
    def __init__(self):
        print("欢迎使用背单词小程序！")
        print("正在加载词库...")
        self.vocabulary = VocabularyTrie("vocabulary.json")
        print("词库加载完成！")
        print("输入help或者h查看帮助")
        self.run()

    def __del__(self):
        print("再见！")

    def add_word(self, word: str):
        translation = input("请输入中文释义：")
        examples = []
        while True:
            example = input("请输入例句（输入空行结束）：")
            if example == "":
                break
            examples.append(example)

        if self.vocabulary.add_word(word, translation, examples):
            print("添加成功！")
        else:
            print("添加失败！")


    def search_word(self, word: str):
        result: TrieNode = self.vocabulary.search_word(word)
        if result:
            print("单词：", result.word)
            print("中文释义：", result.translation)
            print("例句：")
            for example in result.examples:
                print(example)
            print("查询次数：", result.search_count)
        else:
            print("单词未找到！")
            choice = input("是否添加到词库？(y/n)")
            if choice == "y":
                self.add_word(word)

    def print_words(self, prefix: str = "", suffix: str = ""):
        # 输入了空行
        if prefix == "" and suffix == "":
            self.print_all_words()
        elif prefix == "." and suffix == ".": # 前后缀都是任意字符
            self.print_all_words()
        elif prefix == ".": # 只有后缀
            self.print_words_with_suffix(suffix)
        elif suffix == "" or suffix == ".": # 只有前缀
            self.print_words_with_prefix(prefix)
        else: # 既有前缀又有后缀
            self.print_words_with_prefix_and_suffix(prefix, suffix)
    
    def print_all_words(self):
        print("所有单词：")
        for word in self.vocabulary.get_words():
            print(word)

    def print_words_with_prefix(self, prefix: str):
        print("所有以", prefix, "开头的单词：")
        for word in self.vocabulary.get_words(self.vocabulary.find_prefix(prefix)):
            print(word)

    def print_words_with_suffix(self, suffix: str):
        print("所有以", suffix, "结尾的单词：")
        for word in self.vocabulary.get_words(self.vocabulary.find_suffix(suffix)):
            # 颠倒输出
            print(word[::-1])

    def print_words_with_prefix_and_suffix(self, prefix: str, suffix: str):
        print("所有以", prefix, "开头，以", suffix, "结尾的单词：")
        for word in self.vocabulary.find_prefix_and_suffix(prefix, suffix):
            print(word)

    def parse_command(self, command: str):
        # 处理命令
        # parse command
        strings: list = command.split(" ")
        command = strings[0]
        args = strings[1:]
        # handle command
        if command == "add" or command == "a":
            if len(args) > 1:
                print("输入参数过多！")
                return
            if len(args) == 0:
                args.append(input("请输入单词："))
            word: str = args[0]
            if not word.isalpha():
                print("输入的单词不合法！")
                return
            self.add_word(word)
        elif command == "search" or command == "s":
            if len(args) > 1:
                print("输入参数过多！")
                return
            if len(args) == 0:
                args.append(input("请输入单词："))
            word: str = args[0]
            if not word.isalpha():
                print("输入的单词不合法！")
                return
            self.search_word(args[0])
        elif command == "print" or command == "p":
            if len(args) > 2:
                print("输入参数过多！")
                return
            if len(args) == 0:
                self.print_words()
            elif len(args) == 1:
                prefix: str = args[0]
                if not prefix.isalpha() and prefix != ".":
                    print("输入的前缀不合法！")
                    return
                self.print_words(prefix)
            else:
                prefix = args[0]
                suffix = args[1]
                if not prefix.isalpha() and prefix != ".":
                    print("输入的前缀不合法！")
                    return
                if not suffix.isalpha() and suffix != ".":
                    print("输入的后缀不合法！")
                    return
                self.print_words(prefix, suffix)
        elif command == "translate" or command == "t":
            self.print_words_with_translation()
        elif command == "example" or command == "e":
            self.print_examples_with_word()
        else:
            print("未知命令！")


                     
    def run(self):
        # 程序主循环
        while True:
            # 不换行输出, 打印一个类似bash的提示符
            print(">>>", end = "")
            
            command: str = input()
            command = command.strip()

            if command == "quit" or command == "q":
                self.vocabulary.save_to_json('vocabulary.json')
                break
            elif command == "help" or command == "h":
                print("add/a [WORD]                 添加单词")
                print("search/s [WORD]:             查询单词")
                print("print/p [PREFIX] [SUFFIX]    打印单词, 可以指定前缀和后缀, 只有一个输入表示前缀, .表示任意字符")
                print("translate/t [CHINESE]        根据中文释义搜索单词")
                print("example/e [WORD]             打印例句")
                print("quit/q                       退出程序")
                print("help/h                       打印帮助")
                continue
            elif command == "":
                continue
            
            self.parse_command(command)
    