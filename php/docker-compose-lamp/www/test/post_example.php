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
$x = json_decode( $res->getBody());
// var_dump($x);
echo $x->Message."\n";
echo $x->data->token."\n";
echo $x->data->nonce."\n";

// $url = $res->getBody()->getContents();
// print($client->getUri())
?>