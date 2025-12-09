import os
from fakepinterest import app

# Verificando se está rodando ONLINE com uma variável de ambiente
IS_ONLINE = os.getenv("IS_ONLINE", "false").lower() == "true"

if __name__ == '__main__':
    app.run(debug=IS_ONLINE)
