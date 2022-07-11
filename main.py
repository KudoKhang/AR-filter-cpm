import argparse
from modules.addSticker import AddSticker

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="tests/persons.jpg", help="Path to input image")
    parser.add_argument("--style", type=str, default="tests/uv_face_sticker.png", help="Path to square sticker in Face Texture")
    parser.add_argument("--savedir", type=str, default="output/")
    args = parser.parse_args()
    print("           ⊱ ──────ஓ๑♡๑ஓ ────── ⊰")
    print("🎵 hhey, arguments are here if you need to check 🎵")
    for arg in vars(args):
        print("{:>15}: {:>30}".format(str(arg), str(getattr(args, arg))))
    print()
    return args

if __name__ == "__main__":
    args = get_args()
    add_sticker = AddSticker()
    output = add_sticker.run(args.input, args.style, savedir=args.savedir)