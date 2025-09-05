# ---------------- OWASP (Juice Shop) ----------------
OWASP_IMAGE      ?= bkimminich/juice-shop
OWASP_CONTAINER  ?= owasp-juice-shop
OWASP_PORT       ?= 3000
OWASP_HOST_PORT  ?= 3000

# ---------------- bWAPP ----------------
BWAPP_COMPOSE    ?= docker-compose
BWAPP_VOLUME     ?= vaccine_db_data


# ========== GENERAL ==========
.PHONY: owasp owasp-up owasp-down owasp-build owasp-restart owasp-clean owasp-fclean owasp-re owasp-fre \
        bwapp bwapp-up bwapp-down bwapp-build bwapp-restart bwapp-clean bwapp-fclean bwapp-re bwapp-fre \
		all up down build restart clean fclean re fre

all: owasp bwapp

up: owasp-up bwapp-up
down: owasp-down bwapp-down

build: owasp-build bwapp-build

restart: owasp-restart bwapp-restart

clean: owasp-clean bwapp-clean
fclean: owasp-fclean bwapp-fclean

re: owasp-re bwapp-re
fre: owasp-fre bwapp-fre


# ========== OWASP ==========
owasp: owasp-build owasp-up

owasp-up:
	@echo "[OWASP] Starting $(OWASP_CONTAINER) on http://localhost:$(OWASP_HOST_PORT)"
	@docker run -d --restart unless-stopped --name $(OWASP_CONTAINER) -p $(OWASP_HOST_PORT):$(OWASP_PORT) $(OWASP_IMAGE)
owasp-down:
	@echo "[OWASP] Removing container: $(OWASP_CONTAINER)"
	-@docker rm -f $(OWASP_CONTAINER)

owasp-build:
	@echo "[OWASP] Pulling image"
	@docker pull $(OWASP_IMAGE)

owasp-restart:
	@echo "[OWASP] Restarting $(OWASP_CONTAINER) (or start if missing)"
	@docker restart $(OWASP_CONTAINER) || $(MAKE) owasp-up

owasp-clean: owasp-down
	@echo "[OWASP] Removing image: $(OWASP_IMAGE)"
	-@docker rmi -f $(OWASP_IMAGE)
owasp-fclean: owasp-clean
	@echo "[OWASP] No volumes to remove."

owasp-re: owasp-clean owasp
owasp-fre: owasp-fclean owasp


# ========== bWAPP ==========
bwapp: bwapp-build bwapp-up

bwapp-up:
	@echo "[bWAPP] Starting stack"
	@$(BWAPP_COMPOSE) up -d
bwapp-down:
	@echo "[bWAPP] Stopping stack"
	@$(BWAPP_COMPOSE) down

bwapp-build:
	@echo "[bWAPP] Building images"
	@$(BWAPP_COMPOSE) build

bwapp-restart:
	@echo "[bWAPP] Restarting services"
	@$(BWAPP_COMPOSE) restart

bwapp-clean:
	@echo "[bWAPP] Down + remove images/orphans"
	@$(BWAPP_COMPOSE) down --rmi all --remove-orphans --timeout 3 || true
bwapp-fclean: bwapp-clean
	@echo "[bWAPP] Removing volume: $(BWAPP_VOLUME)"
	-@docker volume rm $(BWAPP_VOLUME)

bwapp-re: bwapp-clean bwapp
bwapp-fre: bwapp-fclean bwapp