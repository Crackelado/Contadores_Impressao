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

# Variável array para armazenar lista com o número de série das impressoras
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

# Função para salvar print da tela com a quantidade de impressões realizadas
def contadores(IP, impressora, numero):

	# Acrescenta um atraso na execução de cada comando do módulo "pyautogui"
	pyautogui.PAUSE = 1

	# Variável responsável para diferenciar tela de configuração das impressora
	# Das 6 impressoras somente uma é diferente a tela de consulta
	action = 0

	# Abre o navegador "Google Chrome" no endereço da impressora
	run(['/usr/bin/google-chrome-stable', IP])

	# Variável que executa "IF" caso não seja imagem "reload.png" (imagem mostrada quando impressora está offline)
	opcao = verificar(pasta, ['information.png', 'logoxerox.png', 'reload.png'])

	# Executa ação caso variável "opcao" seja diferente de 2
	if opcao != 2:

		# Caso encontre imagem "information.png" (presente na consulta de 5 impressoras) executa a ação de clicar no botão
		if opcao == 0:
			verificar(pasta, ['information.png'], True, 2)

		# Caso a impressora com número de série específica seja chamada, executar comandos de diferem das demais
		if impressora == '6TB443854':

			# Pesquisa se algumas das 2 imagens está sendo exibida na tela do computador
			if verificar(pasta, ['badvanced.png', 'logoxerox.png']) == 0:

				# Clica nas opçãos para prosseguir
				verificar(pasta, ['badvanced.png'], True)
				verificar(pasta, ['proceed.png'], True)

			# Verifica se imagem "logoxerox.png" é localizada na tela do computador, caso contrário não executa os próximos comandos
			verificar(pasta, ['logoxerox.png'])

			# Clica na barra de rolagem para descer uma página
			pyautogui.click(pyautogui.size().width - 6, pyautogui.size().height / 2 + 200)

			# Clica na opção para prosseguir
			verificar(pasta, ['busage.png'], True)

			# Verifica se imagem "refresh.png" é localizada na tela do computador, caso contrário não executa os próximos comandos
			verificar(pasta, ['refresh.png'])

			# Mudar valor da variável
			action = 2

		# Executa ação se a variável for menor que 2
		if action < 2:

			# Clica na opção exibida na tela do computador
			verificar(pasta, ['counters.png'], True, 1)

		# Cria variável temporária para armazenar atalho de onde será salvo o arquivo com: pasta + nome impressora + _ data e hora (%dia%mês%ano(2 dígitos)%hora%minutos%segundos) + _ último número do ip + png
		temp = atalho + impressora + '_' + datetime.now().strftime('%d%m%y%H%M%S') + '_' + numero + '.png'

		# Preenche a lista de prints salvos
		contlista.append(temp)

		# Realiza uma pausa de 1 segundo para que os dados apareçam corretamente na tela do computador antes do print
		time.sleep(1)

		# Realiza a captura da tela do computador, começando abaixo da barra de endereços e acima da barra de tarefas
		img = pyautogui.screenshot(region=(0, int(pyautogui.size()[1] * 0.04), pyautogui.size()[0], int(pyautogui.size()[1] * 0.935)))

		# Salva o print no local designado pela variável
		img.save(temp)

	# Confirma se há na tela do computador alguma da imagens para continuar o código
	verificar(pasta, ['information.png', 'refresh.png', 'reload.png'])

	# Executa o atalho do teclado (ctrl+w) para fechar aba aberta
	pyautogui.hotkey('ctrl', 'w')

# Realiza uma consulta de terminal, na pasta onde foram salvas as imagens, e joga saída para variável
lista = run(['ls', '-t', atalho], stderr=PIPE, stdout=PIPE)

# Converte os dados da pesquisa em texto e transforma em um array, com o indicador de quebra de linha como final do texto
lista = lista.stdout.decode('utf-8').split('\n')

# Realiza um loop para pegar somente o final do ip, que foi acresentado ao arquivo antes de salvar
# Somente das imagens salvas na data atual a execução do script
lista = ''.join([s[-5] for s in lista if data in s])

# Loop para criar lista somente dos prints que ainda não foram realizados no dia
lista = [s for s in '234567' if s not in lista]

# Somente entra na condição se a quantidade de prints que não foram encontrados no dia for maior que zero
if len(lista) > 0:

	# Loop para percorrer lista de prints a realizar e gerar arquivos
	for a in lista:
		contadores('10.150.200.20' + a, imp[int(a) - 2], a)

	# Loop para abrir prints salvos no Google Chrome e exibir na tela do computador (Obs.: pode ser utilizado com outro programa)
	for i in contlista:
		run(['/usr/bin/google-chrome-stable', '--incognito', i])
