# re

**Zero-width match**

表示某个条件成立的那个位置，但是没有提取字符

`^`, `$`, `\b`, `(?=...)`, `(?!=...)`



**re.finditer()**会返回一个迭代器，每一个结果是一个`re.Match`对象

```py
import re

pattern = r'\d+'  # 匹配一个或多个数字
s = "abc123def456ghi789"

matches = re.finditer(pattern, s)
for match in matches:
    print(match)         # Match对象
    print(match.group()) # 匹配到的字符串
    print(match.start()) # 匹配开始位置
    print(match.end())   
```

```bash
<re.Match object; span=(3, 6), match='123'>
123
3
6
<re.Match object; span=(9, 12), match='456'>
456
9
12
<re.Match object; span=(15, 18), match='789'>
789
15
18
```

```py
import re
s = "hi! bye."
# 下面的正则在每个单词边界零宽匹配
matches = list(re.finditer(r'\b', s))
for m in matches:
    print(m.start(), m.group())
```

```bash
0 
2 
4 
7 
```

- **普通匹配**：`start()` 是匹配到的子串的第一个字符的下标。
- **零宽度匹配**：`start()` 返回的是“匹配发生的位置”，可以理解为“字符之间的间隔下标”，也就是“切片分隔点”。



**re.split()**

如果开头被匹配，则第一个`re.match`是`''`，末尾被匹配则最后一个`re.match`是`''`

零间隔返回的`re.match`对象的坐标是间隔的坐标。

**优先匹配能消耗掉字符的分隔符，对于不能消耗任何字符的地方，也会把这些位置当作分割点。**

![](1.png)

得到的结果

![](2.png)

第一个匹配到`...`，之后对`words...`进行匹配，匹配到`''`，之后对没有开头的`words...`匹配，匹配到`w` `o`之间的空隙... 结果为

```bash
['', '', 'w', 'o', 'r', 'd', 's', '', '']
```

```py
re.split(r'(\W*)', '...words...')
['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
```

