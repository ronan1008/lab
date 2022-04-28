<?php
class Person {
    public $name, $address, $age;

    function __construct($name, $address, $age) {
        $this->name = $name;
        $this->address = $address;
        $this->age = $age;
    }
}

class Employee extends Person {
    public $position, $salary;

    function __construct($name, $address, $age, $position, $salary) {
        parent::__construct($name, $address, $age);
        $this->position = $position;
        $this->salary = $salary;
    }
}

$me = new Employee("shock", 'taipei', 32, 'country', 39999);
$name = $me->name;
$salary = $me->salary;
echo $name."\n";
echo $salary."\n";