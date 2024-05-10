from cruzada.control import Gerador
from config import *
import google.generativeai as genai

genai.configure(api_key=API_KEY)
#Gerar testes
gerador = Gerador('/uploads/cruzada1.txt')
gerador.gera_quadro()