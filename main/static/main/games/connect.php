<?PHP
// error_reporting(E_ALL);
// ini_set('display_errors', '1');

$username = "Vladimir";
$password = "6UhZG3g2x5MQmZytFWfTLU1OWRQI3";

$ip = 'http://185.130.47.75:8080';

$url = '0';

if ($_GET['mode'] == "roulette") {
	if ( strlen($_GET['token']) < 40 || ($_GET['action'] != "init" && $_GET['action'] != "spin")){
		http_response_code(403);
		die('Forbidden !conditions');
	}
	$url = $ip.'/roulette?action='.$_GET['action'].'&token='.$_GET['token'];
	if ($_GET['action'] == 'spin'){
		$url .= '&request='.$_GET['request'];
	}
} // connect.php?mode=roulette&action=spin&token=<token>&request=<base64>

if ($_GET['mode'] == "blackjack" || $_GET['mode'] == "blackjack_exposure"){
	if ($_SERVER['REQUEST_METHOD'] != "POST") {
		http_response_code(403);
		die('Forbidden !post');
	} 

    $text = file_get_contents('php://input');

    $json = json_decode($text, false);
    if ($json === null || empty($json->action) || strlen($json->token) < 45 || ($json->game != "blackjack" && $json->game != "blackjack_exposure")){
		http_response_code(403);
		die('json error: '.$text);
    }

	$url = $ip.'/blackJack?action='.$json->action.'&token='.$json->token.'&all='.base64_encode($text).'&game='.$json->game;
	// switch ($json->action){
	// 	case "init":
	// 		$url .= '&game='.$json->game;//.'&chipCount='.$json->chipCount.'&chipPrice='.$json->chipPrice.'&placeCount='.$json->placeCount;
	// 	    break;
		// case "deal":
		// 	if (count($json->coins) < 1) {
		// 		http_response_code(403);
		// 		die('coins < 1');
		// 	} 
		// 	foreach ($json->coins  as &$coin) {
		// 		$url .= '&coins='.$coin;
		// 	}
		// 	break;
		// default:
		// 	http_response_code(403);
		// 	die('Forbidden action not тcorrect');
	// }
} else {
	if (empty($_GET['token'])){
		http_response_code(403);
		die('Forbidden !token');
	}
}
// ОБРАБОТКА СЛОТЫ
switch ($_GET['mode']) {
	case "slotsinit":
		$url = $ip.'/slotsInit?game='.$_GET['game'].'&token='.$_GET['token'];
		break;
	case "spinreq":
		if ( empty($_GET['bet']) || empty($_GET['lines']) ){
			http_response_code(403);
			die('Forbidden !bet&lines');
		}
		$url = $ip.'/spinRequest?token='.$_GET['token'].'&bet='.$_GET['bet'].'&lines='.$_GET['lines'];
		break;
	case "take":
		$url = $ip.'/takeRequest?token='.$_GET['token'];
		break;
	case "double":
		$url = $ip.'/doubleRequest?token='.$_GET['token'];
		break;
	case "bonus":
		$url = $ip.'/bonusGame?token='.$_GET['token'].'&collect='.$_GET['collect'];
		break;
}

if ($url != "0"){
	$opts = array(
		'http'=>array(
			'method'=>"GET",
			'header' => "Authorization: Basic " . base64_encode("$username:$password")                 
		)
	);
	$context = stream_context_create($opts);
	
	$file = file_get_contents($url, false, $context);
	if (empty($file)){
		http_response_code(403);
		die('Forbidden empty ans');
	}else {
		print($file);
		die();
	}
} 
http_response_code(403);
die("mode not selected");

?>