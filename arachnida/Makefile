FILES=	scorpion \
		spider

SRC_DIR=src
SRC= $(addprefix $(SRC_DIR)/, $(addsuffix .ts, $(FILES)))

DIST_DIR=dist
DIST= $(addprefix $(DIST_DIR)/, $(addsuffix .js, $(FILES)))

CC=npx tsc
OUTPUT_FLAG= --outDir $(DIST_DIR)

NODE_MODULES=node_modules/typescript/bin/tsc node_modules/@types/node/package.json

.PHONY: all re clean_dist clean_node_modules clean

all: $(NODE_MODULES) $(DIST)

re: clean_dist all

clean_dist:
	rm -rf $(DIST_DIR)

clean_node_modules:
	rm -rf node_modules

clean: clean_dist clean_node_modules

$(NODE_MODULES):
	npm install

$(DIST_DIR):
	mkdir -p $@

$(DIST_DIR)/%.js: $(SRC_DIR)/%.ts
	$(CC) $^ $(OUTPUT_FLAG)

