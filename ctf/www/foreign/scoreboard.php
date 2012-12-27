<?php
$url = 'http://127.0.0.1:8000/scoreboard';
$ch = curl_init(); 
curl_setopt($ch, CURLOPT_URL, $url);
$out = curl_exec($ch);
?>