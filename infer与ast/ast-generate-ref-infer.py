'''
Author: Li Ji
Date: 2021-10-13 16:43:14
LastEditTime: 2021-10-13 18:01:54
Description: 参考infercode,修改的程序
Software:VSCode,env:infer
'''
from tree_sitter import Language,Parser
PY_LANGUAGE = Language(r'..\build\python.so', 'python')
ast_parser = Parser()
ast_parser.set_language(PY_LANGUAGE)

# Simplify the AST 
def simplify_ast(tree, text):
    # tree = self.ast_parser.parse(text)
    root = tree.root_node

    ignore_types = ["\n"]#2021-10-13:为什么只忽略\n
    num_nodes = 0
    root_type = str(root.type)#2021-10-13: 本来就是str.
    root_type_id = num_nodes
    queue = [root]

    root_json = {
        "node_type": root_type,
        "node_type_id": root_type_id,
        "node_tokens": [],
        "node_tokens_id": [],
        "children": []
    }

    queue_json = [root_json]
    while queue:
        
        current_node = queue.pop(0)
        current_node_json = queue_json.pop(0)#2021-10-13:两个队列,一个存节点,一个存节点的json
        num_nodes += 1#2021-10-13: 记录节点个数


        for child in current_node.children:
            child_type = str(child.type)
            if child_type not in ignore_types:
                queue.append(child)

                child_type_id = num_nodes

                child_token = ""
                child_sub_tokens_id = []
                child_sub_tokens = []
                
                has_child = len(child.children) > 0#2021-10-13: 判断有孩子吗

                if not has_child:#2021-10-13:没有孩子就读取终端节点,即文本内容.
                    child_token = text[child.start_byte:child.end_byte].decode()
                    child_sub_tokens_id = ['child_sub_tokens_id']
                    #subtokens = " ".join(identifiersplitting.split_identifier_into_parts(child_token))
                    #child_sub_tokens = self.token_vocab.tokenize(subtokens)

                if len(child_sub_tokens_id) == 0:
                    child_sub_tokens_id.append(0)
                else:
                    child_sub_tokens_id = [x for x in child_sub_tokens_id if x != 0]


                # print(children_sub_token_ids)
                child_json = {
                    "node_type": child_type,
                    "node_type_id": child_type_id,
                    "node_tokens": child_sub_tokens,
                    "node_tokens_id": child_sub_tokens_id,
                    "children": []
                }

                current_node_json['children'].append(child_json)
                queue_json.append(child_json)
    return root_json, num_nodes
def ast_picture(tree,text):
    from treelib import Tree,Node
    tree_clone = Tree()
    tree_id = 0
    tree_id_str = str(tree_id)
    node_id_list = list()
    tree_clone.create_node(tag=tree.root_node.type,identifier=tree_id_str,data=tree.root_node)
    node_id_list.append([tree.root_node,tree_id_str])
    print(node_id_list)
    print(type(node_id_list[0][0]))
    print(1)
    tree_clone.show()
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
        if node.child_count ==0:
            child_token = text[node.start_byte:node.end_byte].decode()
            print('token:',child_token)
            tree_id+=1
            tree_id_str = str(tree_id)
            node_id_list.append([child_token,tree_id_str])
            temp = [ j for j in range(len(node_id_list))if node_id_list[j][0]==node]
            tree_clone.create_node(tag='__'+child_token,identifier=tree_id_str,data='terminal',parent=node_id_list[temp[0]][1])
                  
    #tree_clone.show()
    import os
    tree_clone.to_graphviz(filename='tree.gv', shape='ellipse')
    check_gv('tree.gv')
    os.system('dot -Tpng tree.gv -o tree.gv1.png')
    os.startfile('tree.gv1.png')
def check_gv(gv_file):
    with open(gv_file,'r') as f:
        content = f.read()
    content = content.replace("\"\"\"","\"\\\"\"")
    with open(gv_file,'w') as f:
        f.write(content)
code_snippet = '''class apple(fruit):
    self.id = '001'
    def id():
        return self.id'''#错误的程序
code_snippet_to_byte = str.encode(code_snippet)
ast = ast_parser.parse(code_snippet_to_byte)
#tree_representation, _ = simplify_ast(ast, code_snippet_to_byte)
ast_picture(ast,code_snippet_to_byte)