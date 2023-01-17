cd data/images
echo "Removing images..."
rm *.png
cd ../labels
echo "Removing labels..."
rm *.txt
cd ../training_data
echo "Removing training data..."
rm *.bmp
echo "Done!"