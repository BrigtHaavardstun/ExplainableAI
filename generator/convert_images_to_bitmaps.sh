cd generated
for f in *.png; do
    python3 ../image_to_bitmap.py $f
done