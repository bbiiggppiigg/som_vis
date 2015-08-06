read -p "Please Input categ id : " categ_id
read -p "Please Input Start Date yyyy-mm-dd : " start_date
read -p "Please Input End Date yyyy-mm-dd : " end_date
read -p "Please Input Map Size : " map_size
output_dir="out/"
timeseed=$(date +"%s")
stage1=$timeseed"_stage1"
stage2=$timeseed"_stage2"
final_output=$output_dir"categ"$categ_id"_"$start_date"_"$end_date"_"$map_size".csv"
if [ -f $final_output ]
then
	echo "Ouput Generated"
else
echo "Generating Model"
#echo $stage1".out"
./gen_model.py $output_dir$stage1".out" $categ_id $start_date $end_date
echo "Model Generated"
echo "Start Training Model"
scala -classpath encog-core-3.2.0.jar test.jar $output_dir$stage1".out" $output_dir$stage2".out" $map_size
echo "Model Trained"
echo "Generating CSV"
./gen_csv.py  $output_dir$stage2".out" $final_output
echo "CSV Generated"
fi