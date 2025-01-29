#! python3.10

# Importa a class "datetime" do módulo "datetime" para manipulação de data e tempo
from datetime import datetime

# Importa o módulo para ter a função de dar uma pausa na execução do programa por um determinado tempo
import time

# Importa o módulo que permiti que o programa controle o mouse e teclado
import pyautogui

# Importa as classes "run", responsável para executar comandos no terminal, e "PIPE", que armazena a saída e entrada do comando do terminal, do módulo "subprocess"
from subprocess import run, PIPE

# Variável que armazena o atalho das imagens utilizadas para automação
pasta = '/home/usuario/Documents/Luiz2023/Automacao/'

# Variável para armazenar o atalho de onde serão salvos os prints de tela
atalho = '/home/usuario/Downloads/'

# Variável para armazernar uma lista de prints realizado no dia
contlista = []

# Variável para armazenar lista com o número de série das impressoras
imp = ['ZEQYBQAF4000CFW', 'ZEQYBQAF5001FLM', 'ZDDPB07K110ZF4Y', 'ZEQYBQAF6001RZL', 'ZDDPB07MA174KBW', '6TB443854']

# Variável para armazenar a data formatada: %dia%mês%ano (somente 2 dígitos do ano)
data = datetime.now().strftime('%d%m%y')

# Função para confirmar se imagem que está salva é a mesma que está sendo exibida na tela do computador
def verificar(caminho, imgs = [], click = False, vel = 0):

	# Variável responsável para manter o loop até satisfeita condição
	continua = True

	# Enquanto a variável for verdadeira, continua o loop
	while continua:

		# Loop para verificar se alguma das imagens passada é exibida na tela do computador
		for i in range(len(imgs)):
			try:
				# Caso seja localizada a mesma imagem do arquivo na tela do computador, a variável armazena as coordenadas encontradas x (largura), y (altura)
				temp = pyautogui.locateOnScreen(caminho + imgs[i], grayscale=True)

				# Muda valor da variável para sair do loop, uma vez localizada a imagem na tela do computador
				continua = False

				# Se a variável clicar for verdadeira, simula o click do mouse nas cooerdenadas da imagem localizada (clica no centro da imagem)
				if click:

					# Realiza uma pausa para ter tempo de ser exibido na tela do computador a consulta com a imagem de onde será realizado o click do mouse
					time.sleep(vel)

					# Clica nas coordenadas indicada
					pyautogui.click(temp)

				# Retorno da função com o posição das imagens passada, a que foi localizada na tela do computador
				return i

			# Caso alguma imagem não seja localiza, mantém a variável de loop com o valor positivo
			except:

				# Essa linha não influencia em nada mas é necessária, pois o "except" não aceita ficar em branco sem ação
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
