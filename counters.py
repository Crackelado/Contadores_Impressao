#! python3.10

from datetime import datetime
import time
import pyautogui
from subprocess import run, PIPE
pasta = '/home/usuario/Documents/Luiz2023/Automacao/'
atalho = '/home/usuario/Downloads/'
contlista = []
imp = ['ZEQYBQAF4000CFW', 'ZEQYBQAF5001FLM', 'ZDDPB07K110ZF4Y', 'ZEQYBQAF6001RZL', 'ZDDPB07MA174KBW', '6TB443854']
data = datetime.now().strftime('%d%m%y')

def verificar(caminho, imgs = [], click = False, vel = 0):
	continua = True

	while continua:
		for i in range(len(imgs)):
			try:
				temp = pyautogui.locateOnScreen(caminho + imgs[i], grayscale=True)
				continua = False

				if click:
					time.sleep(vel)
					pyautogui.click(temp)

				return i
			except:
				continua = True

def contadores(IP, impressora, numero):
	pyautogui.PAUSE = 1
	action = 0
	run(['/usr/bin/google-chrome-stable', IP])
	opcao = verificar(pasta, ['information.png', 'logoxerox.png', 'reload.png'])

	if opcao != 2:
		
		if opcao == 0:
			verificar(pasta, ['information.png'], True, 2)

		if impressora == '6TB443854':
			if verificar(pasta, ['badvanced.png', 'logoxerox.png']) == 0:
				verificar(pasta, ['badvanced.png'], True)
				verificar(pasta, ['proceed.png'], True)

			verificar(pasta, ['logoxerox.png'])
			pyautogui.click(pyautogui.size().width - 6, pyautogui.size().height / 2 + 200)
			verificar(pasta, ['busage.png'], True)
			verificar(pasta, ['refresh.png'])
			action = 2

		if action < 2:
			verificar(pasta, ['counters.png'], True, 1)

		temp = atalho + impressora + '_' + datetime.now().strftime('%d%m%y%H%M%S') + '_' + numero + '.png'
		contlista.append(temp)
		time.sleep(1)
		img = pyautogui.screenshot(region=(0, int(pyautogui.size()[1] * 0.04), pyautogui.size()[0], int(pyautogui.size()[1] * 0.935)))
		img.save(temp)

	verificar(pasta, ['information.png', 'refresh.png', 'reload.png'])
	pyautogui.hotkey('ctrl', 'w')

lista = run(['ls', '-t', atalho], stderr=PIPE, stdout=PIPE)
lista = lista.stdout.decode('utf-8').split('\n')
lista = ''.join([s[-5] for s in lista if data in s])
lista = [s for s in '234567' if s not in lista]

if len(lista) > 0:
	for a in lista:
		contadores('10.150.200.20' + a, imp[int(a) - 2], a)

	for i in contlista:
		run(['/usr/bin/google-chrome-stable', '--incognito', i])
