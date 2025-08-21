<?php

/*

bwapp, or a buggy web application, is a free and open source deliberately insecure web application.
It helps security enthusiasts, developers and students to discover and to prevent web vulnerabilities.
bwapp covers all major known web vulnerabilities, including all risks from the OWASP Top 10 project!
It is for security-testing and educational purposes only.

Enjoy!

Malik Mesellem
Twitter: @MME_IT

bwapp is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (http://creativecommons.org/licenses/by-nc-nd/4.0/). Copyright © 2014 MME BVBA. All rights reserved.

*/

include("admin/settings.php");

// Connection settings
$server   = isset($db_server) ? $db_server : 'db';
$username = isset($db_username) ? $db_username : 'bwapp';
$password = isset($db_password) ? $db_password : 'bwapp_pass';
$database = isset($db_name) ? strtolower($db_name) : 'bwapp';
if ($server === 'localhost' || $server === '') $server = 'db';
$port = 3306;

// Connection settings, used in older bwapp versions
// $server = "localhost";
// $username = "root";
// $password = "";
// $database = "bwapp";

?>