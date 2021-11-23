<?php

require __DIR__ . '/vendor/autoload.php';
use GuzzleHttp\Client;
use GuzzleHttp\TransferStats;

$client = new Client(['base_uri' => 'http://34.80.110.80', 'headers' => [ 'Content-Type' => 'application/json' ]]);
// echo var_dump($client)
$mybody['account'] = 'tl-lisa';
$mybody['password'] = '12345678';
// $response = $client->post( '/api/v2/identity/auth/login', ['body'=>$mybody]);
$res = $client->request('POST', '/api/v2/identity/auth/login', ['json'=>$mybody,
    'debug'  =>  true
]);

echo "\n". "*****************"."\n";
$body = $res->getBody();
$status = $res->getStatusCode();
// echo $res->getReasonPhrase();
$x = json_decode( $res->getBody());
var_dump($x);
echo $x->Message;
echo $x->data->token;
echo $x->data->nonce;
echo "\n". "*****************"."\n";




$retText = <<<EOF
[1]
msgid=#000000333
statuscode=0
[2]
msgid=#000000334
statuscode=1
AccountPoint=92
EOF;


function parse_sms_return($retText){

    $ret_list = explode("\n", $retText);   
    $sms_status= array();
    $key = '';

    foreach($ret_list as $val){
        if (preg_match("/^\[\d?\]$/" , $val)){
            $key = $val;
            $sms_status[$key] = array();
        } elseif (strpos($val, 'AccountPoint')===0){
            $row =  explode("=", $val);
            $sms_status[$row[0]] = $row[1];
        } else {
            $row =  explode("=", $val);
            $sms_status[$key][$row[0]]= $row[1];
        }
    }
    return $sms_status;
}

$result = parse_sms_return($retText);
print_r($result);

// echo $body->('Status');

// $request = $client->createRequest('GET', 'http://34.80.110.80');
// echo $client->getUrl();
// echo $client->getScheme();
class mitakeSms{


    public function __construct($username, $password){
        $this->base_uri = 'http://34.80.110.80';
        $this->header = [ 'Content-Type' => 'x-www-form-urlencoded"' ];
        $this->username = $username;
        $this->password = $password;
        $this->client = new Client(['base_uri' =>  $this->base_uri, 'headers' => $this->header]);
    }

    public function smsSend($dstaddr, $destname, $divtime, $vldtime, $smbody, $response, $clientid, $objectID){
        $api =$this->base_uri.'/b2c/mtk/SmSend?CharsetURL=UTF-8';

        if (preg_match("/^(09|9)[0-9]{8}$/" , '0927844755')){
            print('ok');
        }
        else{
            throw("inValid mobile number");
        }


        $body = array(
            'username' => $this->username,
            'password' => $this->password,
            'dstaddr' => $this->dstaddr,
            'destname' => $this->destname,
            'divtime' => 'abc',
            'vldtime' => '',
            'smbody' => '',
            'response' =>'',
            'clientid' => '',
            'objectID' => ''
        );


        // $res = $this->client->request('POST', '/api/v2/identity/auth/login', ['form_params'=>$body]);
        print_r($body);


    }


}

?>