    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $name = $_POST['name'];
        $email = $_POST['email'];

        $file = 'formData.txt';
        $current = file_get_contents($file); // Read existing data
        $current .= "Name: " . $name . ", Email: " . $email . "\n"; // Append new data
        file_put_contents($file, $current); // Write back to the file

        echo "Data saved successfully!";
    }
    ?>