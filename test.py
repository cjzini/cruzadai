from cruzada.control import Gerador
from config import *
import google.generativeai as genai


# Por questões de seguranca, a API_KEY está armazenada em arquivo sem ser enviado para o GitHub
genai.configure(api_key=API_KEY)




#Gerar testes
gerador = Gerador('/uploads/cruzada1.txt')
gerador.gera_quadro()