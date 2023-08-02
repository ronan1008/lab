<form name="frmTestPay" method="post" action="https://dev.paydibs.com/PPGSG/PymtCheckout.aspx">
	     TxnType
	     <input type="text" name="TxnType" value="PAY">
	     <br/>
	     MerchantID
             <input type="text" name="MerchantID" value="POIYAK">
	     <br/>
	     MerchatPymtID
             <input type="text" name="MerchantPymtID" value="pd2308015dQ5BU7jeQvc">
<br/>
	     MerchantOrdID
             <input type="text" name="MerchantOrdID" value="pd2308015dQ5BU7jeQvc">
<br/>
             MerchantOrdDesc
             <input type="text" name="MerchantOrdDesc" value="Payment for abc">
<br/>
             MerchantTxnAmt
             <input type="text" name="MerchantTxnAmt" value="25.00">
<br/>
             MerchantCurrCode
             <input type="text" name="MerchantCurrCode" value="MYR">
<br/>
             MerchantRURL
             <input type="text" name="MerchantRURL" value="https://testshockleeapi.free.beeceptor.com/my/api/path">
<br/>
             CustIP
             <input type="text" name="CustIP" value="36.227.106.111">
<br/>
             CustName
             <input type="text" name="CustName" value="shock lee">
<br/>
	     CustEmail
             <input type="text" name="CustEmail" value="shock@truelovelive.dev">
<br/>
             CustPhone
             <input type="text" name="CustPhone" value="0937855506">
<br/>
             Sign
             <input type="text" name="Sign" value="3ab615fa85dddee8d96462d8d24557a6eae6fc41dce0e40d7aba410ad0a835e3a7f1da217964bc28e7158cfc2b1fed0051548b048c05bd3968c2103fa8e2c14b">
<br/>
             MerchantCallbackURL
             <input type="text" name="MerchantCallbackURL" value="https://testing-api.xtars.com/api/v3/transaction/paydibs/callback?merchantPymtId=pd2308015dQ5BU7jeQvc">
<br/>
	     PageTimeout
	     <input type="text" name="PageTimeout" value="300">
<br/>
             <input type="submit" value="Pay Now" />
         </form>