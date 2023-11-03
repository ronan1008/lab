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
	$trans->nodes["COID"] = "es2211145gkBwE6ZVeRk";
	// 幣別 ISO Alpha Code
	$trans->nodes["CUID"] = "VND";
	// 付款代收業者代碼 
	$trans->nodes["PAID"] = "";
	// 交易金額
	$trans->nodes["AMOUNT"] = "100000.0000";
	// 商家接收交易結果網址
	$trans->nodes["RETURN_URL"] = "https://ptsv2.com/t/gpa6a-1668410593/post";
	// 是否指定付款代收業者
	$trans->nodes["ORDER_TYPE"] = "E"; // 請固定填 E 
	// 商家代碼
	$trans->nodes["MID"] = "M3000015";
	// 商家商品名稱
	$trans->nodes["PRODUCT_NAME"] = "Esgame點數 240000";
	// 商家商品代碼
	$trans->nodes["PRODUCT_ID"] = "xtars.web.esgame.points.240000";
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
	$data = "eyJNU0dfVFlQRSI6ICIwMTAwIiwgIlBDT0RFIjogIjMwMDAwMCIsICJDSUQiOiAiQzAwMDE1MDAwMDAxNSIsICJDVUlEIjogIlZORCIsICJQQUlEIjogIiIsICJBTU9VTlQiOiAxMDAwMDAuMCwgIlVTRVJfQUNDVElEIjogIjc3NGFiNzNmLTZhYTYtNGVkMS1hOTkxLTYwOWQ3ZGI3ZDFhMyIsICJSRVRVUk5fVVJMIjogImh0dHBzOi8vcHRzdjIuY29tL3QvZ3BhNmEtMTY2ODQxMDU5My9wb3N0IiwgIk9SREVSX1RZUEUiOiAiRSIsICJNSUQiOiAiTTMwMDAwMTUiLCAiUFJPRFVDVF9OQU1FIjogIkVzZ2FtZVx1OWVkZVx1NjU3OCAyNDAwMDAiLCAiUFJPRFVDVF9JRCI6ICJ4dGFycy53ZWIuZXNnYW1lLnBvaW50cy4yNDAwMDAiLCAiQ09JRCI6ICJlczIyMTExNDVSUE5OVGFUbzNuaiIsICJFUlFDIjogImxLcXFrUzcrNzVvM1dadlRubXRWbXJjVFVBbz0iLCAiRVJRQ0lJIjogIkg0bmJyTjR3dDNOUHNrbTdEMnJJTm1kZTErUT0ifQ==";
	
   
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // collect value of input field
    $name = $_POST['fname'];
        if (empty($name)) {
            echo "Name is empty";
        } else {
            echo $name;
        }
    }
 

    echo $name;
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
	<input type="hidden" name="data" value="<?php echo $name ?>">
	<input type="submit" value="送出交易至ESG測試機">
	</form>
	
</body>
</html>
