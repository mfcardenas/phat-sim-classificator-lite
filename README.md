# phat-sim-classificator-lite
PHAT-SIM module to detect patterns in the movements in the simulation version lite

# PHAT SIM Classificator
Módulo PHAT-SIM para detectar patrones de movimientos realizados en simulaci&oacute;n.

Estructura del proyecto:

- beaglebone/: script de configuraci&oacuten y lectura de sensores de beaglebone (i2C, USB, otros)
- img/: im&aacute;genes de ayuda para la documentaci&oacute;n del proyecto
- data/: datos de entrenamiento [/train], datos de test [/test] y recogida de datos online (in-live). [1 y 2 aceler&oacute;metros]
- logs/: hist&oacute;rico de envoluci&oacute;n del entrenamiento, calculando precisi&oacuten (para el desarrollador)
- models/: modelo generado y guardado en disco (pkl). Se reutiliza en otros dispositivos de igual caracter&iacute;sticas (32/64bits) [1 y 2 aceler&oacute;metros].
- src/: script de aplicaci&oacute;n

### Procedimiento

Los datos obtenidos del sensor son utilizados para generar un modelo de clasificaci&oacute;n. Dicho modelo es guardado en disco para su posterior uso.

Gestos definidos:

- 0: Stop
- 1: Running
- 2: Walking
- 3: Drink
- 4: Wave attention
- 5: Clap
- 6: Belly?
- 7: Arm?

###### PHAT-SIM Simulations
![Simulations](https://github.com/mfcardenas/phat-sim-classificator-na/blob/master/img/img_phat-sim-animation.png)

###### PHAT-SIM Chart Accelerometer
![Chart Accelerometer](https://github.com/mfcardenas/phat-sim-classificator-na/blob/master/img/img_chart_acceleration.png)

###### PHAT-SIM Classifications
![Classifications](https://github.com/mfcardenas/phat-sim-classificator-na/blob/master/img/img_execute_classificator.png)

### Referencias

1 - [Stisen, A., Blunck, H., Bhattacharya, S., Prentow, T. S., Kjærgaard, M. B., Dey, A., ... & Jensen, M. M. (2015, November). Smart Devices are Different: Assessing and MitigatingMobile Sensing Heterogeneities for Activity Recognition. In Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems (pp. 127-140). ACM.](http://pure.au.dk/portal/files/93103132/sen099_stisenAT3.pdf)

2 - [Ravi, N., Dandekar, N., Mysore, P., & Littman, M. L. (2005, July). Activity recognition from accelerometer data. In AAAI (Vol. 5, pp. 1541-1546).](http://www.aaai.org/Papers/IAAI/2005/IAAI05-013)

3 - [Saumell i Ortoneda, J. (2015). Classification of physical activity from the embedded smartphone sensors: algorithm development and validation.](http://upcommons.upc.edu/handle/2117/78033)
