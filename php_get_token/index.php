<?php 
   include("../config.php");
   $code = $_REQUEST["code"];

   if(empty($code)) {
     $dialog_url = "https://www.facebook.com/dialog/oauth?client_id=" 
       . $app_id . "&redirect_uri=" . urlencode($my_url) . "&state=whatever".
"&scope=manage_pages,publish_stream,read_requests,xmpp_login,read_mailbox,read_stream";

     echo("<script> top.location.href='" . $dialog_url . "'</script>");
   }
   if ($_REQUEST['state'] == "whatever") {
     $token_url = "https://graph.facebook.com/oauth/access_token?"
       . "client_id=" . $app_id . "&redirect_uri=" . urlencode($my_url)
       . "&client_secret=" . $app_secret . "&code=" . $code;

     $response = file_get_contents($token_url);
     $params = null;
     parse_str($response, $params);
     echo "<pre>";
     echo "response: ".$response."\n";
     echo "access_token: ".$params['access_token']."\n";
     echo "</pre>";
     echo "<a href=\"index.php\">try again</a>";
   }
?>
