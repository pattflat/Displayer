<html>
    <head>
    		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
			<script src="http://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.2/modernizr.js"></script>
        	<title>Web Agent Display Propriodirect</title>
    </head>

    <body>
    <div class="se-pre-con"></div>
	 <link href="style.css" type="text/css" rel="stylesheet" />

	<?php
		header("content-type: text/html; charset=UTF-8");  
		include 'ChromePhp.php';
		
		$param = $_GET["next"];
		if($param == null)
			$param = 0;
		//ChromePhp::log($param);

		$db = new SQLite3('WEBAgent.db');
		
		
		$checkcount = 'SELECT count(*) as count FROM agentview';
		$count = $db->querySingle($checkcount);
		//ChromePhp::log("select count = " . $count);
		
		//echo printf("%s",$results);
		
		$agentquery = 'SELECT * FROM agentview LIMIT 1 OFFSET ' . $param;
		//ChromePhp::log('agent query = ' . $agentquery);
		$results = $db->query($agentquery);
		//ChromePhp::log($count);
		ChromePhp::log($param + 1);
		if($param + 1 == $count)
			$param = 0;
		else
			$param += 1; 
		$row = $results->fetchArray();
		$elements = explode("|", $row['phone']);
		$phone_img = "<div class='image'><img src=".$row['imgphone']."></div>";
		echo '<table>';
		echo "<tr>";
		echo "<td><img class='agentimg' src=" . $row['img'] . "></td>";
		echo "<td>";
		echo "<table>";
		echo "<tr><td><table class='pretty'><tr><td>". $phone_img. "</td><td>" . $elements[0] . "</td></tr></table></td></tr>";
		echo "<tr><td><table class='pretty'><tr><td>". $phone_img. "</td><td>" . $elements[1] ."</td></tr></table></td></tr>";
		echo "<tr><td><table class='pretty'><tr><td>". $phone_img. "</td><td>" . $elements[2] ."</td></tr></table></td></tr>";
		echo "</table>";
		echo '</td>';
		$logo = "<img class='newsize' src=logo_proprio_fr.png>";
		echo '<td>' . $logo . '</td>';
		echo "</tr>";
		echo '</table>';
		echo '<br/>';
		echo '<br/>';
		echo '<br/>';
		$stmt = 'SELECT * FROM ' .$row['name']. ' LIMIT 6 OFFSET '. $row['last_display'];
		$current_name = $row['name'];
		$total_count = $row['count'];
		$current_display_position = $row['last_display'];

		$results = $db->query($stmt);
		
		echo '<table cellspacing="15" id="score">';

		$count = 0;
		while ($row = $results->fetchArray()) 
		{
			if($count==2)
			{	
			echo '<br>';
			echo '<br>';
				echo '</tr>';
				$count = 0;
			}
			if($count==0)
         {
         	echo "<tr>";
         }
         echo "<td>";
			echo '<div class="image">';
			echo '<img src="'.$row['img'].'">';
			echo '<h2><span>'.$row['address'] . "<span class='spacer'></span>";
			echo "<br/><span class='spacer'></span>" . $row['city'] . " " . $row['price'].' $</span></h2>';
			echo '</div>';
			$count++;
         print "</td>";

		}
		if($count>0)
      {
      	print "</tr>";
		}
		echo '</table>';
		$current_display_position +=6;
		if($current_display_position > $total_count)
		 $current_display_position = 0;
		$stmt = "";
		$stmt = <<<EOD
		UPDATE agentview SET last_display='$current_display_position' WHERE name='$current_name'
EOD;
		$db->exec($stmt);		
		$db->close();
		#echo sprintf("Inscription : %s / %s",$current_display_position,$total_count)

	?>
		
    	
		
		<script>
		
		setTimeout(function()
    	{
		//return;
    		var url = window.location.href;
    		var val = "?next=";
    		val +=  <?php echo json_encode($param) ?>;
    		url = url.replace( /[\?#].*|$/, val ); 
    		window.location.href = url;
   		document.location.assign(url);
		}, 8000);
		
		
		//paste this code under head tag or in a seperate js file.
		// Wait for window load
		$(window).load(function() {
			// Animate loader off screen
			$(".se-pre-con").fadeOut("slow");;
		});
		
    </script>

    </body>
</html>
