cd FaceBoxes
sudo apt install build-essential
sh ./build_cpu_nms.sh
cd ..

pip install gdown
gdown --id 1UoE-XuW1SDLUjZmJPkIZ1MLxvQFgmTFH -O PRNet/net-data

pip uninstall tensorflow -y --q
pip install -r requirements.txt --q