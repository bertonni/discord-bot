import discord
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração do bot
TOKEN = 'SEU_DISCORD_TOKEN'
client = discord.Client(intents=discord.Intents.default())

# Configuração do e-mail
EMAIL = "seuemail@gmail.com"
PASSWORD = "suasenha"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Função para enviar e-mail
def send_email(to_email, subject, body):
    try:
        # Configuração do e-mail
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectar ao servidor SMTP e enviar o e-mail
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# Evento de inicialização do bot
@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}!')

# Evento para receber mensagens
@client.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == client.user:
        return
    
    # Comando para enviar e-mail
    if message.content.startswith("!enviar_email"):
        try:
            # Pega parâmetros do comando
            _, email_destino, assunto, conteudo = message.content.split("|", 3)
            email_enviado = send_email(email_destino.strip(), assunto.strip(), conteudo.strip())
            
            # Retorna resposta no Discord
            if email_enviado:
                await message.channel.send("E-mail enviado com sucesso!")
            else:
                await message.channel.send("Erro ao enviar o e-mail.")
        except Exception as e:
            await message.channel.send(f"Erro no comando: {e}")

client.run(TOKEN)
