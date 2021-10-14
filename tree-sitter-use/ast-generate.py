'''
Author: Li Ji
Date: 2021-10-13 16:43:14
LastEditTime: 2021-10-15 00:33:40
Description: 参考infercode,修改的程序
Software:VSCode,env:infer
'''
from os import name
from tree_sitter import Language,Parser
lang_dict = {
    'python' : r'build\python.so',
    'java'   : r'build\java.so',
    'c'      : r'build\c.so'
}


def ast_clone(tree,text):
    from treelib import Tree,Node
    tree_clone = Tree()
    tree_id = 0
    tree_id_str = str(tree_id)
    node_id_list = list()
    tree_clone.create_node(tag=tree.root_node.type,identifier=tree_id_str,data=tree.root_node)
    node_id_list.append([tree.root_node,tree_id_str])
    from collections import deque

    todo = deque([tree.root_node])
    while todo:
        node = todo.popleft()
        #print(node)
        if node.child_count:
            todo.extendleft(node.children)
            for i in node.children:
                tree_id+=1
                tree_id_str = str(tree_id)
                node_id_list.append([i,tree_id_str])
                temp = [ j for j in range(len(node_id_list))if node_id_list[j][0]==i.parent]
                tree_clone.create_node(tag=i.type,identifier=tree_id_str,data=i,parent=node_id_list[temp[0]][1])
                print(tree_id)
        if node.child_count ==0:
            child_token = text[node.start_byte:node.end_byte].decode()
            #print('token:',child_token)
            tree_id+=1
            tree_id_str = str(tree_id)
            node_id_list.append([child_token,tree_id_str])
            temp = [ j for j in range(len(node_id_list))if node_id_list[j][0]==node]
            tree_clone.create_node(tag='__'+child_token,identifier=tree_id_str,data='terminal',parent=node_id_list[temp[0]][1])
    return tree_clone              
    #tree_clone.show()
def ast_to_graphviz(tree,filename):
    import os
    tree.to_graphviz(filename=filename, shape='ellipse')
    check_gv(filename)
    os.system('dot -Tpng {0} -o {1}'.format(filename,filename+'.png'))
    print('---created ast_picture---')
    #pricture = filename+'.png'
    #os.startfile(pricture)
    return True
    
def check_gv(gv_file):
    with open(gv_file,'r') as f:
        content = f.read()
    content = content.replace('"""',r'"\""')
    content = content.replace('"__""',r'"__\""')
    with open(gv_file,'w') as f:
        f.write(content)
    return True
def code_to_ast_picture(code_snippet,filename,language):
    code_snippet_to_byte = str.encode(code_snippet)
    LANGUAGE = Language(lang_dict[language], language)
    ast_parser = Parser()
    ast_parser.set_language(LANGUAGE)
    ast = ast_parser.parse(code_snippet_to_byte)
    tree_clone = ast_clone(ast,code_snippet_to_byte)
    ast_to_graphviz(tree_clone,filename)
if __name__ == '__main__':
    # with open('python-code.txt','r') as f:
    #     code = f.read()
    #     code_to_ast_picture(code,r'.\ast_pictures\python-code.gv','python')
    # with open('c-code.txt','r') as f:
    #     code = f.read()
    #     code_to_ast_picture(code,r'.\ast_pictures\c-code.gv','c')
     with open('java-code.txt','r') as f:
        code = f.read()
        code_to_ast_picture(code,r'.\ast_pictures\java-code.gv','java')