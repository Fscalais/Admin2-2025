<?php
$dbname = getenv('MARIADB_DATABASE');
$dbuser = getenv('MARIADB_USER');
$dbpass = getenv('MARIADB_PASSWORD');
$dbhost = getenv('MARIADB_HOST');

$connect = mysqli_connect($dbhost, $dbuser, $dbpass);
if (!$connect) { http_response_code(500); die("DB connect failed: ".mysqli_connect_error()); }
if (!mysqli_select_db($connect,$dbname)) { http_response_code(500); die("DB select failed"); }

$result = mysqli_query($connect,"SELECT id, product_name, product_price FROM products");
?>
<!doctype html>
<title>Catalogue WoodyToys</title>
<h1>Catalogue WoodyToys</h1>
<table border="1" cellpadding="8" cellspacing="0">
<tr><th>#</th><th>Produit</th><th>Prix</th></tr>
<?php while ($row = mysqli_fetch_row($result)) {
  printf("<tr><td>%s</td><td>%s</td><td>%s</td></tr>",
    htmlspecialchars($row[0]), htmlspecialchars($row[1]), htmlspecialchars($row[2]));
} ?>
</table>
