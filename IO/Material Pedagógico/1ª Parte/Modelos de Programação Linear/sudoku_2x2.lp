
/* funcão objectivo */
min: ;

/* restrições */
// cada célula apenas pode ter um algarismo
celula11: x111 + x112 + x113 + x114 = 1;
celula12: x121 + x122 + x123 + x124 = 1;
celula13: x131 + x132 + x133 + x134 = 1;
celula14: x141 + x142 + x143 + x144 = 1;

celula21: x211 + x212 + x213 + x214 = 1;
celula22: x221 + x222 + x223 + x224 = 1;
celula23: x231 + x232 + x233 + x234 = 1;
celula24: x241 + x242 + x243 + x244 = 1;

celula31: x311 + x312 + x313 + x314 = 1;
celula32: x321 + x322 + x323 + x324 = 1;
celula33: x331 + x332 + x333 + x334 = 1;
celula34: x341 + x342 + x343 + x344 = 1;

celula41: x411 + x412 + x413 + x414 = 1;
celula42: x421 + x422 + x423 + x424 = 1;
celula43: x431 + x432 + x433 + x434 = 1;
celula44: x441 + x442 + x443 + x444 = 1;

// numa linha, cada algarismo apenas pode aparecer uma vez
lin1num1: x111 + x121 + x131 + x141 = 1;
lin1num2: x112 + x122 + x132 + x142 = 1;
lin1num3: x113 + x123 + x133 + x143 = 1;
lin1num4: x114 + x124 + x134 + x144 = 1;

lin2num1: x211 + x221 + x231 + x241 = 1;
lin2num2: x212 + x222 + x232 + x242 = 1;
lin2num3: x213 + x223 + x233 + x243 = 1;
lin2num4: x214 + x224 + x234 + x244 = 1;

lin3num1: x311 + x321 + x331 + x341 = 1;
lin3num2: x312 + x322 + x332 + x342 = 1;
lin3num3: x313 + x323 + x333 + x343 = 1;
lin3num4: x314 + x324 + x334 + x344 = 1;

lin4num1: x411 + x421 + x431 + x441 = 1;
lin4num2: x412 + x422 + x432 + x442 = 1;
lin4num3: x413 + x423 + x433 + x443 = 1;
lin4num4: x414 + x424 + x434 + x444 = 1;

// numa coluna, cada algarismo apenas pode aparecer uma vez
col1num1: x111 + x211 + x311 + x411 = 1;
col1num2: x112 + x212 + x312 + x412 = 1;
col1num3: x113 + x213 + x313 + x413 = 1;
col1num4: x114 + x214 + x314 + x414 = 1;

col2num1: x121 + x221 + x321 + x421 = 1;
col2num2: x122 + x222 + x322 + x422 = 1;
col2num3: x123 + x223 + x323 + x423 = 1;
col2num4: x124 + x224 + x324 + x424 = 1;

col3num1: x131 + x231 + x331 + x431 = 1;
col3num2: x132 + x232 + x332 + x432 = 1;
col3num3: x133 + x233 + x333 + x433 = 1;
col3num4: x134 + x234 + x334 + x434 = 1;

col4num1: x141 + x241 + x341 + x441 = 1;
col4num2: x142 + x242 + x342 + x442 = 1;
col4num3: x143 + x243 + x343 + x443 = 1;
col4num4: x144 + x244 + x344 + x444 = 1;

// num bloco 2 x 2, cada algarismo apenas pode aparecer uma vez
NWnum1: x111 + x121 + x211 + x221 = 1;
NWnum2: x112 + x122 + x212 + x222 = 1;
NWnum3: x113 + x123 + x213 + x223 = 1;
NWnum4: x114 + x124 + x214 + x224 = 1;

NEnum1: x131 + x141 + x231 + x241 = 1;
NEnum2: x132 + x142 + x232 + x242 = 1;
NEnum3: x133 + x143 + x233 + x243 = 1;
NEnum4: x134 + x144 + x234 + x244 = 1;

SWnum1: x311 + x321 + x411 + x421 = 1;
SWnum2: x312 + x322 + x412 + x422 = 1;
SWnum3: x313 + x323 + x413 + x423 = 1;
SWnum4: x314 + x324 + x414 + x424 = 1;

SEnum1: x331 + x341 + x431 + x441 = 1;
SEnum2: x332 + x342 + x432 + x442 = 1;
SEnum3: x333 + x343 + x433 + x443 = 1;
SEnum4: x334 + x344 + x434 + x444 = 1;

// células que devem ter o algarismo dado no puzzle
dado12: x121 = 1;
dado13: x134 = 1;
dado24: x242 = 1;
dado31: x311 = 1;
dado42: x423 = 1;
dado43: x432 = 1;

// comentário:
// o lpsolve "confunde-se" quando se declara uma variável como
// binária depois de lhe atribuir explicitamente o valor 0 ou 1,
// como foi feito.
//
// declarar essas variáveis como binárias tem como efeito que
// a atribuição é ignorada.
bin
x111 x112 x113 x114      x122 x123 x124
x131 x132 x133      x141 x142 x143 x144
x211 x212 x213 x214 x221 x222 x223 x224
x231 x232 x233 x234 x241      x243 x244
     x312 x313 x314 x321 x322 x323 x324
x331 x332 x333 x334 x341 x342 x343 x344
x411 x412 x413 x414 x421 x422      x424
x431      x433 x434 x441 x442 x443 x444;

