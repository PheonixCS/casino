<?php 
/*********************************************************/
/**  © 2023 NULLcode Studio. All Rights Reserved.
/**  Разработано в рамках проекта: https://null-code.ru/
/*********************************************************/
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

require_once('SlotLogic.php');

if ($_SERVER['REQUEST_METHOD'] == "POST") {
	ParsePost();
} else {
	SendError("No post data received");
}

function ParsePost()
{
	header("Content-type: text/json");
	$text = file_get_contents('php://input');
	$json = json_decode($text, false);
	
	if ($json === null) {
		SendError("json decode error");
		exit;
	}
	
	$lines = $json->lines;
	$bet = $json->bet;
	$balance = $json->balance;
	$freeSpinCount = $json->freeSpinCount;
	
	if (isset($json->specialSameTime))
		$specialSameTime = $json->specialSameTime;
	else
		$specialSameTime = false;

	if (isset($json->complex))
		$complex = $json->complex;
	else
		$complex = false;

	if (isset($json->wild_ID))
		$wild_ID = $json->wild_ID;
	else
		$wild_ID = -1;

	if (isset($json->limit))
		$limit = $json->limit;
	else
		$limit = -1;

	if (isset($json->complex_get))
		$complex_get = $json->complex_get;
	else
		$complex_get = false;

	if (isset($json->winner))
		$winner = $json->winner;
	else
		$winner = false;

	if (isset($json->ignoreSpecial))
		$ignoreSpecial = $json->ignoreSpecial;
	else
		$ignoreSpecial = null;

	if (isset($json->getSpecial))
		$getSpecial = $json->getSpecial;
	else
		$getSpecial = null;

	if (isset($json->handle))
		$handle = $json->handle;
	else
		$handle = 'Scheme';

	$file = __DIR__ . '/Schemes/' . $handle . '.json';
	if (!file_exists($file)) {
		SendError("there is no file: " . $file);
		exit;
	}
	$json = json_decode(file_get_contents($file));
	if ($json === null) {
		SendError("json decode error");
		exit;
	}
	$logic = new SlotLogic();
	$logic->Calculate(new SlotSchemeData($json), $lines, $bet, $balance, $freeSpinCount, $specialSameTime, $complex, $wild_ID, $limit, $complex_get, $winner, $ignoreSpecial, $getSpecial);
	if ($logic === null) {
		SendError("function Calculate(...) return null");
		exit;
	}
	echo json_encode($logic->result);
}

function SendError($text)
{
	$jsonErr = json_decode('{}', false);
	$jsonErr->error = $text;
	$sendJson=json_encode($jsonErr);
	echo $sendJson;
	exit;
}
?>
