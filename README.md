# AR-filter-cpm

```
pip install gdown
cd AR-filter-cpm
gdown --id 1UoE-XuW1SDLUjZmJPkIZ1MLxvQFgmTFH -O PRNet/net-data
python main.py --input "tests/input.jpg" --style "tests/fillter256.png"
```
IN THRER:

--input: A straight face have size 256 * 256
<p align="center">
    <img src="tests/input.jpg">
</p>

--style: A square mask

<p align="center">
    <img src="tests/fillter256.png">
</p>
Result:
<p align="center">
    <img src="result.png">
</p>

Note: Create mask based-on face UV_texture (using https://pixlr.com or photoshop)

<p align="center">
    <img src="tests/faceFeminine.jpg">
</p>