<?php
	set_time_limit(0);
	$db =mysql_connect("127.0.0.1", "root","6a5a4a");
	$conn = mysql_select_db("gmarket",$db);
	date_default_timezone_set('Asia/Taipei');
	mysql_query("set character_set_results='utf8'");
	mysql_query("set character_set_client='utf8'");
	mysql_query("set names utf8");

?>
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="style.css">
<script type="text/javascript">
	function checkForm(){
				if(document.myform.start_date.value > document.myform.end_date.value ){
					alert("Start Date must not be later then end date!!");
					return false;
				}
				return true;
			}
</script>
</head>
<body>
<form name = 'myform' method = "POST">

<table cellspacing="10">
<tr>
<th>Category Type</th><th> Start Date</th><th> End Date</th> 
</tr>
<tr>
<td>
<select name = 'categ'>
<?php	$sql = "select * from categ order by id";
	$result = mysql_query($sql) or die  ("GG".mysql_error());
	while($row = mysql_fetch_assoc($result)){
		echo "<option value = '".$row['id']."'> ".$row['id']." ".$row['categ_name']."</option>";
	}
?>
</select>
</td><td>
<select name = 'start_date'>
<?php	$sql = "select * from date_list";
	$result = mysql_query($sql) or die ("GG".mysql_error());
	while($row = mysql_fetch_assoc($result)){
		echo "<option value = '".$row['record_time']."'>".$row['record_time']."</option>";
	}
?>
</select>
</td>
<td>
<select name = 'end_date'>
<?php	$sql = "select * from date_list";
	$result = mysql_query($sql) or die ("GG".mysql_error());
	while($row = mysql_fetch_assoc($result)){
		echo "<option value = '".$row['record_time']."'>".$row['record_time']."</option>";
	}
?>
</select>
</td>

<td>
<input type="submit" onclick="return checkForm()"></input>
</td>
</tr>

</table>



</form>


<?php	
	if(isset($_POST["categ"])){
		$start_date = $_POST['start_date'];
		$end_date = $_POST['end_date'];
		//echo $_POST['categ']." ".$start_date." ".$end_date;
		$query=  "./gen_model.py tt.out {$_POST['categ']} {$start_date} {$end_date}";
		//$out = shell_exec("./gen_model.py tt.out $_POST['categ'] $start_date $end_date");
		echo "Generating Models";
		$out = shell_exec($query);
		if($out==""){
			echo "Sucessfully Generate Model <br />";
			$query2 = "./test2.sh";
			echo "Start SOM Training <br />";
			echo $query2;
			$out = shell_exec($query2);
			if($out ==""){
				echo "Successfully Trained SOM";

			}
		}else 
			echo $out."<br />";
	
	}
		#$date_str = date('Y-m-d');

	
	mysql_close($db);
?>


</body>
</html>
