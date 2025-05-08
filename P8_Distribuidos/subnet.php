<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Subneteo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        label {
            font-weight: bold;
        }
        input[type="text"], input[type="submit"] {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"] {
            background-color: #007BFF;
            color: white;
            cursor: pointer;
            border: none;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .results {
            margin-top: 20px;
        }
        .result-item {
            background-color: #e9ecef;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculadora de Subneteo</h1>
        <form method="post">
            <label for="ip">Dirección IP:</label>
            <input type="text" id="ip" name="ip" placeholder="192.168.1.1" required>
            
            <label for="subnet">Máscara de Subred:</label>
            <input type="text" id="subnet" name="subnet" placeholder="255.255.255.0" required>
            
            <input type="submit" value="Calcular">
        </form>

        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $ip = $_POST["ip"];
            $subnet = $_POST["subnet"];

            function ipToBinary($ip) {
                return str_pad(decbin(ip2long($ip)), 32, '0', STR_PAD_LEFT);
            }

            function binaryToIp($bin) {
                return long2ip(bindec($bin));
            }

            $ipBinary = ipToBinary($ip);
            $subnetBinary = ipToBinary($subnet);
            
            $networkBinary = $ipBinary & $subnetBinary;
            $networkAddress = binaryToIp($networkBinary);

            $wildcardBinary = str_pad(strtr($subnetBinary, '01', '10'), 32, '1', STR_PAD_RIGHT);
            $broadcastBinary = $networkBinary | $wildcardBinary;
            $broadcastAddress = binaryToIp($broadcastBinary);

            echo "<div class='results'>";
            echo "<div class='result-item'><strong>Dirección de Red:</strong> $networkAddress</div>";
            echo "<div class='result-item'><strong>Dirección de Broadcast:</strong> $broadcastAddress</div>";
            echo "</div>";
        }
        ?>
    </div>
</body>
</html>
