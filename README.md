实现了奇校验, 偶校验, CRC循环冗余校验和海明校验。
由于本人水平有限, 已尽最大努力完成。

------------------------------------------------------------
增加了GUI图形界面 (很简陋)

------------------------------------------------------------
在CRC.py文件中，发现生成并计算100个数据过慢，所以使用了pytorch(张量类型)进行计算(CRC_GPU.py)。

************************************************************

Odd check, even check, CRC cyclic redundancy check and Hemming check are implemented.
Due to my limited level, I have done my best to complete it.

------------------------------------------------------------
Added GUI (very ugly)

------------------------------------------------------------
In the CRC.py file, it was found that it was too slow to generate and calculate 100 pieces of data, so I used pytorch (tensor type) to calculate (CRC_GPU.py).
