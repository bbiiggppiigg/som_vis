FILES="in/*"
for f in $FILES
do
	./gen_graph.sh < $f
done
