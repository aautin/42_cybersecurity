# VM Setup and Work Summary for `ft_onion` Branch

## 🖥️ Environment
- Ubuntu 22.04 LTS
- VM hosted on VirtualBox
- Local only, not pushed to GitHub

## 🔧 Steps Performed On VM
1. Initialized the VM
	Operating System: Debian GNU/Linux 12
	Hard Disk: 20GB

2. Add host to sudoers
	```su```
	```sudo adduser HOSTNAME sudo```

3. Installed NGINX and SSH
	```sudo apt install nginx``` <- listen on port 80 by default
	```sudo apt install ssh``` <- listen on port 22 by default

4. Set SSH on port 4242
	```sudo nano /etc/ssh/sshd_config```
	Found ``` #Port 22 ``` and modified to ```Port 4242```
	Verify result with ```sudo ss -tuln```
