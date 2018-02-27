#installer python3-usb
#Ajout  dans /lib/udev/rules.d/999-local-permissions.rules
#SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0777"
# SUBSYSTEMS=="usb" ATTRS{idVendor}=="08ff" ATTRS{idProduct}=="0009" MODE:="0777" SYMLINK+="RFID reader"
#recharger les règles udev :
#sudo udevadm control --reload-rules
#Débrancher et rebrancher le lecteur

#Dans le dossier, rien à installer
from keyboard_alike import reader

#installer python3-selenium et le driver selenium chromium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#installer vlc, mais le binding python est dans le dossier pas besoin de l'installer
import vlc

class RFIDReader(reader.Reader):
    """
    """
    pass

BASE_URL = "http://192.168.1.36/index.php/Login/"
driver = ''

def navigate_to(url):
	global driver
	try:
		driver.get(url)
	except :
		#browser is closed
		create_driver()
		driver.get(url)
	
		
def create_driver():
	chrome_options = webdriver.ChromeOptions();
	chrome_options.add_argument("--kiosk")
	global driver 
	driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)		

if __name__ == "__main__":
	player_scanner = vlc.MediaPlayer("file:///home/habemus/Documents/pyring/scanner_sweep.mp3")
	player_error = 	vlc.MediaPlayer("file:///home/habemus/Documents/pyring/beep_error.mp3")
	reader = RFIDReader(0x13ba, 0x18, 8, 10, should_reset=False, debug=False)
	reader.initialize()
	create_driver()
	navigate_to(BASE_URL + "/show_login_ring")
	while True:
		data = reader.read().strip()
		#On enlève tout ce qui est après un éventuel \n pour limiter la casse sur la lecture
	 	#si on passe trop vite sur le lecteur
		#Normalement obsolète depuis le rework de keyboard alike, mais on garde au cas ou ...
		data =  data.split("\n")[0]
		#On enlève les leading 0 et on en rajoute 3, parce qu'on en a pas toujours le même nombre
		data = data.lstrip("0")
		data = "000"+data;
		if len(data) != 10:
			print("Erreur de lecture : taille de données incorrecte : " + str(len(data)))
			player_error.stop()
			player_error.play()	
			count_sound = count_sound + 1;
		else:
			player_scanner.stop()
			player_scanner.play()
			url = BASE_URL + "log_in_ring/" + str(data)
			navigate_to(url)


