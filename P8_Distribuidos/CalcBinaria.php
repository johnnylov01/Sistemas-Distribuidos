<?php
function decimalToBinary($decimal) {
    return decbin($decimal);
}

function binaryToDecimal($binary) {
    return bindec($binary);
}

function decimalToHex($decimal) {
    return dechex($decimal);
}

function hexToDecimal($hex) {
    return hexdec($hex);
}

function decimalToOctal($decimal) {
    return decoct($decimal);
}

function octalToDecimal($octal) {
    return octdec($octal);
}

$decimal = isset($_POST['decimal']) ? $_POST['decimal'] : null;
$binary = isset($_POST['binary']) ? $_POST['binary'] : null;
$hex = isset($_POST['hex']) ? $_POST['hex'] : null;
$octal = isset($_POST['octal']) ? $_POST['octal'] : null;

$result = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if ($decimal !== null && $decimal !== "") {
        $result = "Decimal a Binario: " . decimalToBinary($decimal) . "<br>";
        $result .= "Decimal a Hexadecimal: " . decimalToHex($decimal) . "<br>";
        $result .= "Decimal a Octal: " . decimalToOctal($decimal);
    } elseif ($binary !== null && $binary !== "") {
        $result = "Binario a Decimal: " . binaryToDecimal($binary). "<br>";
        $result .= "Binario a Hexadecimal: " . decimalToHex(binaryToDecimal($binary)) . "<br>";
        $result .= "Binario a Octal: " . decimalToOctal(binaryToDecimal($binary));  
    } elseif ($hex !== null && $hex !== "") {
        $result = "Hexadecimal a Decimal: " . hexToDecimal($hex). "<br>";
        $result .= "Hexadecimal a Binario: " . decimalToBinary(hexToDecimal($hex)) . "<br>";
        $result .= "Hexadecimal a Octal: " . decimalToOctal(hexToDecimal($hex));
    } elseif ($octal !== null && $octal !== "") {
        $result = "Octal a Decimal: " . octalToDecimal($octal) . "<br>";
        $result .= "Octal a Binario: " . decimalToBinary(octalToDecimal($octal)) . "<br>";
        $result .= "Octal a Hexadecimal: " . decimalToHex(octalToDecimal($octal));
    } else {
        $result = "Por favor, introduce un valor en decimal, binario, hexadecimal u octal.";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Conversiones</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #33FFA5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        input[type="number"],
        input[type="text"] {
            width: calc(100% - 20px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            border: none;
            background-color: #007BFF;
            color: #fff;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .btn {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            background-color: #007BFF;
            color: #fff;
            border-radius: 4px;
            text-decoration: none;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        p {
            color: #333;
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculadora de Conversiones</h1>
        <form action="" method="post">
            <div class="form-group">
                <label for="decimal">Decimal:</label>
                <input type="number" name="decimal" id="decimal" value="<?php echo htmlspecialchars($decimal); ?>">
            </div>
            <div class="form-group">
                <label for="binary">Binario:</label>
                <input type="text" name="binary" id="binary" value="<?php echo htmlspecialchars($binary); ?>">
            </div>
            <div class="form-group">
                <label for="hex">Hexadecimal:</label>
                <input type="text" name="hex" id="hex" value="<?php echo htmlspecialchars($hex); ?>">
            </div>
            <div class="form-group">
                <label for="octal">Octal:</label>
                <input type="text" name="octal" id="octal" value="<?php echo htmlspecialchars($octal); ?>">
            </div>
            <button type="submit">Convertir</button>
        </form>
        <?php if ($_SERVER["REQUEST_METHOD"] == "POST"): ?>
            <p><?php echo $result; ?></p>
        <?php endif; ?>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var decimalInput = document.getElementById('decimal');
            var binaryInput = document.getElementById('binary');
            var hexInput = document.getElementById('hex');
            var octalInput = document.getElementById('octal');

            decimalInput.addEventListener('input', function() {
                if (decimalInput.value) {
                    binaryInput.disabled = true;
                    hexInput.disabled = true;
                    octalInput.disabled = true;
                } else {
                    binaryInput.disabled = false;
                    hexInput.disabled = false;
                    octalInput.disabled = false;
                }
            });

            binaryInput.addEventListener('input', function() {
                if (binaryInput.value) {
                    decimalInput.disabled = true;
                    hexInput.disabled = true;
                    octalInput.disabled = true;
                } else {
                    decimalInput.disabled = false;
                    hexInput.disabled = false;
                    octalInput.disabled = false;
                }
            });

            hexInput.addEventListener('input', function() {
                if (hexInput.value) {
                    decimalInput.disabled = true;
                    binaryInput.disabled = true;
                    octalInput.disabled = true;
                } else {
                    decimalInput.disabled = false;
                    binaryInput.disabled = false;
                    octalInput.disabled = false;
                }
            });

            octalInput.addEventListener('input', function() {
                if (octalInput.value) {
                    decimalInput.disabled = true;
                    binaryInput.disabled = true;
                    hexInput.disabled = true;
                } else {
                    decimalInput.disabled = false;
                    binaryInput.disabled = false;
                    hexInput.disabled = false;
                }
            });
        });
    </script>
</body>
</html>
