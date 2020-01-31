#!/bin/bash

 echo "<odoo>" |tee editienda.xml
 echo "<data>" | tee -a editienda.xml

 for image in $(ls imagetienda); do
    echo "<record id=\"burguer.$image\" model=\"burguer.almacen\">" | tee -a editienda.xml
    echo "<field name=\"name\">$image</field>" | tee -a editienda.xml
    echo "<field name=\"image\">$(base64 imagetienda/$image)</field>" | tee -a editienda.xml
    echo "<field name=\"template\">true</field>" | tee -a editienda.xml
    echo "</record>" | tee -a editienda.xml
  done

echo "</data>" | tee -a editienda.xml
echo "</odoo>" | tee -a editienda