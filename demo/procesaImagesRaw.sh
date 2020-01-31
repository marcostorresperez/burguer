#!/bin/bash


 echo "<odoo>" |tee recursos.xml
 echo "<data>" | tee -a recursos.xml

 for image in $(ls imageraw); do
    echo "<record id=\"burguer.$image\" model=\"burguer.raw\">" | tee -a recursos.xml
    echo "<field name=\"name\">$image</field>" | tee -a recursos.xml
    echo "<field name=\"image\">$(base64 imageraw/$image)</field>" | tee -a recursos.xml
    echo "<field name=\"template\">true</field>" | tee -a recursos.xml
    echo "</record>" | tee -a recursos.xml
  done

echo "</data>" | tee -a recursos.xml
echo "</odoo>" | tee -a recursos.xml