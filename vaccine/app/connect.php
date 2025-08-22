<?php

/*

bWAPP, or a buggy web application, is a free and open source deliberately insecure web application.
It helps security enthusiasts, developers and students to discover and to prevent web vulnerabilities.
bWAPP covers all major known web vulnerabilities, including all risks from the OWASP Top 10 project!
It is for security-testing and educational purposes only.

Enjoy!

Malik Mesellem
Twitter: @MME_IT

bWAPP is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (http://creativecommons.org/licenses/by-nc-nd/4.0/). Copyright © 2014 MME BVBA. All rights reserved.

*/

// Connection settings
include("config.inc.php");

// Use mysqli instead of the removed mysql_* extension and provide shims
// Connect to the server
$link = @new mysqli($server, $username, $password);

if($link->connect_error)
{
    die("Could not connect to the server: " . $link->connect_error);
}

// Select database
$database = @mysqli_select_db($link, $database);

if(!$database)
{
    die("Could not connect to the database: " . mysqli_error($link));
}

// --- mysql_* compatibility shims for legacy pages ---
if(!function_exists('mysql_query')) {
    function mysql_query($query, $link_identifier = null) {
        $l = $link_identifier ?: ($GLOBALS['link'] ?? null);
        return mysqli_query($l, $query);
    }
}

if(!function_exists('mysql_fetch_array')) {
    function mysql_fetch_array($result, $result_type = MYSQLI_BOTH) {
        return mysqli_fetch_array($result, $result_type);
    }
}

if(!function_exists('mysql_num_rows')) {
    function mysql_num_rows($result) {
        return mysqli_num_rows($result);
    }
}

if(!function_exists('mysql_error')) {
    function mysql_error($link_identifier = null) {
        $l = $link_identifier ?: ($GLOBALS['link'] ?? null);
        return mysqli_error($l);
    }
}

if(!function_exists('mysql_real_escape_string')) {
    function mysql_real_escape_string($string, $link_identifier = null) {
        $l = $link_identifier ?: ($GLOBALS['link'] ?? null);
        return mysqli_real_escape_string($l, $string);
    }
}

if(!function_exists('mysql_close')) {
    function mysql_close($link_identifier = null) {
        $l = $link_identifier ?: ($GLOBALS['link'] ?? null);
        return mysqli_close($l);
    }
}

if(!function_exists('mysql_select_db')) {
    function mysql_select_db($database_name, $link_identifier = null) {
        $l = $link_identifier ?: ($GLOBALS['link'] ?? null);
        return mysqli_select_db($l, $database_name);
    }
}

// ---------------------------------------------------

?>