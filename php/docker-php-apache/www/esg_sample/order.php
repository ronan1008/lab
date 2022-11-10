<?php
	// ===============================================================================
	/* 
	 * Note:
	 * ESG PHP Order Sample Code
	 * 
	 */
	// ===============================================================================
	include( "Common.php" );

	$trans = new Trans( null );
		
	// 交易訊息代碼
	$trans->nodes["MSG_TYPE"] = "0100"; 
	// 交易處理代碼 
	$trans->nodes["PCODE"] = "300000"; // 一般交易請使用 300000
	// 商家遊戲代碼
	$trans->nodes["CID"] = "C000150000015";
	// 商家訂單編號
	$trans->nodes["COID"] = "CP" . date("YmdHis");
	// 幣別 ISO Alpha Code
	$trans->nodes["CUID"] = "VND";
	// 付款代收業者代碼 
	$trans->nodes["PAID"] = "";
	// 交易金額
	$trans->nodes["AMOUNT"] = "10000.00";
	// 商家接收交易結果網址
	$trans->nodes["RETURN_URL"] = "http://xxx.xxx.xxx.xxx/Return_URL.php";
	// 是否指定付款代收業者
	$trans->nodes["ORDER_TYPE"] = "E"; // 請固定填 E 
	// 商家代碼
	$trans->nodes["MID"] = "M3000015";
	// 商家商品名稱
	$trans->nodes["PRODUCT_NAME"] = "Lễ bao 10K";
	// 商家商品代碼
	$trans->nodes["PRODUCT_ID"] = "vn.esgame.lh3d_e_lb_00010";
	// 玩家帳號
	$trans->nodes["USER_ACCTID"] = "40";
	// 交易備註 ( 此為選填 )
	$trans->nodes["MEMO"] = "";
	// 交易備註 ( 此為選填 )
	$trans->nodes["ESG_INFO"] = "TEST_INfO";
	// 以商家密碼、商家密鑰 I , II ( 已於 Common.php 內設定 ) 取得 ERQC
	$erqc = $trans->GetERQC( $p, $k, $v );
	// 商家交易驗證壓碼
	$trans->nodes["ERQC"] = $erqc;
	// 商家交易驗證壓碼 (USER_ACCTID)
	$erqcII = $trans->GetERQCII( $p, $k, $v );
	// 商家交易驗證壓碼II
	$trans->nodes["ERQCII"] = $erqcII;
	
	// 取得送出之交易資料
	$data = $trans->GetSendData();
	echo $data
	
?>

<html> 
<head> 
<title>ESG Transaction Sample Code</title> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
	Test ESG transaction start <br>
	
	COID : <?php echo $trans->nodes["COID"]; ?>
	
	<form name="form1" id="form1" action="https://pay.esgame.vn/purchase/3rd/generate-purchase" method="post" target="_blank">
	<input type="hidden" name="data" value="<?php echo $data ?>">
	<input type="submit" value="送出交易至ESG測試機">
	</form>
	
</body>
</html>