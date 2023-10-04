$(document).ready(function() {
	$(".block").hide();
	$("#blockMoneyIn").show();

	$("#moneyIn").click(function() {
		$(".block").hide();
		$("#blockMoneyIn").show();
	});

	$("#moneyOut").click(function() {
		$(".block").hide();
		$("#blockMoneyOut").show();
	});

	$("#moneyHistory").click(function() {
		$(".block").hide();
		$("#blockMoneyHistory").show();
	});

});