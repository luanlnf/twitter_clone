# 🐦 Twitter Clone (Projeto Django)

Clone simples do Twitter desenvolvido com **Django** para fins educacionais.  
O projeto implementa autenticação, criação de tweets, seguidores, perfis com foto e muito mais.

---

## 🚀 Funcionalidades

- Registro, login e logout  
- Criar, editar e excluir tweets  
- Curtir e descurtir tweets  
- Feed exibindo tweets de quem você segue  
- Perfis com:
  - Foto de perfil
  - Bio
  - Nome e email
- Sistema de seguir / deixar de seguir usuários  
- Upload de imagens (media)  

---

## 📦 Tecnologias utilizadas

- Python 3.10+  
- Django 3+  
- HTML / CSS  
- Banco SQLite (local) e MySQL (deploy)  
- PythonAnywhere para deploy  
- Git e GitHub  

---

## 📁 Estrutura do projeto
twitter_clone/
├─ setup/
├─ twitter/
│ ├─ templates/
│ ├─ static/
│ └─ models.py, views.py, urls.py
├─ media/
├─ staticfiles/
├─ manage.py
├─ requirements.txt
---

# 🖥️ Como rodar o projeto localmente

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/luanlnf/twitter_clone.git
cd twitter_clone
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 
````
MIT License — livre para estudar, modificar e distribuir.

