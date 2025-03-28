set -e

for file in tests/*.py
do
    echo "Executing $file"
    python $file
    sleep 1
done