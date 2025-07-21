//   caminho mais curto num grafo acíclico
min:       6 xs1 +1 xs2 +7 x13 +2 x21 +3 x24 +6 x3t + 1x43 +1 x4t;

/* Restrições */
//  conservação de fluxo
vertice_s:   xs1  + xs2                                              =  1;
vertice_1: - xs1         + x13  - x21                                =  0;
vertice_2:        - xs2         + x21  + x24                         =  0;
vertice_3:               - x13                + x3t  - x43           =  0;
vertice_4:                             - x24         + x43  + x4t    =  0;
vertice_t:                                    - x3t         - x4t    = -1;

//  tempo máximo de viagem
           1 xs1 +5 xs2 +3 x13 +1 x21 +2 x24 +4 x3t +3 x43 +5 x4t    <= 9;

bin xs1, xs2, x13, x21, x24, x3t, x43, x4t;










