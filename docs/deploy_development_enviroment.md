# TIM Tec > Develop Mode

Se você quer desenvolver features para ferramenta timtec ou ainda resolver bugfixes, o primeiro passo é criar um ambiente adequado para isso. 

## Vagrant Local install
O primeiro passo recomendado é fazer uma instalação local. Recomendamos usar uma máquina virtual via commandline para isso, com Vagrant. Se você não quiser usar Vagrant, faça uma instalação de outra forma e siga para o próximo passo. 

1. Instale o vagrant e o virtualbox na sua máquina
2. Crie um diretório para hospedar uma máquina ubuntu 16.04: sugestão de nome ```2017_06_vagrant_ubuntu_16_04_timtec```
Ex.: de execução:
```
user@server$ mkdir vagrant_ubuntu_16_04_timtec
user@server$ vagrant init ubuntu/xenial64; vagrant up --provider virtualbox
```
3. Clone o repositório dentro desta pasta:
```
user@server/vagrant_ubuntu_16_04_timtec$ git clone https://github.com/institutotim/timtec.git
```
Exemplo de como ficará seu diretório:
![selecao_028](https://user-images.githubusercontent.com/641411/27146350-7d277e0c-510f-11e7-8f6e-ddd3316b9d11.png)

4. Entre no arquivo Vagrantfile criado pelo Vagrant e edite a linha de pastas syncadas. Acrescente na opção synced_folder a pasta padrão do timtec. Ficará mais ou menos desta forma dependendo de onde você tenha feito o clone do repo:

```
  config.vm.synced_folder "timtec", "/home/timtec-development/timtec",
  owner: "timtec-development", group: "timtec-development"
```
Sugerimos que use o user ```timtec-development``` para o ambiente de desenvolvimento, por isso esse seria o nome do diretório do user da aplicação. Mas isso é totalmente opcional. 

5. Edite também o redirecionamento de portas do guest para o host. Deixe no host algo como 3131, ou qualquer outra porta alta sem uso. 

```
  config.vm.network "forwarded_port", guest: 80, host: 3131
```

Uma vez que você tenha clonado o repo do timtec dentro de um diretório vagrant ele irá aparecer na pasta /vagrant/timtec quando estiveres logado, certo? O que a linha acima faz é linkar isso com a pasta home do usuário da aplicação, no caso ```/home/timtec-development/timtec```. 

6. Prossiga com o procedimento de deploy normal da aplicação dentro do Vagrant, isto é, entre no vagrant com ```vagrant ssh```, vire root com ```sudo su``` e execute os passos necessários como root, incluindo a criação de um user, que nesse caso ao contrário do que recomendado na documentação padrão do timtec, sugerimos que seja ```timtec-development```. 


## Ative o env


source env/bin/activate


## Runserver
O Django possui um servidor livein para desenvolvimento. Ao rodar esse servidor a aplicação fica em modo "watch" permitindo com que toda e qualquer alteração gere um logo ao vivo no terminal de comandos. Para ativar o ```runserver``` junto com vagrant no timtec, você seguir o exemplo abaixo:

```
./timtec/manage.py runserver 0.0.0.0:8000
```













