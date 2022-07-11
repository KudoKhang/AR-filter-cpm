# AR Filter based-on PRNet

➡️ *Try it in Google Colab [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1F1yCr-JPaTXQNSUQt9gnkIRJlvdQkea3?usp=sharing)*

-------------

```
git clone https://github.com/KudoKhang/AR-filter-cpm
cd AR-filter-cpm
sh ./build.sh
python main.py --input "tests/JianzhuGuo.jpg" --style "tests/uv_face_sticker.png"
```
IN THRER:

--input: A person image
 
<p align="center">
    <img src="tests/JianzhuGuo.jpg">
</p>

--style: A square mask

<p align="center">
    <img src="tests/uv_face_sticker.png" height="256" width="256">
</p>
Result:
<p align="center">
    <img src="output/JianzhuGuo.png">
</p>

Guide: Create mask based-on face UV_texture of PRNet (using https://pixlr.com or photoshop)

<p align="center">
    <img src="tests/uv_face_PRNet.png" height="256" width="256">
</p>

# Todo-list:

- [ ] Gradio -> Hugging Face
- [ ] ONNX
- [ ] Set opacity