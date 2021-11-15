<?php

require __DIR__ . '/vendor/autoload.php';
use GuzzleHttp\Client;

$client = new Client(['base_uri' => 'http://34.80.110.80', 'headers' => [ 'Content-Type' => 'application/json' ]]);
// echo var_dump($client)
$mybody['account'] = 'tl-lisa';
$mybody['password'] = '12345678';
print_r($mybody);
// $response = $client->post( '/api/v2/identity/auth/login', ['body'=>$mybody]);
$res = $client->request('POST', '/api/v2/identity/auth/login', ['json'=>$mybody]);

$body = $res->getBody();
$status = $res->getStatusCode();
echo $res->getReasonPhrase();

// print $status;
// print_r($body);
$x = json_decode( $res->getBody());
// print($x->nonce);
var_dump($x);
echo $x->Message;
echo $x->data->token;
echo $x->data->nonce;


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