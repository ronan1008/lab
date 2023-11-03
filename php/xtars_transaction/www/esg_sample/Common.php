<?php
  // ===============================================================================
	/* 
	 * Note:
	 * 解析回傳資料
	 * 
	 */
	// ===============================================================================
	include( "Cryptography7.php" );

	// 商家密碼
	$p = "n4c8He2juc";
	// 商家密鑰 I
	$k = "VHgt3qFfql5ctDKe2mQuCpYg1ukWZ2Bk";
	// 商家密鑰 II
	$v = "R0ZvZXVSRUw=";
	
	// 交易物件
	class Trans
	{
		private $key = ""; // key for content provider 
		private $iv = ""; // iv for content provider 
		private $odata = ""; // Recv From CP Module 
		private $data = ""; // Json String
		private $bolIsParsed = false; // parse flag
		public $msg = ""; 
		public $recvDesc = ""; 
		public $nodes = null; 
		public $base64_encrypt_data = ""; 
		public $encrypt_data = ""; 

		/**
		* 建構式
		*
		* @param string $odata
		*/
		function __construct ($odata)
		{
			if (empty($odata)) {
			
				$this->bolIsParsed = true;
				$this->nodes = array();
				
			}else{
				$this->odata = $odata;
				$this->data = base64_decode( $this->odata );
				
				$json_data = json_decode($this->data,true);
				$this->bolIsParsed = $this->IsParsedByJson($json_data);
				
				if ( !$this->bolIsParsed ) {
					$this->msg = "trans data format is not valid";
					return;
				}
				//Json to Nodes
				$this->nodes = array();
				$this->PutNodes($json_data);
			}
		}
		
		private function IsParsedByJson($json_data){
			$ret = true;
			if(!array_key_exists("MSG_TYPE",$json_data)){
				$ret = false;
			}
			return $ret;
		}
		
		// 解析 Json 資料
		private function PutNodes($json_data)
		{
			foreach($json_data as $key => $value){
				$this->nodes[ $key ] = $value;
			}
		}
		
		// 建構送出之交易、查詢、請款資料
		public function GenerateJson()
		{
			$return_data = Array();
			if ( count( $this->nodes ) > 0 ){
				foreach ( $this->nodes as $key => $value ) 
				{
					$return_data[$key] = $value;
				}
			}			
			$json_data = json_encode($return_data);
			return $json_data;
		}
		
		// 建構送出之交易、查詢、請款資料
		public function GetSendData()
		{
			return base64_encode($this->GenerateJson());
		}

		/**
		* 產生商家交易驗證壓碼
		* 
		* @param string $pwd
		* @param string $key
		* @param string $iv
		*/
		public function GetERQC( $pwd = "xxx", $key = "xxx", $iv = "xxx" )
		{
			if ( !$this->bolIsParsed ) {
			
				$this->msg = "trans data format is not valid";
				return false;

			}else if (empty($key) || empty($iv)) {
			
				$this->msg = "key and iv is not valid";
				return false;
			}
			
			$this->key = $key;
			$this->iv = $iv;
			
      $cid = "";
      $coid = "";
      $cuid = "";
      $amt = "";

			// vdata = cid + coid + cuid + amt(12,2) + pwd
			
			// Get Content ID
			$cid = $this->nodes["CID"];

			// Get Content Ordere ID
			$coid = $this->nodes["COID"];

			// Get Trans Currency ID
			$cuid = $this->nodes["CUID"];

			// Get Trans Amount need parse to fix format
			$amt = $this->nodes["AMOUNT"];

      return $this->_GetERQC($cid, $coid, $cuid, $amt, $pwd);
    }

		/**
		* 產生商家交易驗證壓碼
		* 
		* @param string $cid
		* @param string $coid
		* @param string $cuid
		* @param string $amt
		* @param string $pwd
		*/
    private function _GetERQC($cid, $coid, $cuid, $amt, $pwd)
    {
			$erqc = "";
      $encrypt_data = "%s%s%s%s%s";
      
      // 驗證用的 AMOUNT 需整理成 14 碼
      if (strpos($amt, ".") !== false)
      {
      	$amt = substr($amt, 0, strpos($amt, ".")) . ((strlen($amt) - strpos($amt, ".")) > 3 ? substr($amt, strpos($amt, ".") + 1, 2) : str_pad(substr($amt, (strpos($amt, ".") + 1)), 2, "0"));
      	$amt = str_pad($amt, 14, "0", STR_PAD_LEFT);
      } else {
      	$amt = str_pad($amt, 12, "0", STR_PAD_LEFT) . "00"; //.PadLeft(14, '0');
      }

			//$amt = "00000000005000";
			$this->encrypt_data = sprintf($encrypt_data, $cid, $coid, $cuid, $amt, $pwd);
			$des = new Crypt3Des($this->key,$this->iv);
			$this->base64_encrypt_data = $des->encrypt( $this->encrypt_data );
			$erqc = base64_encode( sha1( $this->base64_encrypt_data, true ) );
			return $erqc;
    }
		
		// 檢核商家交易驗證壓碼
    public function VerifyERQC($pwd = "xxx", $key = "xxx", $iv = "xxx")
    {
			if ( $pwd == "xxx" || $key == "xxx" || $iv == "xxx" ) return false;
			
			$cp_data = $this->GetERQC($pwd, $key, $iv);
			$esg_data = $this->nodes["ERQC"];
			
			return ($esg_data != "" && $cp_data != "" && $esg_data == $cp_data);
    }
		
				/**
		* 產生商家交易驗證壓碼
		* 
		* @param string $pwd
		* @param string $key
		* @param string $iv
		*/
		public function GetERQCII( $pwd = "xxx", $key = "xxx", $iv = "xxx" )
		{
			if ( !$this->bolIsParsed ) {
				
				$this->msg = "trans data format is not valid";
				return false;
				
			}else if (empty($key) || empty($iv)) {
				
				$this->msg = "key and iv is not valid";
				return false;
			}
			
			$this->key = $key;
			$this->iv = $iv;
			
			$cid = "";
			$coid = "";
			$cuid = "";
			$amt = "";
			$user_acc_id = "";
			
			// Get Content ID
			$cid = $this->nodes["CID"];
			
			// Get Content Ordere ID
			$coid = $this->nodes["COID"];
			
			// Get Trans Currency ID
			$cuid = $this->nodes["CUID"];
			
			// Get Trans Amount need parse to fix format
			$amt = $this->nodes["AMOUNT"];
			
			// Get Content USER_ACCIDt
			$user_acctid = $this->nodes["USER_ACCTID"];
			
			return $this->_GetERQCII($cid, $coid, $cuid, $amt, $user_acctid, $pwd);
		}
    
		/**
		* 產生商家交易驗證壓碼
		* 
		* @param string $cid
		* @param string $coid
		* @param string $cuid
		* @param string $amt
		* @param string $user_acctid
		* @param string $pwd
		*/
		private function _GetERQCII($cid, $coid, $cuid, $amt, $user_acctid, $pwd)
		{
			$erqcII = "";
			
			$encrypt_data = "%s%s%s%s%s%s";
			
			// 驗證用的 AMOUNT 需整理成 14 碼
			if (strpos($amt, ".") !== false)
			{
				$amt = substr($amt, 0, strpos($amt, ".")) . ((strlen($amt) - strpos($amt, ".")) > 3 ? substr($amt, strpos($amt, ".") + 1, 2) : str_pad(substr($amt, (strpos($amt, ".") + 1)), 2, "0"));
				$amt = str_pad($amt, 14, "0", STR_PAD_LEFT);
			}
			else
			{
				$amt = str_pad($amt, 12, "0", STR_PAD_LEFT) . "00"; //.PadLeft(14, '0');
			}
			
			$this->encrypt_data = sprintf($encrypt_data, $cid, $coid, $cuid, $amt, $user_acctid, $pwd);
			
			$des = new Crypt3Des($this->key,$this->iv);
			$this->base64_encrypt_data = $des->encrypt( $this->encrypt_data );
			$erqcII = base64_encode( sha1( $this->base64_encrypt_data, true ) );
			
			return $erqcII;
		}
		
		/**
		* 產生ESG交易驗證壓碼
		* 
		* @param string $key
		* @param string $iv
		*/
    public function GetERPC( $key = "xxx", $iv = "xxx" )
    {
			if ( !$this->bolIsParsed ) {
			
				$this->msg = "trans data format is not valid";
				return false;

			} else if (empty($key) || empty($iv)) {
			
				$this->msg = "key and iv is not valid";
				return false;
			}
			
			$this->key = $key;
			$this->iv = $iv;
			
			$cid = "";
			$coid = "";
			$rrn = "";
			$cuid = "";
			$amt = "";
			$rcode = "";

			// vdata = cid + coid + cuid + amt(12,2) + $rcode
			
			// Get Content ID
			$cid = $this->nodes["CID"];

			// Get Content Ordere ID
			$coid = $this->nodes["COID"];

			// Get ESG Ordere ID
			$rrn = $this->nodes["RRN"];

			// Get Trans Currency ID
			$cuid = $this->nodes["CUID"];

			// Get Trans Amount need parse to fix format
			$amt = $this->nodes["AMOUNT"];

			// Get Trans Amount need parse to fix format
			$rcode = $this->nodes["RCODE"];
			
			return $this->_GetERPC($cid, $coid, $rrn, $cuid, $amt, $rcode);
    }

		/**
		* 產生ESG交易驗證壓碼
		* 
		* @param string $cid
		* @param string $coid
		* @param string $rrn
		* @param string $cuid
		* @param string $amt
		* @param string $rcode
		*/
		private function _GetERPC($cid, $coid, $rrn, $cuid, $amt, $rcode)
		{
			$erpc = "";
			
			$encrypt_data = "%s%s%s%s%s%s";
			
			// 驗證用的 AMOUNT 需整理成 14 碼
			if (strpos($amt, ".") !== false)
			{
				$amt = substr($amt, 0, strpos($amt, ".")) . ((strlen($amt) - strpos($amt, ".")) > 3 ? substr($amt, strpos($amt, ".") + 1, 2) : str_pad(substr($amt, (strpos($amt, ".") + 1)), 2, "0"));
				$amt = str_pad($amt, 14, "0", STR_PAD_LEFT);
			} else {
				$amt = str_pad($amt, 12, "0", STR_PAD_LEFT) . "00"; //.PadLeft(14, '0');
			}

			//$amt = "00000000005000";
			$this->encrypt_data = sprintf($encrypt_data, $cid, $coid, $rrn, $cuid, $amt, $rcode);
			echo $this->encrypt_data . PHP_EOL;

			$des = new Crypt3Des($this->key,$this->iv);
			
			$this->base64_encrypt_data = $des->encrypt( $this->encrypt_data );
			$erpc = base64_encode( sha1( $this->base64_encrypt_data, true ) );
			echo $erpc . PHP_EOL;
      return $erpc;
    }
		
		// 檢核ESG交易驗證壓碼
		public function VerifyERPC($key = "xxx", $iv = "xxx")
		{
			if ( $key == "xxx" || $iv == "xxx" ) return false;
			
			$cp_data = $this->GetERPC($key, $iv);
			$esg_data = $this->nodes["ERPC"];		
			
			return ($esg_data != "" && $cp_data != "" && $esg_data == $cp_data);			
		}
		
	}
	
?>