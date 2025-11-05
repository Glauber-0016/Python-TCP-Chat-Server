# Python TCP Chat Server

Este projeto implementa um simples chat multi-cliente e multi-salas usando sockets TCP em Python. Ele é composto por dois scripts principais:

* `TCPServer.py`: O script do servidor que gerencia conexões, salas e a distribuição de mensagens.
* `TCPClient.py`: O script do cliente que permite aos usuários se conectarem ao servidor, entrarem em salas e trocarem mensagens.

* **Chat Multi-Cliente:** O servidor utiliza *threading* para lidar com múltiplos clientes simultaneamente.
* **Salas de Chat:** Os usuários podem criar e entrar em diferentes salas usando o comando `/join #nome_da_sala`.
* **Criação Dinâmica de Salas:** As salas são criadas automaticamente quando o primeiro usuário entra e são removidas quando o último usuário sai.
* **Comandos Básicos:** Suporta comandos como `/join`, `/exit` e `/quit`.

## Requisitos

* Python 3.x
* Duas máquinas na mesma rede local (física ou virtual).
* Permissões de administrador (para editar arquivos de configuração de rede, se necessário).

## Configuração e Execução

Para conectar duas máquinas na mesma rede, você precisar configurar um IP estático na máquina do servidor, para que o cliente saiba exatamente para qual endereço IP se conectar.

### Passo 1: Configuração de Rede (Máquina Servidor)

As instruções abaixo são um exemplo para sistemas baseados em Debian (como Debian, Ubuntu antigo) que usam o arquivo `/etc/network/interfaces`.

1.  **Encontre sua interface de rede:**
    Use o comando `ip a` ou `ifconfig` para descobrir o nome da sua interface de rede (ex: `eth0`, `enp0s3`).

2.  **Defina um IP Estático:**
    Abra o arquivo de configuração de interfaces com um editor de texto:
    ```bash
    sudo nano /etc/network/interfaces
    ```

3.  **Adicione a configuração:**
    Adicione as seguintes linhas ao final do arquivo, substituindo `[nome_da_interface]` pelo nome da sua interface e escolhendo um IP para seu servidor (ex: `192.168.0.1`).

    ```
    # Configuração de IP Estático para o Servidor de Chat
    auto [nome_da_interface]
    iface [nome_da_interface] inet static
        address 192.168.0.1
        netmask 255.255.255.0
        # gateway 192.168.0.1  <-- Adicione se precisar de acesso à internet/roteador
    ```

4.  **Reinicie o serviço de rede:**
    Salve o arquivo e reinicie o serviço para que as alterações tenham efeito.
    ```bash
    sudo /etc/init.d/networking restart
    ```

### Passo 2: Executando o Servidor

1.  Na máquina **servidor** (a que você acabou de configurar com o IP `192.168.0.1`), navegue até a pasta onde o script está.
2.  Execute o servidor:
    ```bash
    python3 TCPServer.py
    ```
### Passo 3: Executando o Cliente

1.  Vá para a máquina **cliente**. Certifique-se de que ela está na mesma rede (ex: com um IP como `192.168.0.2`, que você vai configurar da mesma forma que fez no passo 1
2.  Navegue até a pasta onde o script está.
3.  Execute o cliente:
    ```bash
    python3 TCPClient.py
    ```


## Como Usar o Chat

1.  **Conectar:** Siga o "Passo 3" acima.
2.  **Entrar em uma Sala:** Você deve entrar em uma sala para enviar mensagens.
    ```
    > /join #geral
    ```
3.  **Conversar:** Qualquer texto que não comece com `/`.
    ```
    > Olá, mundo!
    ```
4.  **Sair:** Para desconectar do servidor, digite:
    ```
    > /exit
    ```
    (ou `/quit`)
