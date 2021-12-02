# twitter_bot
Python Twitter bot POC 

Recibe por parametro codigos de divisas (ie ars, usd, etc), busca esos valores en bitso cada x T y twittea cada y T en https://twitter.com/julian_bitgalea

Para correrlo, con python3 instalado, desde una terminal: 

#Clonar el repo
git clone https://github.com/julian-bitgalea/twitter_bot.git;

#Meterse en el directorio donde estan los archivos
cd twitter_bot;

#(Buena practica de python, crear un entorno virtual donde instalar las dependencias y ejecutar el script)
python3 -m venv environment; 
source environment/bin/activate;

#Instalar dependencias
pip install -r requirements.txt;

#Uncommentear la linea 140 (es la linea que manda el/los twits. Esta comentada para evitar spammiar)

#Ejecutar 
python twitter_bot.py --help;
python twitter_bot.py --fiat_codes ars eur usd cad;
