<?php


if (preg_match("/^(09|9)[0-9]{8}$/" , '0927844751')){
    print('ok'."\n");
}
else{
    // throw("inValid mobile number");
    print('no'."\n");
}