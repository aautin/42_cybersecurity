NAME=ft_otp

CC=cc
CFLAGS=-Wall -Werror -Wextra -g3

INC_LIB=sha1
LIB=sha1

INC_DIR=-Iinc -Isha1/inc
SRC_DIR=src
OBJ_DIR=obj

FILES=hmac debug parsing time totp

SRC=$(addsuffix .c, $(addprefix $(SRC_DIR)/, $(FILES)))
OBJ=$(addsuffix .o, $(addprefix $(OBJ_DIR)/, $(FILES)))

.PHONY: all re clean fclean

all: $(NAME)

$(INC_LIB)/Makefile:
	git submodule update --init --recursive

$(INC_LIB)/lib$(LIB).a: $(INC_LIB)/Makefile
	make -C $(INC_LIB)

$(NAME): $(INC_LIB)/lib$(LIB).a $(OBJ_DIR) $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -L$(INC_LIB) -l$(LIB) -o $@

$(OBJ_DIR):
	mkdir -p $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@ $(INC_DIR)

re: fclean all

clean:
	rm -rf $(OBJ_DIR)

fclean: clean
	rm -f $(INC_LIB)/lib$(LIB).a
	rm -f $(NAME)
