/*
 * Copyright (C) 2017 Inria
 *               2017 Inria Chile
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     tests
 *
 * @file
 * @brief       Semtech LoRaMAC test application
 *
 * @author      Alexandre Abadie <alexandre.abadie@inria.fr>
 * @author      Jose Alamos <jose.alamos@inria.cl>
 */

#include <string.h>
#include <inttypes.h>

#include "msg.h"
#include "shell.h"
#include "fmt.h"

#include "net/loramac.h"
#include "semtech_loramac.h"
#include <time.h>
#include "xtimer.h"

semtech_loramac_t loramac;

static const uint8_t deveui[LORAMAC_DEVEUI_LEN] = { 0x00, 0x95, 0xE2, 0xB0, 0x7D, 0x00, 0xAD, 0x7B };
static const uint8_t appeui[LORAMAC_APPEUI_LEN] = { 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x02, 0xD6, 0xD1 };
static const uint8_t appkey[LORAMAC_APPKEY_LEN] = { 0x81, 0xB2, 0xD0, 0x81, 0x59, 0xEC, 0x2F, 0xEE, 0xAC, 0x19, 0x74, 0x77, 0x58, 0x50, 0xB2, 0x3B };

int data_gen(char* data_sens)
{
	srand(time(0));
	static int data[5];
	data[0]= (rand() % 51) - (rand() % 51);
	data[1]= rand() % 101;
	data[2]= rand() % 361;
	data[3]= rand() % 101;
	data[4]= rand() % 51;

	sprintf(data_sens , "%d,%d,%d,%d,%d", data[0],data[1],data[2],data[3],data[4]);
	
	return 0;
}

int loramac_data_transmission(void)
{
	 
	printf("start function");
	
	while (1){
		xtimer_sleep(10);
		uint8_t cnf = LORAMAC_DEFAULT_TX_MODE;  /* Default: confirmable */
		uint8_t port = LORAMAC_DEFAULT_TX_PORT; /* Default: 2 */

		semtech_loramac_set_tx_mode(&loramac, cnf);
		semtech_loramac_set_tx_port(&loramac, port);

		char data_sens[128];
		
		data_gen(data_sens);
		
        switch (semtech_loramac_send( &loramac, (uint8_t *)data_sens, strlen(data_sens) )) {
            case SEMTECH_LORAMAC_NOT_JOINED:
                puts("Cannot send: not joined");
                return 1;

            case SEMTECH_LORAMAC_DUTYCYCLE_RESTRICTED:
                puts("Cannot send: dutycycle restriction");
                return 1;

            case SEMTECH_LORAMAC_BUSY:
                puts("Cannot send: MAC is busy");
                return 1;

            case SEMTECH_LORAMAC_TX_ERROR:
                puts("Cannot send: error");
                return 1;
        }

        /* wait for receive windows */
        switch (semtech_loramac_recv(&loramac)) {
            case SEMTECH_LORAMAC_DATA_RECEIVED:
                loramac.rx_data.payload[loramac.rx_data.payload_len] = 0;
                printf("Data received: %s, port: %d\n",
                       (char *)loramac.rx_data.payload, loramac.rx_data.port);
                break;

            case SEMTECH_LORAMAC_DUTYCYCLE_RESTRICTED:
                puts("Cannot send: dutycycle restriction");
                return 1;

            case SEMTECH_LORAMAC_BUSY:
                puts("Cannot send: MAC is busy");
                return 1;

            case SEMTECH_LORAMAC_TX_ERROR:
                puts("Cannot send: error");
                return 1;

            case SEMTECH_LORAMAC_TX_DONE:
                puts("TX complete, no data received");
                break;
        }

	}
    return 0;
}

int main(void)
{
    semtech_loramac_init(&loramac);

	 semtech_loramac_set_dr(&loramac, 5);

    /* set LoRaWAN keys */
    semtech_loramac_set_deveui(&loramac, deveui);
    semtech_loramac_set_appeui(&loramac, appeui);
    semtech_loramac_set_appkey(&loramac, appkey);

    /* join procedure */
    puts("Starting join procedure");
    if (semtech_loramac_join(&loramac, LORAMAC_JOIN_OTAA) != SEMTECH_LORAMAC_JOIN_SUCCEEDED) {
        puts("Join procedure failed");
        return 1;
    }

    puts("Join procedure succeeded");
    loramac_data_transmission();
}
