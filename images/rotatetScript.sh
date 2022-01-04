for d in */; do
    cd $d
    short=${d:0:1}
    for f in $short?.png; do
        echo $f
        rm $f
    done
    python3 ../../generator/generate.py $short    
    cd ".."
done
