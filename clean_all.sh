current_dir=$(basename "$PWD")

echo "Checking folder is correct..."
if [ "$current_dir" = "ExplainableAI" ]
then
    echo "Folder correct name. Continuing..."
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
else
    echo "Folder does not have correct name. Aborting..."
fi