# -*- coding: utf-8 -*-
class ExampleBots(object):

    bank_bot_code = """[define cajeros (list
    '("Isabel La Católica - Av. Manquehue Sur N° 1567, Las Condes" -33.4245626 -70.5645574 "Av. Manquehue Sur N° 1567, Las Condes")
    '("Americo Vespucio - Av. Americo Vespucio Sur Nº 1816" -33.42900497 -70.57454766 "Av. Americo Vespucio Sur Nº 1816")
    '("La Reina - Avda. Príncipe de Gales N°6161, local 1" -33.4385765 -70.56884019 "Avda. Príncipe de Gales N°6161, local 1")
    '("Príncipe de Gales - Príncipe de Gales Nº 7056, La Reina" -33.4387906 -70.5588757 "Príncipe de Gales Nº 7056, La Reina")
    '("Plaza Atenas - Av. Cuarto Centenario Nº 914, Las Condes" -33.41648233 -70.55435092 "Av. Cuarto Centenario Nº 914, Las Condes")
    '("Apumanque - Avda. Manquehue Sur 31" -33.4092247 -70.5671926 "Avda. Manquehue Sur 31")
    '("Rosario Norte - Av. Apoquindo Nº 5710, Las Condes" -33.40931508 -70.57044181 "Av. Apoquindo Nº 5710, Las Condes")
    '("Cerro El Plomo - Rosario Norte 555 local 102" -33.4087844 -70.567069 "Rosario Norte 555 local 102, Las Condes, Santiago, Chile. ")
    '("Noruega - Av. Apoquindo 6427 local 2, Las Condes." -33.40829924 -70.56439269 "Av. Apoquindo 6427 local 2, Las Condes.")
    '("La Gloria - Orinoco 90, Torre 1, piso 20, Las Condes" -33.411079 -70.578879 "Orinoco 90, Torre 1, piso 20, Las Condes")
    '("Escuela Militar - Av. Apoquindo Nº 4385" -33.41504117 -70.58485183 "Av. Apoquindo Nº 4385")
    '("Subcentro Escuela Militar - Av. Apoquindo 4400 Local 144" -33.4074818 -70.5624574 "Av. Apoquindo 4400 Local 144")
    '("Juan Montalvo - Avda. Apoquindo 6832, local 4" -33.40736111 -70.55987835 "Avda. Apoquindo 6832, local 4")
    '("Fleming - Alexandre Fleming 8896, local 1" -33.423931 -70.539529 "Alexandre Fleming 8896, local 1")
    '("El Golf - Gertrudis Echeñique Nº 49" -33.41628988 -70.59200733 "Gertrudis Echeñique Nº 49")
    '("Edificio Corporativo - Av. El Golf 125" -33.4147843 -70.5916999 "Av. El Golf 125")
    '("Carlos Ossandón - Carlos Ossandon 1331" -33.4412741 -70.5432108 "Carlos Ossandon 1331")
    '("Los Domínicos - Metro Los Domínicos Avenida Apoquindo 9000 local 4" -33.407859 -70.545109 "Metro Los Domínicos Avenida Apoquindo 9000 local 4 ")
    '("Patio La Reina - Av. Larraín 8751, Locales 3 y 4" -33.45257 -70.569845 "Av. Larraín 8751, Locales 3 y 4")
    '("Boulevard Kennedy - Av. Presidente Kennedy Nº 5773 Local 3" -33.39996636 -70.57408367 "Av. Presidente Kennedy Nº 5773 Local 3")
    '("Plaza Egaña - Av. Irarrázaval Nº 5580, Ñuñoa" -33.4534209 -70.5722622 "Av. Irarrázaval Nº 5580, Ñuñoa")
    '("La Pastora - Av. Isidora Goyenechea N° 3280" -33.41437195 -70.59652209 "Av. Isidora Goyenechea N° 3280")
    '("Banca Preferencial Napoleón - Av. El Bosque 130 Piso 10" -33.420231 -70.599497 "Av. El Bosque 130 Piso 10")
    '("Banca Preferencial Isidora - Isidora Goyenechea N° 3.000" -33.41409 -70.59849 "Isidora Goyenechea N° 3.000")
    '("Apoquindo - Av. Apoquindo Nº 2705" -33.4181871 -70.60096635 "Av. Apoquindo Nº 2705")
    '("Torre El Bosque Premier - Av. El Bosque Norte 0177, piso 21, Of. 2102" -33.4152461 -70.6011845 "Av. El Bosque Norte 0177, piso 21, Of. 2102")
    '("Plaza San Pío - Pío XI N° 1615, local 6" -33.3976017 -70.5826798 "Pío XI 1615, Vitacura, Santiago, Chile  ")
    '("ALONSO DE CORDOVA 3788 OFICINA 51 - A" -33.4021917 -70.5931029 "Alonso de Cordova 3788")
    '("Vitacura Vespucio - Avda. Vitacura N°4380, local 2" -33.39880431 -70.58860826 "Avda. Vitacura N°4380, local 2")
    '("Vitacura - Av. Vitacura Nº 4009, Vitacura" -33.40018734 -70.59135561 "Av. Vitacura Nº 4009, Vitacura")
    '("Torre Titanium - Isidora Goyenechea 2800, Of 303" -33.4137114 -70.6036572 "Isidora Goyenechea 2800, Of 303")
    '("Bilbao - Francisco Bilbao Nº 2129" -33.437794 -70.604597 "Francisco Bilbao Nº 2129 ")
    '("11 de Septiembre - Av. 11 de Septiembre Nº 2357, Providencia" -33.420423 -70.60652 "Av. 11 de Septiembre Nº 2357, Providencia")
    '("World Trade Center - Av. Andres Bello Nº 2607, Santiago" -33.41572 -70.60611 "Av. Andres Bello Nº 2607, Santiago")
    '("Paseo Las Palmas Premier - Coyancura 2283 piso 8" -33.42303 -70.60805 "Coyancura 2283 piso 8")
    '("Padre Hurtado - Avda. Las Condes 9050, Las Condes" -33.3991249 -70.5400417 "Avda. Las Condes 9050, Las Condes")
    '("Costanera Center - Avenida Andrés Bello 2465,Local 124" -33.4177376 -70.607335 "Avenida Andrés Bello 2465, Providencia, Santiago, Chile")
    '("Luis Carrera - Avda. Luis Pasteur N°5515, local 2" -33.392329 -70.580947 "Avda. Luis Pasteur N°5515, local 2")
    '("Plaza Ñuñoa - Av. Irarrázabal Nº 3665" -33.4553775 -70.5923413 "Av. Irarrázabal Nº 3665")
    '("Ricardo Lyon - Ricardo Lyon 87 Local 5" -33.4225005 -70.60979095 "Ricardo Lyon 87 Local 5")
    '("Banca Privada Magdalena - Magdalena 140 Piso 15" -33.42022 -70.6099047 "Magdalena 140 Piso 15")
    '("Providencia - Av. Providencia Nº 2140, Providencia" -33.4223801 -70.6109531 "Av. Providencia Nº 2140, Providencia, Santiago, Chile.")
    '("Nueva Costanera - Avenida Nueva Costanera 3889" -33.39872775 -70.59763165 "Avenida Nueva Costanera 3889")
    '("Luis Pasteur - Avda. Luis Pasteur N°5840, local 101" -33.388443 -70.57785 "Avda. Luis Pasteur N°5840, local 101")
    '("Vitacura Oriente - Av. Vitacura Nº 6852, Vitacura" -33.38722728 -70.56578905 "Av. Vitacura Nº 6852, Vitacura")
    '("Bicentenario - Avda. Bicentenario N° 3883, local 5" -33.39823121 -70.60045421 "Avda. Bicentenario N° 3883, local 5")
    '("La Concepción - Av Providencia Nº 1819. Providencia" -33.4253774 -70.6144507 "Av Providencia 1819, Providencia, Santiago, Chile.")
    '("Padre Hurtado Norte - Padre Hurtado N°1183 A" -33.387345 -70.548835 "Padre Hurtado N°1183 A")
    '("Las Tranqueras - Av. Vitacura Nº 8157, Vitacura" -33.38541819 -70.55534684 "Av. Vitacura Nº 8157, Vitacura")
    '("Ñuñoa - Av. Irarrázaval Nº 2525, Ñuñoa" -33.4542239 -70.6047427 "Av. Irarrázaval Nº 2525, Ñuñoa")
    '("Antonio Varas - Antonio Varas Nº 03" -33.4279029 -70.6175933 "Antonio Varas 3, Providencia, Santiago, Chile")
    '("Centro Empresarios Panam. Norte - Av. Américo Vespucio Sur 2982" -33.3904892 -70.5959783 "Av. Américo Vespucio Sur 2982")
    '("Camino El Alba - Camino El Alba Nº 11101" -33.401247 -70.522692 "Camino El Alba Nº 11101")
    '("Torre Santa Maria - Los Conquistadores 1700,Piso 1 Local 1, Providencia" -33.42329675 -70.62216136 "Los Conquistadores 1700,Piso 1 Local 1, Providencia")
    '("Santa MarÍa de Manquehue - Av. Santa María Nº 6740, Locales 1, 2, 3 y 4 Vitacura" -33.37669589 -70.57083902 "Av. Santa María Nº 6740, Locales 1, 2, 3 y 4 Vitacura")
    '("Estoril - Estoril 88 Local 1" -33.38481992 -70.53238273 "Estoril 88 Local 1")
    '("San Carlos de Apoquindo - Avda. Camino el Alba 11969, Local 211" -33.40111663 -70.51395471 "Avda. Camino el Alba 11969, Local 211")
    '("Clínica Las Condes - Lo Fontecilla Nº 441" -33.38372255 -70.53070462 "Lo Fontecilla Nº 441")
    '("Seminario - Avda. Francisco Bilbao N° 445" -33.441967 -70.626289 "Avda. Francisco Bilbao N° 445")
    '("Ciudad Empresarial - Av. del Parque N° 4.023, local 109" -33.3940895 -70.6205829 "Ciudad Empresarial - Av. del Parque 4023, Huechuraba, Santiago, Chile ")
    '("Plaza Italia - Av. Providencia Nº 153" -33.4366702 -70.6323142 "Av. Providencia Nº 153, Providencia, Santiago, Chile.")
    '("Clínica Universidad Los Andes - Av. La Plaza 2501, piso 3" -33.405382 -70.503648 "Av. La Plaza 2501, piso 3")
    '("Las Condes - Av. Las Condes Nº 11336, Vitacura" -33.37766374 -70.52833815 "Av. Las Condes Nº 11336, Vitacura")
    '("Plaza Baquedano - Av. L. B. O´Higgins Nº 4, Santiago" -33.4372709 -70.6351631 "Av Libertador Bernardo O'Higgins 4, Providencia, Santiago, Chile")
    '("Irarrázaval - Av. Irarrázaval Nº 099" -33.45250972 -70.62927576 "Av. Irarrázaval Nº 099")
    '("Santa Isabel Portugal - Santa Isabel 209 Local 2" -33.447988 -70.6345114 "Santa Isabel 209 Local 2")
    '("Quilín - Mar Tirreno N° 3349 Local 1006, Peñalolen" -33.48653068 -70.57727148 "Mar Tirreno N° 3349 Local 1006, Peñalolen")
    '("Macul - Av. Macul Nº 2906, Macul" -33.4809231 -70.5989249 "Av. Macul Nº 2906, Macul")
    '("La Ligua - Ortiz de Rozas 298" -33.3971086 -70.6314505 "Ortiz de Rozas 298")
    '("Peñalolén - Av. Consistorial 3503 Local 13 Centro Comercial Consistorial" -33.48899999 -70.55035648 "Av. Consistorial 3503 Local 13 Centro Comercial Consistorial")
    '("Bellas Artes - Monjitas N°390" -33.4366636 -70.6450016 "Monjitas N°390")
    '("La Merced - Merced Nº 595, Santiago Centro" -33.4379231 -70.6455318 "Merced Nº 595, Santiago Centro")
    '("Biblioteca Nacional Premier - Miraflores 178 Of. 1102" -33.4405637 -70.6452505 "Miraflores 178 Of. 1102")
    '("Miraflores - Agustinas Nº 615, Santiago" -33.4403011 -70.6454815 "Agustinas Nº 615, Santiago")
    '("Recoleta - Av. Recoleta Nº 286, Recoleta" -33.4297455 -70.64735914 "Av. Recoleta Nº 286, Recoleta")
    '("Cantagallo - Av. Las Condes 12340, local 6" -33.372454 -70.517499 "Av. Las Condes 12340, local 6")
    '("Santa Elena - Santa Elena Nº 2310, San Joaquín, Santiago" -33.4735779 -70.6260671 "Santa Elena Nº 2310, San Joaquín, Santiago")
    '("Banca Preferencial Edificio Opera - Huérfanos #835 Oficina Piso 11" -33.439315 -70.647664 "Huérfanos #835 Oficina Piso 11")
    '("Teatro Municipal - San Antonio N°224" -33.440011 -70.648069 "San Antonio N°224")
    '("Moneda II - Moneda N° 864" -33.4417801 -70.6487126 "Moneda N° 864")
    '("Estado - Estado Nº 355" -33.4391488 -70.6495695 "Estado 355, Santiago, Chile")
    '("Ahumada - Moneda N° 975, local 3" -33.44183489 -70.650444 "Moneda N° 975, local 3")
    '("Hospital Clínico Universidad de Chile - Santos Dumont 999" -33.420406 -70.65295 "Santos Dumont 999")
    '("Bci Home Santiago - Bandera 341, Piso 9" -33.439186 -70.6524145 "Bandera 341, Piso 9")
    '("Centro Empresarios Bandera 1 Oficina Central - Bandera 250 piso 1" -33.4402281 -70.6523019 "Bandera 250, Santiago, Chile")
    '("Oficina Central - Huérfanos Nº 1134, Santiago" -33.4398343 -70.6527831 "Huérfanos Nº 1134, Santiago")
    '("Edificio Prat Premier - Av. Prat 847, Piso 2" -33.4558707 -70.6479542 "Av. Prat 847, Piso 2")
    '("Paseo Huérfanos - Huérfanos 1263 local 1" -33.43991464 -70.65472001 "Huérfanos 1263 local 1")
    '("Teatinos - Teatinos 235, Santiago" -33.4408985 -70.6549664 "Teatinos 235, Santiago")
    '("Centro de Negocios - Huérfanos 1112" -33.4400547 -70.6553456 "Huérfanos 1112")
    '("POWER CENTER - JOSE ALCALDE DELANO 10581 LOCAL 4 Y 6" -33.3555863 -70.5351105 "JOSE ALCALDE DELANO 10581, Lo Barnechea, Santiago")
    '("Plaza Bulnes - Nataniel Cox Nº 27, Santiago Centro" -33.4453623 -70.6539966 "Nataniel Cox Nº 27, Santiago Centro")
    '("Santa Lucía - Huérfanos Nº 669, Local 1-9, Santiago" -33.4691199 -70.641997 "Huérfanos Nº 669, Local 1-9, Santiago")
    '("Plaza Almagro - Av. Diez de Julio Nº 1140, Santiago" -33.454261 -70.651449 "Av. Diez de Julio Nº 1140, Santiago")
    '("Agustinas - Amunategui 154" -33.4421761 -70.6561234 "Amunategui 154")
    '("Avenida Matta - Av. Matta Nº 1132" -33.45988604 -70.64964062 "Av. Matta Nº 1132")
    '("Plaza San Lucas - Avda. La Dehesa N° 457, local 2" -33.36229297 -70.51486194 "Avda. La Dehesa N° 457, local 2")
    '("La Dehesa - Avda. La Dehesa 1788" -33.356575 -70.5175 "Avda. La Dehesa 1788")
    '("San Diego - San Diego Nº 2043" -33.472448 -70.647983 "San Diego Nº 2043")
    '("Los Trapenses - Av. Camino Los Trapenses N°3515 Loc 202" -33.34391075 -70.54472116 "Av. Camino Los Trapenses N°3515 Loc 202")
    '("El Rodeo - Avda. La Dehesa N°2035, locales 15 y 16" -33.351946 -70.518131 "Avda. La Dehesa N°2035, locales 15 y 16")
    '("Almirante Latorre - Av. B. O'Higgins Nº 2102" -33.44764174 -70.66499946 "Av. B. O'Higgins Nº 2102")
    '("TBANC - Av. Libertador Bernardo O' Higgins 2432" -33.4486565 -70.669942 "Av. Libertador Bernardo O' Higgins 2432")
    '("Beaucheff - Av. Beaucheff Nº 1453" -33.46662774 -70.66388576 "Av. Beaucheff Nº 1453")
    '("El Llano - El Llano Subercaseaux 3397" -33.48549183 -70.65068534 "El Llano Subercaseaux 3397")
    '("Estación Central - Unión Latino Americana Nº 40" -33.45088394 -70.67385248 "Unión Latino Americana Nº 40")
    '("Centro Empresarios Estación Central - Unión Latinoamericana 40" -33.4504407 -70.6740677 "Unión Latinoamericana 40, Estación Central, Santiago, Chile")
    '("Isla de Maipo - Santelices N° 615" -33.3804567 -70.6647241 "Santelices N° 615")
    '("Matucana - Chacabuco Nº 848, Santiago" -33.4351067 -70.6792414 "Chacabuco Nº 848, Santiago")
    '("Renca - Av. Ptde. E. Frei Montalva Nº 1792, Renca" -33.40690297 -70.68056066 "Av. Ptde. E. Frei Montalva Nº 1792, Renca")
    '("La Florida - Av. Vicuña Mackenna Oriente 7385, La Florida" -33.5212524 -70.5989039 "Av. Vicuña Mackenna Oriente 7385, La Florida")
    '("San Miguel - Gran Av. José M. Carrera Nº 4780.San Miguel" -33.49770813 -70.6530588 "Gran Av. José M. Carrera Nº 4780.San Miguel")
    '("El Carmen de Huechuraba - Av. Pedro Fontova 6251, Local 3" -33.36631815 -70.67017355 "Av. Pedro Fontova 6251, Local 3")
    '("Club Hípico de Santiago 4676, Pedro Aguirre Cerda, Santiago" -33.4919827 -70.668105 "Club Hípico de Santiago 4676")
    '("Panamericana Norte - Av. A. Vespucio Sur Nº 2982, Conchalí" -33.368545 -70.67783 "Av. A. Vespucio Sur Nº 2982, Conchalí")
    '("Rojas Magallanes - Rojas Magallanes N°3638" -33.5357656 -70.5745186 "Rojas Magallanes N°3638")
    '("Huechuraba - Av. Américo Vespucio 1737 Local 2154, Mall Plaza Norte" -33.36707572 -70.67805813 "Av. Américo Vespucio 1737 Local 2154, Mall Plaza Norte")
    '("Altos de la Florida - La Florida Nº 9343" -33.538481 -70.5725788 "La Florida Nº 9343, Región Metropolitana, Santiago, Chile")
    '("Base Aerea Cerrillos - Av. Pedro Aguirre Cerda Nº 5.500" -33.48945949 -70.70049577 "Av. Pedro Aguirre Cerda Nº 5.500")
    '("La Cisterna - Gran Av.José M. Carrera 8445, Las Cisterna" -33.53227995 -70.6632211 "Gran Av.José M. Carrera 8445, Las Cisterna")
    '("Cerrillos - Av. Pedro Aguirre Cerda Nº 6049" -33.49377846 -70.70519015 "Av. Pedro Aguirre Cerda Nº 6049")
    '("Arica Norte - Diego Portales 749" -33.5627295 -70.5786623 "Diego Portales 749")
    '("Mall Plaza Tobalaba - Avda. Camilo Henríquez N° 3296, local BS 108 - 110" -33.577385 -70.553114 "Avda. Camilo Henríquez N° 3296, local BS 108 - 110")
    '("Quilicura - José Francisco Vergara N°491" -33.3672309 -70.7340495 "José Francisco Vergara N°491, Quilicura, Santiago, Chile")
    '("Maipú - Av. Pajaritos Nº 5100, Local 12, Maipú" -33.47468796 -70.74097349 "Av. Pajaritos Nº 5100, Local 12, Maipú")
    '("Mall Plaza Oeste - Avda. Américo Vespucio 1501, local C-278 - C-282 - C-286 - BS-124" -33.51686812 -70.71712 "Avda. Américo Vespucio 1501, local C-278 - C-282 - C-286 - BS-124")
    '("Piedra Roja - Av. Paseo Colina Sur 14500 local 101, Colina" -33.27744128 -70.62713055 "Av. Paseo Colina Sur 14500 local 101, Colina")
    '("El Bosque - Av. José Miguel Carrera paradero 32 1/2" -33.557267 -70.677817 "Av. José Miguel Carrera paradero 32 1/2")
    '("Maipú Pajaritos - Avda. Los Pajaritos 2664, Maipú" -33.4839444 -70.7465111 "Avda. Los Pajaritos 2664, Maipú")
    '("Mall Arauco Maipú - Avda Americo Vespucio 399 Local B 02" -33.4823731 -70.75198636 "Avda Americo Vespucio 399 Local B 02")
    '("Moneda - Miguel Cruchaga Tocornal 920, Santiago" -33.5935111 -70.5793159 "Miguel Cruchaga Tocornal 920, Santiago")
    '("Chicureo - Camino Chicureo Km 2,2" -33.285698 -70.678001 "Camino Chicureo Km 2,2")
    '("Camino Lo Echevers 550" -33.3735149 -70.7590944 "Camino Lo Echevers 550")
    '("Las Mercedes - Avda Concha y Toro N°1036" -33.60167007 -70.57928105 "Avda Concha y Toro N°1036")
    '("Puente Alto - Irarrázabal Nº 0178, Puente Alto" -33.60751014 -70.57394295 "Irarrázabal Nº 0178, Puente Alto")
    '("5 de Abril - 5 de Abril N°180" -33.510366 -70.759725 "5 de Abril N°180")
    '("San Andrés Premier - Jorge Alessandri 3177, piso 7" -33.564646 -70.710865 "Jorge Alessandri 3177, piso 7")
    '("Base Aérea Pudahuel - Aeropuerto sector Norte lote 16" -33.396403 -70.793753 "Aeropuerto sector Norte lote 16")
    '("Paseo Puente - Puente Nº 779, Santiago" -33.578651 -70.7071405 "Puente Nº 779, Santiago")
    '("San Bernardo - Covadonga Nº 664, San Bernardo" -33.5942529 -70.7065787 "Covadonga Nº 664, San Bernardo")
    '("Mall Plaza San Bernardo - Presidente Jorge Alessadri N° 20,040, locales BS 122, 126 y 130" -33.6316089 -70.71281424 "Presidente Jorge Alessadri N° 20,040, locales BS 122, 126 y 130")
    '("Colina - Font Nº 146" -33.202846 -70.675298 "Font Nº 146")
    '("Padre Alberto Hurtado - Camino San Alberto Hurtado 3295" -33.5735883 -70.8134319 "Camino San Alberto Hurtado 3295, Región Metropolitana, Chile")
    '("Calera de Tango - Av. Calera Tango 345 Municipalidad Calera Tango" -33.629103 -70.768697 "Av. Calera Tango 345 Municipalidad Calera Tango")
    '("San José de Maipo - Uno Sur Nº 225, San José de Maipo" -33.6408406 -70.3523686 "Uno Sur Nº 225, San José de Maipo")
    '("Buin - JJ Pérez Nº 302" -33.7327659 -70.74141194 "JJ Pérez Nº 302")
    '("Saladillo - Av. Santa Teresa 679, Los Andes" -32.8359327 -70.6039869 "Av. Santa Teresa 679, Los Andes")
    '("Los Andes - Esmeralda Nº 347, Los Andes" -32.8332936 -70.5978586 "Esmeralda Nº 347, Los Andes")
    '("Cordillera Preferencial - Argentina 17 piso 4, oficina 402" -32.8309974 -70.5924856 "Avenida Argentina 17, Los Andes")
    '("Melipilla - Serrano Nº 210, Melipilla" -33.6828262 -71.2137351 "Serrano Nº 210, Melipilla")
    '("San Felipe - Arturo Prat Nº 161, San Felipe" -32.7502436 -70.7246347 "Arturo Prat Nº 161, San Felipe")
    '("Lampa - Baquedano 739" -34.1655788 -70.7670241 "Baquedano 739")
    '("Bci Home Rancagua - Bueras Nº 470, Rancagua" -34.170928 -70.744937 "Bueras Nº 470, Rancagua")
    '("Av. San Juan Nº 133 C Piso 1, Machalí " -34.1827652 -70.6486342 "San Juan Nº 133, Machalí")
    '("Rancagua II - Millán Nº 886, Rancagua" -34.1737718 -70.7481936 "Millán Nº 886, Rancagua")
    '("El Cobre - Carretera El Cobre Nº 1002" -34.1865831 -70.72105338 "Carretera El Cobre Nº 1002")
    '("Villa Alemana - Avda. Valparaíso N° 896, Villa Alemana" -33.0439541 -71.3692845 "Avda. Valparaíso N° 896, Villa Alemana")
    '("Hotel Prat Iquique - Anibal Pinto 601" -32.8839139 -71.2497172 "Anibal Pinto 601")
    '("Quillota - Av. L. B. O´Higgins Nº102, Quillota" -32.87840882 -71.24689088 "Av. L. B. O´Higgins Nº102, Quillota")
    '("Quilpué - Claudio Vicuña Nº 898, Quilpué" -33.0469042 -71.4419194 "Claudio Vicuña Nº 898, Quilpué")
    '("La Calera - José Joaquín Pérez Nº 244, La Calera" -32.78757 -71.189657 "José Joaquín Pérez Nº 244, La Calera")
    '("San Antonio - Av. Centenario Nº 145, San Antonio" -33.5791403 -71.6077543 "Av. Centenario 145, San Antonio, Región de Valparaiso, Chile")
    '("Multiservicio Centro Comercial del lago - CURAUMA Ruta 68 local 1, Valparaiso." -33.118122 -71.561238 "Ruta 68 N°1150 Placilla de Peñuelas")
    '("Caja Auxiliar San Antonio - Alan T. C. Macowan Marks Nº 245" -33.58876551 -71.61456546 "Alan T. C. Macowan Marks Nº 245")
    '("Llo-Lleo - Av. Providencia Nº 45, San Antonio" -33.6122255 -71.6177642 "Av. Divina Providencia Nº 45, San Antonio, Región de Valparaíso, Chile")
    '("Libertad - Av. Libertad Nº 269" -33.019637 -71.551144 "Av. Libertad Nº 269")
    '("8 Norte - Libertad Nº 705" -33.015021 -71.550115 "Libertad Nº 705")
    '("Coraceros - Av. Nueva Libertad 1410 loc. 1" -33.00788583 -71.54816781 "Av. Nueva Libertad 1410 loc. 1")
    '("Caja Auxiliar Algarrobo - Avda Carlos Alessandri 1870" -33.3620114 -71.6699213 "Avda Carlos Alessandri 1870")
    '("Las Salinas - Av. Jorge Montt n°11700 Base Naval Las Salinas" -32.99483146 -71.54706197 "Av. Jorge Montt n°11700 Base Naval Las Salinas")
    '("Reñaca - Av. Borgoño Nº 14477" -32.971232 -71.543678 "Av. Borgoño Nº 14477")
    '("Concon - Av. Manantiales 1455" -32.927543 -71.5144245 "Av. Manantiales 1455, concón, Chile")
    '("Viña del Mar - Av. Valparaíso Nº 193" -33.0446187 -71.6022217 "Av. Valparaíso Nº 193, Región de Valparaiso, Chile")
    '("Almendral - Av. Pedro Montt N°2867" -33.047033 -71.605459 "Av. Pedro Montt N°2867")
    '("Bci Home Valparaíso - Prat 827 of 502-A" -33.0403426 -71.6271243 "Prat 827 of 502-A")
    '("Valparaiso - Prat Nº 801, Valparaíso" -33.0402393 -71.6273512 "Prat Nº 801, Valparaíso")
    '("Caja Auxiliar Quintero - Piloto Alcayaga Nº 1749, Quintero" -32.78382557 -71.5261511 "Piloto Alcayaga Nº 1749, Quintero")
    '("San Fernando - Manuel Rodríguez Nº 901, San Fernando" -34.5879673 -70.9853194 "Manuel Rodríguez Nº 901, San Fernando")
    '("Santa Cruz - Plaza de Armas N°286 - A" -34.6401517 -71.3654825 "Plaza de Armas 286, Santa Cruz, VI Región, Chile")
    '("Huanhuali - Av. El Santo Nº 1570" -32.133853 -71.370858 "Av. El Santo Nº 1570")
    '("Mall Curico - Av. Bernardo O'Higgins Nº 201, Local 69, Curicó " -34.93796761 -71.20102221 "Av. Bernardo O'Higgins Nº 201, Local 69, Curicó ")
    '("Curicó - Merced Nº 315" -34.984505 -71.238976 "Merced Nº 315")
    '("Caja Auxiliar Curicó - Merced Nº 315" -34.984505 -71.238976 "Merced Nº 315")
    '("Casablanca - Avda. Diego Portales N°105" -31.6265565 -71.1692867 "Avda. Diego Portales N°105")
    '("Mall Plaza Maule - Avda. Circunvalación Oriente N°1055, local N° 163 - 164 y 165,Talca" -35.42716844 -71.6262892 "Avda. Circunvalación Oriente N°1055, local N° 163 - 164 y 165,Talca")
    '("Talca - Uno Sur Nº 732, Talca" -35.4270369 -71.6661542 "Uno Sur Nº 732, Talca")
    '("Linares - Independencia Nº 380, Linares" -35.8461795 -71.597827 "Independencia Nº 380, Linares, Chile")
    '("Ovalle - Vicuña Mackenna Nº 440, Ovalle" -30.60417797 -71.20376102 "Vicuña Mackenna Nº 440, Ovalle")
    '("Chillán - Libertad Nº 601" -36.60629 -72.10224 "Libertad Nº 601")
    '("Calama Granaderos - Alonso de Ercilla 2198-2192" -36.6251139 -72.0883069 "Alonso de Ercilla 2198-2192")
    '("Coquimbo - Aldunate Nº 890" -29.95191229 -71.33780827 "Aldunate Nº 890")
    '("Bci Home La Serena - Arturo Prat Nº 614, La Serena" -29.901979 -71.248305 "Arturo Prat Nº 614, La Serena")
    '("La Serena Premier - Los Carrera #380 Of. 218, edificio María Elena" -29.9020922 -71.2512707 "Los Carrera #380 Of. 218, edificio María Elena")
    '("Base Naval Talcahuano - Jorge Montt s/n Base Naval (T)" -36.697214 -73.108477 "Jorge Montt s/n Base Naval (T)")
    '("Talcahuano - Avda. Colón Nº 640, Talcahuano" -36.71531661 -73.11076489 "Avda. Colón Nº 640, Talcahuano")
    '("Las Higueras Colón - Avda Colón 3252, Local A" -36.742186 -73.098155 "Avda Colón 3252, Local A")
    '("Plaza El Trébol - Autop. Concep.-Talcah. 8671 L. B1, Talcahuano" -36.79281059 -73.06921097 "Autop. Concep.-Talcah. 8671 L. B1, Talcahuano")
    '("Chacabuco Concepción - Chacabuco 1085 Local 101" -36.828157 -73.042749 "Chacabuco 1085 Local 101")
    '("Concepción Plaza - Barros Arana 598" -36.8268684 -73.0512118 "Barros Arana 598, Concepción, Chile")
    '("Edificio Centro Plaza - Cochrane 635, Of. 1302, piso 13 torre A" -36.82958 -73.048708 "Cochrane 635, Of. 1302, piso 13 torre A")
    '("Bci Home Concepción - O'Higgins Nº 399" -36.829217 -73.052782 "O'Higgins Nº 399")
    '("Pedro de Valdivia - Pedro de Valdivia Nº 1009, Concepción" -36.84588627 -73.05148915 "Pedro de Valdivia Nº 1009, Concepción")
    '("San Pedro de la Paz - Pedro Aguirre Cerda N° 1055, local 4 y 5" -36.83899856 -73.09642679 "Pedro Aguirre Cerda N° 1055, local 4 y 5")
    '("Andalué - Camino el Venado 560 local A-3" -36.84506404 -73.0949374 "Camino el Venado 560 local A-3")
    '("Los Angeles - Valdivia Nº 286, Los Angeles" -37.4710994 -72.3523821 "Valdivia Nº 286, Los Angeles")
    '("Vallenar - Arturo Prat Nº 911, Vallenar" -28.576003 -70.7601809 "Arturo Prat Nº 911, Vallenar")
    '("Victoria - Suiza N° 1.108" -38.232967 -72.33223 "Suiza N° 1.108")
    '("Cabrero - Anibal Pinto 399" -38.7303526 -72.5784397 "Anibal Pinto 399")
    '("Paseo Prat Temuco - Avenida Prat 955 local 1" -38.732205 -72.58914 "Avenida Prat 955, local 1, Temuco")
    '("Temuco - Manuel Bulnes Nº 615, Temuco" -38.7396243 -72.5892441 "Manuel Bulnes Nº 615, Temuco")
    '("Avenida Alemania - Av. Alemania Nº 0888, L1" -38.733104 -72.61544 "Av. Alemania Nº 0888, L1")
    '("Pucon - Fresia Nº 174, Pucón" -39.272254 -71.977629 "Fresia Nº 174, Pucón")
    '("Villarrica - Pedro de Valdivia Nº 701, Villarrica" -39.28313099 -72.2281221 "Pedro de Valdivia Nº 701, Villarrica")
    '("Copiapó Sur - Av. Copayapu N°2406 Local 1008" -27.38227254 -70.31650125 "Av. Copayapu N°2406 Local 1008")
    '("Copiapó - Chacabuco Nº 449" -27.366015 -70.33271 "Chacabuco Nº 449")
    '("Caldera - Ossa Cerda N° 350" -27.0681466 -70.8224216 "Ossa Cerda N° 350")
    '("Panguipulli - Martínez de Rozas Nº 894, Panguipulli" -39.643632 -72.336494 "Martínez de Rozas Nº 894, Panguipulli")
    '("Isla Teja - Las Encinas N° 111" -39.8103432 -73.2522246 "Las Encinas N° 111")
    '("Bci Home Valdivia - Arauco Nº 101, Valdivia" -39.814731 -73.248155 "Arauco Nº 101, Valdivia")
    '("Mall Plaza Alameda - Avda. Libertador Bernardo Ohiggins 3470, local E116/118" -39.8370536 -73.2143756 "Avda. Libertador Bernardo Ohiggins 3470, local E116/118")
    '("Chañaral - Maipú Nº 319" -26.34755919 -70.62117848 "Maipú Nº 319")
    '("La Union - Arturo Prat Nº 702, La Unión" -40.2910786 -73.0810856 "Arturo Prat Nº 702, La Unión")
    '("El Salvador - Av.18 de Septiembre 2136" -26.244642 -69.622992 "Av.18 de Septiembre 2136")
    '("Osorno - Mackenna Nº 801, Osorno" -40.5745781 -73.13652816 "Mackenna Nº 801, Osorno")
    '("Llanquihue - Av. Vicente Pérez Rosales Nº 304, Llanquihue" -41.2611282 -73.00636769 "Av. Vicente Pérez Rosales Nº 304, Llanquihue")
    '("Alto Cauquenes Premier - Carretera Pdte. Eduardo Frei 340 of.1 piso 2" -41.2746108 -72.9994114 "Carretera Pdte. Eduardo Frei 340 of.1 piso 2")
    '("Puerto Varas - Del Salvador Nº 305, Puerto Varas" -41.3180724 -72.9843986 "Del Salvador Nº 305, Puerto Varas")
    '("Puerto Montt Alto - Circunvalación N°232, Puerto Montt" -41.4655766 -72.9570966 "Circunvalación N°232, Puerto Montt")
    '("El Tepual - Base Aerea El Tepual" -41.439574 -73.097116 "Base Aerea El Tepual")
    '("Torre Costanera Premier - Juan Soler Manfredini 41, oficina 1601, piso 16" -41.4751693 -72.9258523 "Juan Soler Manfredini 41, oficina 1601, piso 16")
    '("Bci Home Puerto Montt - Antonio Varas Nº 560, Puerto Montt" -41.472736 -72.942532 "Antonio Varas Nº 560, Puerto Montt")
    '("Hornopirén - Lago Pinto Concha S/N" -41.8430556 -72.3175 "Lago Pinto Concha S/N")
    '("Ancud - Eleuterio Ramírez Nº 257" -41.86942852 -73.82710211 "Eleuterio Ramírez Nº 257")
    '("Castro - Gamboa Nº 397" -42.48171906 -73.76503774 "Gamboa Nº 397")
    '("Jardines del Sur - Avenida Universadad Antofagasta 02751, Local A2" -23.705814 -70.424427 "Avenida Universidad Antofagasta 02751, Local A2, Antofagasta, Chile")
    '("Avenida Brasil - Av. O'Higgins Nº 1486" -23.66171736 -70.40126485 "Av. O'Higgins Nº 1486")
    '("Mall Antofagasta - Avda. Balmaceda 2355 Local 5B y 4B 1er nivel" -23.647582 -70.401947 "Avda. Balmaceda 2355 Local 5B y 4B 1er nivel")
    '("Bci Home Antofagasta - Washington Nº 2683" -23.64601 -70.39859 "Washington Nº 2683")
    '("Antofagasta Norte - Avda. Pedro Aguirre Cerda 6259 Local 6" -23.6125876 -70.38872122 "Avda. Pedro Aguirre Cerda 6259 Local 6")
    '("San Pedro de Atacama - Vilama 425 D" -23.6024751 -70.3848722 "Vilama 425 D")
    '("Caja Auxiliar Cerro Moreno - Base Aérea Cerro Moreno" -23.439966 -70.431993 "Base Aérea Cerro Moreno")
    '("Centro Plataforma Comercial Calama - Sotomayor 2041" -22.4626918 -68.9261988 "Sotomayor 2041")
    '("Calama - Sotomayor Nº 2002" -22.46259477 -68.92580418 "Sotomayor Nº 2002")
    '("Mall Calama - Avda. Balmaceda 3242 local 115" -22.44892054 -68.92058904 "Avda. Balmaceda 3242 local 115")
    '("Chuquicamata - Av. Grau N°803, Villa Los Volcanes" -22.44438224 -68.90648874 "Av. Grau N°803, Villa Los Volcanes")
    '("Tocopilla - Arturo Prat Nº 1401, Tocopilla" -22.09375429 -70.20370281 "Arturo Prat Nº 1401, Tocopilla")
    '("Puerto Aysen - Sargento Aldea Nº 586, Puerto Aysén" -45.4043845 -72.6946926 "Sargento Aldea Nº 586, Puerto Aysén")
    '("Coyhaique - Arturo Prat Nº 387" -45.57292158 -72.07117633 "Arturo Prat Nº 387")
    '("Caja Auxiliar Los Condores - Base Aérea Los Cóndores, Iquique" -20.535278 -70.181389 "Base Aérea Los Cóndores, Iquique")
    '("Alto Hospicio - Av. La Pampa 3121 local 3,4 y 5" -20.27076064 -70.10174529 "Av. La Pampa 3121 local 3,4 y 5")
    '("Iquique Sur - Av. Arturo Prat 3068, LC1, edificio Agua Marina II" -20.24767332 -70.1383505 "Av. Arturo Prat 3068, LC1, edificio Agua Marina II")
    '("Playa Brava - Tadeo Haenke Nº 1690, Iquique" -20.2379785 -70.1439917 "Tadeo Haenke Nº 1690, Iquique")
    '("Bci Home Iquique - Tarapacá Nº 404" -20.213918 -70.151554 "Tarapacá Nº 404")
    '("Caja Auxiliar Zofri - Manzana 1 Sitio uno-A, Recinto Amurallado Zofri" -20.209051 -70.132986 "Manzana 1 Sitio uno-A, Recinto Amurallado Zofri")
    '("Zofri - Edificio Convenciones de ZOFRI s/n piso 1 loc.N°3" -20.205298 -70.140459 "Edificio Convenciones de ZOFRI s/n piso 1 loc.N°3 ")
    '("Arica - Bolognesi 221" -18.4781428 -70.320303 "Bolognesi 221")
    '("Chabunco - Base Aérea Chabunco s/n" -53.0054 -70.847682 "Base Aérea Chabunco s/n")
    '("Zona Franca Punta Arenas - Zona Franca, Lote N°5, manzana 8." -53.133057 -70.875715 "Zona Franca, Lote N°5, manzana 8.")
    '("Punta Arenas - Pdte. Errázuriz Nº 799, Punta Arenas" -53.154478 -70.916476 "Pdte. Errázuriz Nº 799, Punta Arenas")
    '("Ojo Bueno - C.General 5ª División Ejército de Chile, P. Arenas" -53.163147 -70.908662 "C.General 5ª División Ejército de Chile, P. Arenas ")
    '("Quellón - 22 de Mayo N° 343" -53.7680342 -67.7303054 "22 de Mayo N° 343")
    '("Caja Auxiliar Villa Las Estrellas - Base Teniente Marsh, Antártica Chilena" -62.195659 -58.97472 "Base Teniente Marsh, Antártica Chilena")
    '("Mall Plaza Vespucio - Froilán Roa 7107, local D 116 -120" 27.6648274 -81.5157535 "Froilán Roa 7107, local D 116 -120, La Florida")
    '("Rengo - Carlos Condell N° 57, local 1" 0 0 "Carlos Condell N° 57, local 1")
)]

[define PI 3.14159265359]
[define EARTH_R_KM 6371]
[defun deg-to-rad (deg) (/ (* deg PI) 180)]
[define distance
    (function (lat1 lon1 lat2 lon2)
        [define dLat (deg-to-rad (- lat2 lat1))]
        [define dLon (deg-to-rad (- lon2 lon1))]
        [define radLat1 (deg-to-rad lat1)]
        [define radLat2 (deg-to-rad lat2)]
        [define a
            (+
                (*
                    (sin (/ dLat 2))
                    (sin (/ dLat 2))
                )
                (*
                    (* [sin (/ dLon 2)] [sin (/ dLon 2)])
                    (* [cos radLat1] [cos radLat2])
                )
            )
        ]
        [define c (* 2 (atan2 [sqrt a] [sqrt (- 1 a)]))]
        (* EARTH_R_KM c)
    )
]

[define log-nodes-trace
    (function (nodes-path)
        (list)
    )
]

[define add-step
    (function (data step-id)
        [define nodes-path (get data "nodes-path")]
        (put data "nodes-path" (extend nodes-path step-id))
    )
]

[define pop-step
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (put data "nodes-path" (init nodes-path))
    )
]

[define reset-path
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (put data "nodes-path" (list))
    )
]

[define log-path
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (log-nodes-trace nodes-path)
    )
]

[define derive-ticket
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (log-nodes-trace nodes-path)
        (log-event (append (join "_" nodes-path) "_DERIVED"))
        (log-derive-ticket (get data "ticket-open-time"))
        (terminal-node "ASSIGN_TO_CM")
    )
]

[define close-ticket
    (function (data)
        (log-path data)
        (terminal-node "CLOSE_TICKET")
    )
]

[defun format-quick-replies (first-message quick-replies)
    (make-dict (list
        (cons "text" first-message)
        (list "quick_replies"
            (map
                (function (r)
                    (make-dict (list
                        (cons "content_type" "text")
                        (cons "title" r)
                        (cons "payload" r)
                    ))
                )
                quick-replies
            )
        )
    ))
]

[defun format-quick-replies-with-images (first-message quick-replies)
    (make-dict (list
        (cons "text" first-message)
        (list "quick_replies"
            (map
                (function (r)
                    (make-dict (list
                        (cons "content_type" "text")
                        (cons "title" (get r 0))
                        (cons "payload" (get r 0))
                        (cons "image_url" (get r 1))
                    ))
                )
                quick-replies
            )
        )
    ))
]

[defun ask-location (message)
    (make-dict (list
        (cons "text" message)
        (list "quick_replies"
            (list
                (make-dict (list
                    (cons "content_type" "location")
                ))
            )
        )
    ))
]

[define format-image
    (function (image-url)
        (make-dict (list
            (cons "attachment"
                (make-dict (list
                    (cons "type" "image")
                    (cons "payload" (make-dict (list
                        (cons "url" image-url)
                        (cons "is_reusable" #t)
                    )))
                ))
            )
        ))
    )
]

[define format-location
    (function (info)
        [define name (get info 0)]
        [define latitude (str (get info 1))]
        [define longitude (str (get info 2))]
        [define address (get info 3)]
        [define map-img-url (append
            "https://maps.googleapis.com/maps/api/staticmap?size=640x336&maptype=roadmap&markers="
            latitude "," longitude
        )]
        [define gmaps-url (append
            "https://www.google.cl/maps/search/"
            latitude "," longitude
        )]
        (make-dict (list
            (cons "attachment"
                (make-dict (list
                    (cons "type" "template")
                    (cons "payload"
                        (make-dict (list
                            (cons "template_type" "generic")
                            (list "elements" (list
                                (make-dict (list
                                    (cons "title" name)
                                    (cons "subtitle" address)
                                    (cons "image_url" map-img-url)
                                    (list "buttons" (list
                                        (make-dict (list
                                            (cons "type" "web_url")
                                            (cons "url" gmaps-url)
                                            (cons "title" "Abrir Mapa")
                                            (cons "webview_height_ratio" "full")
                                        ))
                                    ))
                                ))
                            ))
                        ))
                    )
                ))
            )
        ))
    )
]

(define THUMBS_UP_EMOJI
    "https://emojipedia-us.s3.amazonaws.com/thumbs/160/facebook/65/thumbs-up-sign_1f44d.png"
)
(define THUMBS_DOWN_EMOJI
    "https://emojipedia-us.s3.amazonaws.com/thumbs/160/facebook/65/thumbs-down-sign_1f44e.png"
)

[define was-answer-useful-msg
    (function (data)
        (format-quick-replies-with-images
            (translate data "TE_SIRVIO?")
            (list
                (list "Sí" THUMBS_UP_EMOJI)
                (list "No" THUMBS_DOWN_EMOJI)
            )
        )
    )
]

[define answer-useful-response-node
    (bot-node (data)
        [define response (plain (input-message))]
        (cond
            [(match? "(no)|(nada)" response)
                (node-result
                    (no-entendi-reset data)
                    (list
                        (translate data "DESPEDIDA_NEGATIVA")
                    )
                    (begin
                        (log-event "TERMINO_INSATISFECHO")
                        (close-ticket data)
                    )
                )
            ]
            [else
                (node-result
                    (no-entendi-reset data)
                    (list
                        (translate data "DESPEDIDA")
                    )
                    (begin
                        (close-ticket data)
                    )
                )
            ]
        )
    )
]

[define was-answer-useful?
    (function (data)
        (node-result
            data
            (was-answer-useful-msg data)
            answer-useful-response-node
        )
    ) 
]

[define back-to-menu?-response-node
    (bot-node (data)
        [define response (plain (input-message))]
        (cond
            [(match? "(si\s?.*)|(afirmativo)" response)
                (begin
                    (log-path data)
                    (node-result
                        (no-entendi-reset (reset-path data))
                        (list
                            (translate data "QUE_OTRA_COSA_NECESITAS?")
                            (entry-menu data)
                        )
                        entry-menu-response-node
                    )
                )
            ]
            [(match? "(no)|(nada)" response)
                (was-answer-useful? data)
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "NO_ENTENDI") (back-to-menu-msg data))
                    back-to-menu?-response-node
                )
            ]
        )
    )
]

[defun back-to-menu-msg (data)
    (format-quick-replies
        (translate data "ALGO_MAS?")
        (list "Sí" "No")
    )
]

[define back-to-menu?
    (function (data previous-messages)
        (node-result
            data
            (extend
                previous-messages
                (back-to-menu-msg data)
            )
            back-to-menu?-response-node
        )
    ) 
]

[define closest-atm
    (function (latitude longitude)
        [define distances
            (map
                (function (p)
                    (list
                        (distance latitude longitude (get p 1) (get p 2))
                        p
                    )
                )
                cajeros
            )
        ]
        [define min-distance (min (map (function (d) (get d 0)) distances))]
        [define closest
            (get
                (filter (function (p) (= min-distance (get p 0))) distances)
                0
            )
        ]
        (format-location (get closest 1))
    )
]

[define cajeros-response-node
    (bot-node (data)
        [define msg (input-message)]
        (cond
            [(equal? "__LOCATION__" msg)
                (begin
                    [define coords (get data "location")]
                    [define latitude (get coords "lat")]
                    [define longitude (get coords "long")]
                    (back-to-menu?
                        data 
                        (list
                            (translate data "CAJERO_MAS_CERCANO")
                            (closest-atm latitude longitude)
                        )
                    )
                )
            ]
            [else
                (node-result
                    data
                    (ask-location (translate data "ENVIAME_TU_UBICACION"))
                    cajeros-response-node
                )
            ]
        )
    )
]

[define block-card-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? ".*credito.*" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "CREDITO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "BLOQUEAR_CREDITO_PASO_1")
                        (translate data "BLOQUEAR_CREDITO_PASO_2")
                        (translate data "BLOQUEAR_CREDITO_PASO_3")
                        (format-image (translate data "BLOQUEAR_CREDITO_IMAGEN"))
                        (translate data "BLOQUEAR_CREDITO_PASO_4")
                        (translate data "BLOQUEAR_CREDITO_PASO_5")
                        (translate data "BLOQUEAR_CREDITO_PASO_6")
                    )
                )
            ]
            [(match? ".*debito.*" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "DEBITO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "BLOQUEAR_DEBITO_PASO_1")
                        (translate data "BLOQUEAR_DEBITO_PASO_2")
                        (translate data "BLOQUEAR_DEBITO_PASO_3")
                    )
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "OPCION_INVALIDA") (tarjeta-a-bloquear? data))
                    block-card-node
                )
            ]
        )
    )
]

[defun tarjeta-a-bloquear? (data)
    (format-quick-replies
        (translate data "TARJETA_A_BLOQUEAR?")
        (list "T. Crédito" "T. Débito")
    )
]

[define emergencies-response-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? "(.*desbloque.*)|(.*clave.*)" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "CLAVE"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "INGRESAR_A_BANCO_EN_LINEA")
                        (format-image (translate data "BANCO_EN_LINEA_IMAGEN"))
                        (translate data "INGRESA_DATOS_SIGUE_PASOS")
                    )
                )
            ]
            [(match? ".*tarjeta.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "TARJETA"))
                    (tarjeta-a-bloquear? data)
                    block-card-node
                )
            ]
            [(match? "(.*auto.*)|(.*siniestro.*)" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "AUTO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "SINIESTRO_AUTO_PASO_1_TITULO")
                        (translate data "SINIESTRO_AUTO_PASO_1_CUERPO")
                        (translate data "SINIESTRO_AUTO_PASO_1_CUERPO2")
                        (translate data "SINIESTRO_AUTO_PASO_2_TITULO")
                        (translate data "SINIESTRO_AUTO_PASO_2_CUERPO1")
                        (translate data "SINIESTRO_AUTO_PASO_2_CUERPO2")
                    )
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list
                        (translate data "NO_ENTENDI")
                        (emergencies-menu (translate data "EMERGENCIAS_MANEJADAS") data)
                    )
                    emergencies-response-node
                )
            ]
        )
    )
]

[define emergencies-menu
    (function (heading data)
        (list
            heading
            "DESBLOQUEO_CLAVE"
            "BLOQUEO_TARJETA"
            "SINIESTRO_AUTOMOTRIZ"
        )
    )
]

[define cuenta-response-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? "(si)|(afirmativo)|(claro)|(exacto)" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "OTRO-BANCO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "CUENTA_CLIENTE_OTRO_BANCO_1")
                        (translate data "CUENTA_CLIENTE_OTRO_BANCO_2")
                        (translate data "CUENTA_CLIENTE_OTRO_BANCO_3")
                    )
                )
            ]
            [(match? "(no)|(negativo)|(nones)" msg)
                (node-result
                    (no-entendi-reset (add-step data "BCI"))
                    (translate data "CUENTA_CLIENTE_BCI")
                    (derive-ticket data)
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "NO_ENTENDI") (cuenta-menu data))
                    cuenta-response-node
                )
            ]
        )
    )
]

[defun cuenta-menu (data)
    (format-quick-replies
        (translate data "CLIENTE_OTRO_BANCO?")
        (list "Sí" "No")
    )
]

[define entry-menu-response-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? ".*emergencia.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "EMERGENCIA"))
                    (emergencies-menu (translate data "EMERGENCIAS_CABECERA") data)
                    emergencies-response-node
                )
            ]
            [(match? ".*cajero.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "CAJERO"))
                    (ask-location (translate data "ENVIAME_TU_UBICACION"))
                    cajeros-response-node
                )
            ]
            [(match? ".*cuenta.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "CUENTA"))
                    (cuenta-menu data)
                    cuenta-response-node
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "NO_ENTENDI") (entry-menu data))
                    entry-menu-response-node
                )
            ]
        )
    )
]

[defun no-entendi-reset (data) (put data "NO_ENTENDI_COUNTER" 0)]

[define NO_ENTENDI_RETRY_LIMIT 1]

[define no-entendi-node
    (function (data messages next-node)
        (define no-entendi-counter (get data "NO_ENTENDI_COUNTER"))
        (if (>= no-entendi-counter NO_ENTENDI_RETRY_LIMIT)
            (node-result
                data
                (translate data "EJECUTIVO_TE_CONTACTARA")
                (derive-ticket data)
            )
            (node-result
                (put data "NO_ENTENDI_COUNTER" (+ no-entendi-counter 1))
                messages
                next-node
            )
        )
    )
]

[define entry-menu
    (function (data)
        (make-dict (list
            (cons "attachment"
                (make-dict (list
                    (cons "type" "template")
                    (cons "payload"
                        (make-dict (list
                            (cons "template_type" "generic")
                            (list "elements" (list
                                (make-dict (list
                                    (cons "title" (translate data "MENU_ENTRADA_TITULO"))
                                    (cons "image_url" (translate data "MENU_ENTRADA_IMAGEN"))
                                    (list "buttons" (list
                                        (make-dict (list
                                            (cons "title" (translate data "MENU_ENTRADA_EMERGENCIAS"))
                                            (cons "type" "postback")
                                            (cons "payload" "emergencias")
                                        ))
                                        (make-dict (list
                                            (cons "title" (translate data "MENU_ENTRADA_CAJEROS"))
                                            (cons "type" "postback")
                                            (cons "payload" "cajeros")
                                        ))
                                        (make-dict (list
                                            (cons "title" (translate data "MENU_ENTRADA_CUENTA"))
                                            (cons "type" "postback")
                                            (cons "payload" "cuenta")
                                        ))
                                    ))
                                ))
                            ))
                        ))
                    )
                ))
            )
        ))
    )
]

[defun translate (data identifier) identifier] 

[define entry-node
    (bot-node (input-data)
        [define data
            (put
                (no-entendi-reset input-data)
                "nodes-path"
                (list)
            )
        ]
        [define msg (input-message)]
        (cond
            [(match? ".*emergencia.*" msg)
                (node-result
                    (add-step data "EMERGENCIA")
                    (emergencies-menu (translate data "EMERGENCIAS_CABECERA") data)
                    emergencies-response-node
                )
            ]
            [(match? ".*cajero.*" msg)
                (node-result
                    (add-step data "CAJERO")
                    (ask-location (translate data "ENVIAME_TU_UBICACION"))
                    cajeros-response-node
                )
            ]
            [(match? ".*cuenta.*" msg)
                (node-result
                    (add-step data "CUENTA")
                    (cuenta-menu data)
                    cuenta-response-node
                )
            ]
            [else
                (node-result
                    data
                    (list
                        (translate data "ENTRY_MESSAGE")
                        (entry-menu data)
                    )
                    entry-menu-response-node
                ) 
            ]
        )
    )
]

entry-node"""