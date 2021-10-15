'''
Author: Li Ji
Date: 2021-10-15 14:52:11
LastEditTime: 2021-10-16 00:39:55
Description: 关于python的ast可视化
Software:VSCode,env:
'''
#logging
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s : %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'
                    )
#import <library>
from treelib import Tree,Node
import ast
import json
from io import StringIO
def node_show(cursor):
    def name(child):
        return child.__class__.__name__
    show_str = 'Node_name: {0}\n'.format(name(cursor))
    content = list(ast.iter_fields(cursor))#以下程序就是解析这句话

    for i in content:
        if isinstance(i[1],str):
            s = '{0}: {1}\n'.format(i[0],i[1])
            show_str+=s
        if isinstance(i[1],ast.AST):
            s = '{0}: {1}\n'.format(i[0],name(i[1]))
            #print(s)
            show_str+=s
        if isinstance(i[1],list):
            if len(i[1])==0:
                s = '{0}: None\n'.format(i[0])
                #print(s)
                show_str+=s
            else:
                l = [name(x) for x in i[1]]
                s = '{0}: {1}\n'.format(i[0],str(l))
                #print(s)
                show_str+=s
    for i in cursor._attributes:
        getattr(cursor,i,'')
        s = '{0}: {1}\n'.format(i,getattr(cursor,i,''))
        show_str+=s
    return show_str

def ast_clone(tree,text=None):
    def name(node):
        return node.__class__.__name__
    from treelib import Tree,Node
    tree_clone = Tree()
    tree_id = 0
    tree_id_str = str(tree_id)
    node_id_list = list()
    cursor = tree
    #tree_clone.create_node(tag=tree.root_node.type,identifier=tree_id_str,data=tree.root_node)
    tree_clone.create_node(tag=node_show(cursor),identifier=tree_id_str,data=cursor)
    node_id_list.append([cursor,tree_id_str])
    from collections import deque

    todo = deque([cursor])
    while todo:
        node = todo.popleft()
        #print(node)
        if len(list(ast.iter_child_nodes(node))):
            todo.extendleft(ast.iter_child_nodes(node))
            for i in list(ast.iter_child_nodes(node)):
                tree_id+=1
                tree_id_str = str(tree_id)
                node_id_list.append([i,tree_id_str])
                temp = [ j for j in range(len(node_id_list))if node_id_list[j][0]==node]
                tree_clone.create_node(tag=node_show(i),identifier=tree_id_str,data=i,parent=node_id_list[temp[0]][1])#这个写的不好,最好[id,node]这样存进去,一起pop.或者建立继承一个类.
    return tree_clone              

def ast_to_graphviz(tree,filename):
    import os
    tree.to_graphviz(filename=filename, shape='box')
    #check_gv(filename)

    if os.system('dot -Tpng {0} -o {1} -Gdpi=150 '.format(filename,filename+'.png')) ==0:
        print('---created ast_picture---')
    else : print('failure')

    #pricture = filename+'.png'
    #os.startfile(pricture)
    return True


if __name__ == '__main__':
    with open('python-code.txt','r') as f:
        code = f.read()
    origin_ast = ast.parse(code)
    tree_clone = ast_clone(origin_ast)
    ast_to_graphviz(tree_clone,r'.\ast_pictures\python.gv')
