实现了奇校验, 偶校验, CRC循环冗余校验和海明校验。
由于本人水平有限, 已尽最大努力完成。

------------------------------------------------------------
增加了GUI图形界面 (很简陋)

------------------------------------------------------------
在CRC.py文件中，发现生成并计算100个数据过慢，所以使用了pytorch(张量类型)进行计算(CRC_GPU.py)。

------------------------------------------------------------
文件名中包含(Data)字样, 是对GUI页面的进一步完善, 用户可由在GUI页面输入数据。

************************************************************

Odd check, even check, CRC cyclic redundancy check and Hemming check are implemented.
Due to my limited level, I have done my best to complete it.

------------------------------------------------------------
Added GUI (very ugly)

------------------------------------------------------------
In the CRC.py file, it was found that it was too slow to generate and calculate 100 pieces of data, so I used pytorch (tensor type) to calculate (CRC_GPU.py).

------------------------------------------------------------
The inclusion of the word "(Data)" in the file name is a further refinement of the GUI page, which allows users to enter data from the GUI page.
