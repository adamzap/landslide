#include <stdio.h>
#include <stdlib.h>

static const char *day[] = {
	NULL, 		/* day 0 */
	"monday",
	"tuesday",
	"wednesday",
	"thursday",
	"friday",
	"saturday",
	"sunday",
};
int
main(int argc, char *argv[])
{
	int nth;
	if (argc > 1 && (nth = atoi(argv[1])) < 7 && nth > 0)
		printf("%s\n", day[nth]);
	else	fprintf(stderr, "%s [1-7]\n", argv[0]);
	return 0;
}
