<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once 'config.inc.php'; // sets $server, $username, $password, $database

if (!function_exists('mysql_connect')) {

    $GLOBALS['_bwapp_mysqli'] = null;

    function mysql_connect($host = null, $user = null, $pass = null) {
        if ($GLOBALS['_bwapp_mysqli'] instanceof mysqli) return $GLOBALS['_bwapp_mysqli'];
        global $server, $username, $password;
        $h = $host ?: $server;
        $u = $user ?: $username;
        $p = $pass ?: $password;
        $link = @new mysqli($h, $u, $p);
        if ($link->connect_error) die('MySQL connect error: ' . $link->connect_error);
        $GLOBALS['_bwapp_mysqli'] = $link;
        return $link;
    }

    function mysql_select_db($db, $link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'] ?: mysql_connect();
        if (!$lnk->select_db($db)) die('Cannot select DB: ' . $lnk->error);
        return true;
    }

    function mysql_query($query, $link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'] ?: mysql_connect();
        $res = $lnk->query($query);
        if ($res === false) die('MySQL query error: ' . $lnk->error);
        return $res;
    }

    function mysql_real_escape_string($str, $link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'] ?: mysql_connect();
        return $lnk->real_escape_string($str);
    }

    function mysql_fetch_array($result) {
        return $result->fetch_array(MYSQLI_BOTH);
    }

    function mysql_fetch_assoc($result) {
        return $result->fetch_assoc();
    }

    function mysql_num_rows($result) {
        return $result->num_rows;
    }

    function mysql_insert_id($link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'];
        return $lnk ? $lnk->insert_id : 0;
    }

    function mysql_affected_rows($link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'];
        return $lnk ? $lnk->affected_rows : 0;
    }

    function mysql_error($link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'];
        return $lnk ? $lnk->error : '';
    }

    function mysql_free_result($result) {
        if ($result instanceof mysqli_result) $result->free();
        return true;
    }

    function mysql_close($link = null) {
        $lnk = $link ?: $GLOBALS['_bwapp_mysqli'];
        if ($lnk instanceof mysqli) {
            $lnk->close();
            $GLOBALS['_bwapp_mysqli'] = null;
            return true;
        }
        return false;
    }
}

$link = mysql_connect();
mysql_select_db($database);
?>