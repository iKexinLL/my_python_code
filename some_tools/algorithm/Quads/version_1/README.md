
2016年3月31日10:51:17
根据pic中的两张图对比, 我发现这个树多了一层 <br/>
也就是说, 在quadtree4_final_tree.png中的蓝点和黄点之间多了一层蓝点,<br/>
导致无法直接计算当前rect中的weight集合<br/>
从quadtree4_final_tree_form.png的左下角可以对比出来<br/>
在tree.png中应该是一个蓝点+三个黄点<br/>
而不是一个蓝点+三个蓝点+三个黄点<br/>
