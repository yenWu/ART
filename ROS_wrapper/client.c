/*
 * Copyright © 2008-2010 Stéphane Raimbault <stephane.raimbault@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
//sudo apt-get install libmodbus5 libmodbus-dev
//gcc bandwidth-client.c -o bandwidth-client `pkg-config --libs --cflags libmodbus`

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <errno.h>

#include <modbus.h>

uint16_t * intdup(uint16_t const * src, size_t len)
{
   uint16_t * p = malloc(len * sizeof(int));
   memcpy(p, src, len * sizeof(int));
   return p;
}

/* Tests based on PI-MBUS-300 documentation */
int main(int argc, char *argv[])
{
    uint16_t *read_reg_array;
    uint16_t *write_reg_array;
    uint16_t *read_reg_array_old;

    modbus_t *ctx;
    int i;
    int nb_points;

    int rc;
    int use_backend;

    int address_used = 10;



    ctx = modbus_new_tcp("127.0.0.1", 1502);

    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Connexion failed: %s\n",
                modbus_strerror(errno));
        modbus_free(ctx);
        return -1;
    }

    /* Allocate and initialize the memory to store the registers */
    read_reg_array = (uint16_t *) malloc(address_used * sizeof(uint16_t));
    read_reg_array_old = (uint16_t *) malloc(address_used * sizeof(uint16_t));
    
    write_reg_array = (uint16_t *) malloc(address_used * sizeof(uint16_t));

    nb_points = address_used;

    memset(read_reg_array, 0, address_used * sizeof(uint16_t));
    memset(write_reg_array, 0, address_used * sizeof(uint16_t));

    read_reg_array_old = intdup(read_reg_array,address_used);

    for(i=0;i<address_used;i++)
    	write_reg_array[i] = i*3;



    /*print array*/
/*
    printf("iniaial REGISTERS\n\n");
    printf("READ array\n\n");
    for(i=0;i<address_used;i++)
    {
        printf("%d\n",read_reg_array[i]); 
    }
    printf("WRITE array\n\n");
    for(i=0;i<address_used;i++)
    {
        printf("%d\n",write_reg_array[i]); 
    }
*/  

    for(;;)
    {

	//read
	rc = modbus_read_registers(ctx,
		             0, nb_points, read_reg_array);
	if (rc == -1)
	{
		fprintf(stderr, "%s\n", modbus_strerror(errno));
		return -1;
	}
	printf("READ REGISTERS...(100%%)\n");
	for(i=0;i<address_used;i++)
		if(read_reg_array_old[i] != read_reg_array[i])
		{
			printf("Data diff\n");
			read_reg_array_old = intdup(read_reg_array,address_used);
			break;
		}
	sleep(1);
    }

    //write
    rc = modbus_write_registers(ctx,
		             0, nb_points, write_reg_array);
    if(rc == -1)
    {
	fprintf(stderr, "%s\n", modbus_strerror(errno));
	return -1;
    }
    printf("WRITE REGISTERS...(100%%)\n\n");



    /* Free the memory */
    free(read_reg_array);
    free(write_reg_array);
    
  
    /* Close the connection */
    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}

