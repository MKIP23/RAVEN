# Makefile for RISC-V project

# Project name
PROJ=crun

# Source files
SRCS=main.c aes_util.c aes.c

# Object files
OBJS=${SRCS:.c=.o}

# Compiler
CC=/home/mahreen/Downloads/gem5+riscv/riscv/bin/riscv64-unknown-linux-gnu-gcc -O0

# Compiler and linker flags
CFLAGS=-g -DESTDEF=$(EST)
LDFLAGS=-g
LDLIBS=-static -lm

# Target to build the project
all: ${PROJ}

# Build the project
${PROJ}: ${OBJS}
	${CC} ${CFLAGS} -o ${PROJ} ${OBJS} ${LDLIBS}

# Rule for building object files
%.o: %.c
	${CC} ${CFLAGS} -c $< -o $@

# Clean up
clean:
	rm -f ${PROJ} ${OBJS}

