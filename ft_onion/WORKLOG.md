# VM Setup and Work Summary for `ft_onion` Branch

## 🖥️ Environment
- Ubuntu 22.04 LTS
- VM hosted on VirtualBox
- Local only, not pushed to GitHub

## 🔧 Steps Performed On VM
1. Initialize the VM
	Operating System: Debian GNU/Linux 12
	Hard Disk: 20GB

2. Add host to sudoers
	```su```
	```sudo adduser HOSTNAME sudo```

3. Install NGINX and SSH
	```sudo apt install nginx``` <- listen on port 80 by default
	```sudo apt install ssh``` <- listen on port 22 by default

4. Set SSH on port 4242
	```sudo nano /etc/ssh/sshd_config```
	Find ``` #Port 22 ``` and modify to ```Port 4242```
	Verify result with ```sudo ss -tuln```

5. Install TOR, set it on 80 port to be a NetwordRoutingLayer for http requests:
	```sudo apt install tor```
	```sudo nano /etc/tor/torrc```
	Uncomment ```HiddenServiceDir /var/lib/tor/hidden_service/```
	Signify where to store hidden_service files
	Tor generates there a private key and a hostname like xxxx.onion

	Uncomment ```HiddenServicePort 80 127.0.0.1:80```
	Forward incoming traffic on port 80 of xxxx.onion to port 80 on 127.0.0.1
	As it is previously set, NGINX will then receive the incoming request

	```sudo systemctl restart tor```
	Trigger tor new configuration (in /etc/tor/torrc) detection

6. Install curl to make a test request to the .onion website
	```sudo apt install curl```
	```torsocks curl http://xxx.onion```

7. Install TOR Browser to visualize the host-website
	```sudo apt install wget gnupg```
	Install dependencies

	```wget https://www.torproject.org/dist/torbrowser/14.5.3/tor-browser-linux-x86_64-14.5.3.tar.xz```
	```tar -xf tor-browser-linux-x86_64-14.5.3.tar.xz```
	Download TOR Browser archive then extract it

8. Open TOR Browser
	Go in the TOR extracted folder
	Execute the launcher (something like ./start-tor-browser.deskop)

9. Configure NGINX to always send back index.html in the response on localhost:80
	```sudo nano /etc/nginx/nginx.conf```
	```
	###############MYEDIT##################
	server {
		location / {
			root	/data/www;
			index	/html/index.html;
                }       
        }
	###############MYEDIT##################
	```
	To add in the http{} section
10. Generate with AI a simple index.html
