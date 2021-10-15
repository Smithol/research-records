---
author: liji
date: 2021-10-15 11:38:56
description: 
---



# python代码建立AST树及可视化

## 测试代码

```python
class BootyBayBodyguard(MinionCard):
    def __init__(self):
        super().__init__("Booty Bay Bodyguard", 5, CHARACTER_CLASS.ALL, CARD_RARITY.COMMON)
    def create_minion(self, player):
        return Minion(5, 4, taunt=True)
```

## 方法一

 使用`pythonAst.py`,测试在文件中的`main`部分.测试结果在`ast_pictures`

## 方法二

使用`tree-sitter`,见`tree-sitter-use`文件夹.

参考文献: [Tree-sitter｜Introduction](https://tree-sitter.github.io/tree-sitter/#language-bindings).

