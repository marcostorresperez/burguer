#!/bin/bash

 echo "<odoo>" |tee edificis.xml
 echo "<data>" | tee -a edificis.xml

 for image in $(ls images); do
    echo "<record id=\"burguer.$image\" model=\"burguer.productor\">" | tee -a edificis.xml
    echo "<field name=\"name\">$image</field>" | tee -a edificis.xml
    echo "<field name=\"image\">$(base64 images/$image)</field>" | tee -a edificis.xml
    echo "<field name=\"template\">true</field>" | tee -a edificis.xml
    echo "</record>" | tee -a edificis.xml
  done

echo "</data>" | tee -a edificis.xml
echo "</odoo>" | tee -a edificis.xml