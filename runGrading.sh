input_dir=$1;
# output_dir=$2;
assignment_name=$2;

rm log.txt

# python preprocess-add-grade.py $input_dir $output_dir $assignment_name 2>&1 | tee -a log.txt;
python preprocess-upload-notebook.py $input_dir $assignment_name 2>&1 | tee -a log.txt;

for notebook in $input_dir/*.ipynb;
do
    echo "Now executing:" $notebook "🤔" 2>&1 | tee -a log.txt;
    jupyter nbconvert --allow-errors --to notebook --inplace --execute $notebook 2>&1 | tee -a log.txt;
    echo "Notebook:" $notebook "executed 🎉🎊" 2>&1 | tee -a log.txt;
done;

python upload_tests.py $input_dir $assignment_name 2>&1 | tee -a log.txt

echo "All notebooks autograded and executed 🎉🎊" 2>&1 | tee -a log.txt