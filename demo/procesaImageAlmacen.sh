#!/bin/bash


 echo "<odoo>" |tee edialmacen.xml
 echo "<data>" | tee -a edialmacen.xml

 for image in $(ls imagealmacen); do
    echo "<record id=\"burguer.$image\" model=\"burguer.raw\">" | tee -a edialmacen.xml
    echo "<field name=\"name\">$image</field>" | tee -a edialmacen.xml
    echo "<field name=\"image\">$(base64 imagealmacen/$image)</field>" | tee -a edialmacen.xml
    echo "<field name=\"template\">true</field>" | tee -a recursos.xml
    echo "</record>" | tee -a edialmacen.xml
  done

echo "</data>" | tee -a edialmacen.xml
echo "</odoo>" | tee -a edialmacen.xml