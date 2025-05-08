<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Calculadora de Cifrado César</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('img/clouds.png');
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
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }
        h2 {
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
        }
        input[type="text"], input[type="number"], button {
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #5cb85c;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #4cae4c;
        }
        .result {
            background-color: #e9ecef;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Calculadora de Cifrado César</h2>
    <form action="" method="post">
        <label for="texto">Texto a cifrar:</label>
        <input type="text" id="texto" name="texto" placeholder="Introduce el texto aquí" required>
        
        <label for="desplazamiento">Desplazamiento:</label>
        <input type="number" id="desplazamiento" name="desplazamiento" placeholder="Número de posiciones" required>
        
        <button type="submit" name="cifrar">Cifrar</button>
    </form>
    <?php
    if (isset($_POST['cifrar'])) {
        $texto = $_POST['texto'];
        $desplazamiento = $_POST['desplazamiento'];

        function cifrarCesar($texto, $desplazamiento) {
            $resultado = '';
            $desplazamiento = $desplazamiento % 26;
            for ($i = 0; $i < strlen($texto); $i++) {
                $char = $texto[$i];
                if (ctype_alpha($char)) {
                    $min = ctype_lower($char) ? 'a' : 'A';
                    $char = chr((ord($char) + $desplazamiento - ord($min)) % 26 + ord($min));
                }
                $resultado .= $char;
            }
            return $resultado;
        }

        $textoCifrado = cifrarCesar($texto, $desplazamiento);
        echo "<div class='result'><strong>Texto cifrado:</strong> " . htmlspecialchars($textoCifrado) . "</div>";
    }
    ?>
</div>
</body>
</html>
