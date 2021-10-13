'''
Author: Li Ji
Date: 2021-10-11 14:20:04
LastEditTime: 2021-10-12 03:14:40
Description: 如何使用tree-sitter.
Software:VSCode,env:infer
'''


from tree_sitter import Language, Parser
import sys
import logging
from pathlib import Path

#logging config
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'    
                    )

def my_language(language_name:str):
    build_dir = Path(r'./build')
    #reference:https://zhuanlan.zhihu.com/p/139783331
    language_vocabulary = list(build_dir.glob('*.so'))
    language_vocabulary = [x.stem for x in language_vocabulary]
    if language_name in language_vocabulary:
        language_file = r'{}/{}.so'.format(str(build_dir),language_name)
    logging.debug(language_file)
    #logging.debug(isinstance(language_file,str))
    return Language(language_file,language_name)
def code_parse_ast(content:str,language_name:str):
    parser = Parser()
    parser.set_language(my_language(language_name))

    tree = parser.parse(bytes(content, "utf8"))
    return tree
def make_move(cursor, move, all_nodes):
    # 递归遍历该树，把每个节点的信息保存起来，包括结点的类型、涉及范围的代码行起始位置、终止位置。
    # cursor: 即当前光标的位置（即节点的位置），通过cursor.node即可获取当前节点
    # move: 把move参数作为当前节点的移动方向
    # all_nodes: 保存节点信息的列表 （保存的是前序遍历的结果：根左右）

    if (move == "down"):
        all_nodes.append(cursor.node)
        if (cursor.goto_first_child()):
            make_move(cursor, "down", all_nodes)
        elif (cursor.goto_next_sibling()):
            make_move(cursor, "right", all_nodes)
        elif (cursor.goto_parent()):
            make_move(cursor, "up", all_nodes)
    elif (move == "right"):
        all_nodes.append(cursor.node)
        if (cursor.goto_first_child()):
            make_move(cursor, "down", all_nodes)
        elif (cursor.goto_next_sibling()):
            make_move(cursor, "right", all_nodes)
        elif (cursor.goto_parent()):
            make_move(cursor, "up", all_nodes)
    elif move == "up":
        if (cursor.goto_next_sibling()):
            make_move(cursor, "right", all_nodes)
        elif (cursor.goto_parent()):
            make_move(cursor, "up", all_nodes)

def tree_transform(tree):
    pass

if __name__ == "__main__":
    with open('hs.txt','r',encoding='utf-8') as f:
        content = f.read()
    parse_language = 'python'
    tree = code_parse_ast(content,parse_language)
    print(tree)
    cursor = tree.walk()
    all_nodes = []
    make_move(cursor, "down", all_nodes)
    print(all_nodes)
    #print(tree.root_node.sexp())