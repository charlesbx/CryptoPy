##
## EPITECH PROJECT, 2023
## B-CNA-500-PAR-5-1-cryptography-charles.baux
## File description:
## Makefile
##

NAME	=	mypgp

SRC		=	src/main.py

all:	$(NAME)

$(NAME):
	cp $(SRC) $(NAME)
	chmod +x $(NAME)

clean:
	rm -f $(NAME)

fclean:	clean

re:	fclean all

.PHONY:	all clean fclean re