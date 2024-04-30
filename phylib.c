/*Silas Wright
ID: 1217810
swrigh24@uoguelph.ca
Assignment for class 2750
This library will provide physics for colliding billard balls for use in a pool table implementation*/


//Imports
#include "phylib.h"
#include "stdlib.h"
#include <stdio.h>
#include <math.h>
#include <string.h>
/*This function will allocate memory for a new phylib_object, set its type to
PHYLIB_STILL_BALL and transfer the information provided in the function parameters into the
structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
return NULL (before trying to store the function parameters in the (non-existent) structure)
*/
phylib_object *phylib_new_still_ball( unsigned char number,
phylib_coord *pos ){
    phylib_object * newBall;//declare variable
    newBall = (phylib_object*) malloc(sizeof(phylib_object));//dynamically allocate memory

    if(newBall == NULL){//if malloc fails return null
        return NULL;//return null
    }else{
	//set attributes
        newBall->type = PHYLIB_STILL_BALL;
        newBall->obj.still_ball.number = number;
        newBall->obj.still_ball.pos.x = pos->x;
	newBall->obj.still_ball.pos.y = pos->y;
        return newBall;//return the newball
    }
}

/*This function will allocate memory for a new phylib_object, set its type to
PHYLIB_ROLLING_BALL and transfer the information provided in the function parameters into the
structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
return NULL (before trying to store the function parameters in the (non-existent) structure)
*/
phylib_object *phylib_new_rolling_ball( unsigned char number,phylib_coord *pos,phylib_coord *vel,
phylib_coord *acc ){
    phylib_object * newBall;//declare variable
    newBall = (phylib_object*) malloc(sizeof(phylib_object));//dynamically allocate memory

    if(newBall == NULL){//if malloc fails return NULL
        return NULL;//return null
    }else{
	//set attributes
        newBall->type = PHYLIB_ROLLING_BALL;
        newBall->obj.rolling_ball.number = number;
        newBall->obj.rolling_ball.pos.x = pos->x;
	newBall->obj.rolling_ball.pos.y = pos->y;
        newBall->obj.rolling_ball.vel.x = vel->x;
	newBall->obj.rolling_ball.vel.y = vel->y;
        newBall->obj.rolling_ball.acc.x = acc->x;
	newBall->obj.rolling_ball.acc.y = acc->y;
        return newBall;//return the new ball
    }
}


/*This function will allocate memory for a new phylib_object, set its type to
PHYLIB_HOLE and transfer the information provided in the function parameters into the
structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
return NULL (before trying to store the function parameters in the (non-existent) structure)
*/
phylib_object *phylib_new_hole( phylib_coord *pos ){
    phylib_object * newHole;//declare variable
    newHole = (phylib_object*) malloc(sizeof(phylib_object));//dynamically allocate memory

    if(newHole == NULL){//if malloc fails return null
        return NULL;//return null
    }else{
	//set attributes
        newHole->type = PHYLIB_HOLE;
        newHole->obj.hole.pos.x = pos->x;
	newHole->obj.hole.pos.y = pos->y;
        return newHole;//return the new hole
    }
}

/*This function will allocate memory for a new phylib_object, set its type to
PHYLIB_HCUSHION and transfer the information provided in the function parameters into the
structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
return NULL (before trying to store the function parameters in the (non-existent) structure)
*/
phylib_object *phylib_new_hcushion( double y ){
    phylib_object * newCushion;//declare variable
    newCushion = (phylib_object*) malloc(sizeof(phylib_object));//dynamically allocate memory

    if(newCushion == NULL){//if malloc fails return null
        return NULL;//return null
    }else{
	//set attributes
        newCushion->type = PHYLIB_HCUSHION;
        newCushion->obj.hcushion.y = y;
        return newCushion;//return the newcushion
    }
}



/*This function will allocate memory for a new phylib_object, set its type to
PHYLIB_VCUSHION and transfer the information provided in the function parameters into the
structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
return NULL (before trying to store the function parameters in the (non-existent) structure)
*/
phylib_object *phylib_new_vcushion( double x ){
    phylib_object * newCushion;//declare variable
    newCushion = (phylib_object*) malloc(sizeof(phylib_object));//dynamically allocate memory

    if(newCushion == NULL){//if malloc fails return null
        return NULL;//return null
    }else{
	//set attributes
        newCushion->type = PHYLIB_VCUSHION;
        newCushion->obj.vcushion.x = x;
        return newCushion;//return null
    }
}

/*This function will allocate memory for a table structure, returning NULL if the memory
allocation fails. The member variable, time, will be set to 0.0. It will then assign the values of
its array elements to pointers to new objects created by the phylib_new_* functions provided
above. Specifically, it will add elements in this order:
1) a horizontal cushion at y=0.0;
2) a horizontal cushion at y=PHYLIB_TABLE_LENGTH;
3) a vertical cushion at x=0.0;
4) a vertical cushion at x=PHYLIB_TABLE_WIDTH;
5) 6 holes: positioned in the four corners where the cushions meet and two more
midway between the top holes and bottom holes.
The remaining pointers will all be set to NULL.*/
phylib_table *phylib_new_table( void ){
    phylib_table * newTable;//declare variables
    newTable = (phylib_table*) malloc(sizeof(phylib_table));//dynamically allocate memory

    if(newTable == NULL){//return null if malloc fails
        return NULL;//return null
    }else{
	//add objects to table
        newTable->time = 0.0;//set time

        newTable->object[0] = phylib_new_hcushion(0.0);
        newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
        newTable->object[2] = phylib_new_vcushion(0.0);
        newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
	
	//setting up holes
	phylib_coord hole1;
	hole1.x = 0;
	hole1.y = 0;
	phylib_coord hole2;
        hole2.x = PHYLIB_TABLE_LENGTH/2;
        hole2.y = 0;
        phylib_coord hole3;
        hole3.x = PHYLIB_TABLE_LENGTH;
        hole3.y = 0;
        phylib_coord hole4;
        hole4.x = PHYLIB_TABLE_LENGTH;
        hole4.y = PHYLIB_TABLE_WIDTH;
        phylib_coord hole5;
        hole5.x = PHYLIB_TABLE_LENGTH/2;
        hole5.y = PHYLIB_TABLE_WIDTH;
        phylib_coord hole6;
        hole6.x = 0;
        hole6.y = PHYLIB_TABLE_WIDTH;


        newTable->object[4] = phylib_new_hole(&hole1);//first hole in top left
        newTable->object[5] = phylib_new_hole(&hole2);//second hole on top middle
        newTable->object[6] = phylib_new_hole(&hole3);//third hole top right
        newTable->object[7] = phylib_new_hole(&hole4);//fourth hole bottom right
        newTable->object[8] = phylib_new_hole(&hole5);//fith hole bottom middle since width is half height
        newTable->object[9] = phylib_new_hole(&hole6);//sixth hole bottom left


        for(int i = 10;i<PHYLIB_MAX_OBJECTS;i++){//set the rest of the objects to null
            newTable->object[i]=NULL;
        }
	return newTable;//return the new table
    }
}


/*This function should allocate new memory for a phylib_object. Save the address of that
object at the location pointed to by dest, and copy over the contents of the object from the
location pointed to by src. Hint, you can use memcpy to make this a one-step operation that
works for any type of phylib_object. If src points to a location containing a NULL pointer,
then the location pointed to by dest should be assigned the value of NULL.*/
void phylib_copy_object( phylib_object **dest, phylib_object **src ){
    if(*src == NULL){//if we are provided null pointer return null pointer
        *dest = NULL;
	return;//return null
    }
    *dest = (phylib_object*) malloc(sizeof(phylib_object));//dynamically allocate memory
    if(*dest == NULL){//if malloc fails return
	return;//return null
    }
    memcpy(*dest,*src,sizeof(phylib_object));//copy memory with memcpy
}


/*This function should allocate memory for a new phylib_table, returning NULL if the malloc
fails. Then the contents pointed to by table should be copied to the new memory location and
the address returned.*/
phylib_table *phylib_copy_table( phylib_table *table ){
    phylib_table * newTable;//declare variable
    //newTable = (phylib_table*) malloc(sizeof(phylib_table));//dynamically allocate memory
    newTable = phylib_new_table();
    if(newTable == NULL){//if malloc fails return null
        return NULL;//return null
    }

    phylib_object * sb;
    phylib_object * rb;

    newTable->time = table->time;//set time *this doesn't work i dont know why
    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){//loop and copy objects over
        if(table->object[i] != NULL){
            if(table->object[i]->type == PHYLIB_STILL_BALL){
                sb = phylib_new_still_ball(table->object[i]->obj.still_ball.number,&(table->object[i]->obj.still_ball.pos));
                phylib_add_object(newTable,sb);
            }else if(table->object[i]->type == PHYLIB_ROLLING_BALL){
                rb = phylib_new_rolling_ball(table->object[i]->obj.rolling_ball.number,&(table->object[i]->obj.rolling_ball.pos),&(table->object[i]->obj.rolling_ball.vel),&(table->object[i]->obj.rolling_ball.acc));
                phylib_add_object(newTable,rb);
            }
        }
        //phylib_copy_object(&(newTable->object[i]), &(table->object[i]));//copy each object this is shit so
    }
    return newTable;//return the new table
}

/*This function should iterate over the object array in the table until it finds a NULL pointer. It
should then assign that pointer to be equal to the address of object. If there are no NULL
pointers in the array, the function should do nothing.*/
void phylib_add_object( phylib_table *table, phylib_object *object ){
    for(int i = 0; i<PHYLIB_MAX_OBJECTS;i++){//loop through all objects
        if(table->object[i]==NULL){//if we find a null spot
	    phylib_copy_object(&(table->object[i]),&object);//copy the object
	    free(object);//free the object
            i = PHYLIB_MAX_OBJECTS;//and increment i to escape the loop since we are done
        }
    }
}


/*This function should free every non- NULL pointer in the object array of table. It should then
also free table as well.*/
void phylib_free_table( phylib_table *table ){
    for(int i = 0; i<PHYLIB_MAX_OBJECTS;i++){//loop through all objects
        if(table->object[i]==NULL){//if there is no object do nothing
            //do nothing
        }else{//if not free the object
            free(table->object[i]);//free the object
	    table->object[i]=NULL;//then make sure to get rid of the pointer in memory
        }
    }
    free(table);//free the table
}


/*This function should return the difference between c1 and c2. That is the result’s x value
should be c1.x-c2.x and similarly for y.*/
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    //declare and initialize variables to parameter attributes
    double x1 = c1.x;
    double x2 = c2.x;
    double y1 = c1.y;
    double y2 = c2.y;
    //declare a new coord and set its attributes as the difference of the provided coordinates
    phylib_coord newCoord;
    newCoord.x = x1-x2;
    newCoord.y = y1-y2;

    return newCoord;//return the new coordinate
}



/*This function should return the length of the vector/coordinate c. You can calculate this length
by using Pythagorean theorem. Important, you must not use the exp function from the math
library. That function is designed for raising values to a real power and is extremely inefficient
for something as simple as squaring a value.*/
double phylib_length( phylib_coord c ){
    //fprintf(stderr,"lngthfctn");
    double x2 = c.x * c.x;
    double y2 = c.y * c.y;

    double c2 = x2 + y2;
    //fprintf(stderr,"halfway");
    double length = sqrt(c2);
    //fprintf(stderr,"prertn");
    return length;//return the length
}



/*This function should compute the dot-product between two vectors. Hint: the dot product is
equal to the sum of: the product of the x-values and the product of the y-values.*/
double phylib_dot_product( phylib_coord a, phylib_coord b ){
    //multiply the parameters
    double xProduct = a.x * b.x;
    double yProduct = a.y * b.y;
    //add the products
    double dotProduct = xProduct + yProduct;

    return dotProduct;//return the dot product
}



/*This function should calculate the distance between two objects, obj1 and obj2. obj1 must be
a PHYLIB_ROLLING_BALL; if it is not the function should return -1.0. Otherwise ,the distance
between the obj1 (PHYLIB_ROLLING_BALL) and obj2 is given by the following rules:
1) If obj2 is another BALL ( ROLLING or STILL), then compute the distance between the
centres of the two balls and subtract two radii (i.e. one PHYLIB_BALL_DIAMETER).
2) If obj2 is a HOLE, then compute the distance between the centre of the ball and the
hole and subtract the HOLE_RADIUS.
3) If obj2 is a CUSHION calculate the distance between the centre of the ball and the
CUSION and subtract the BALL_RADIUS. Hint: use abs since the ball might be left/above
or right/below to CUSHION.
Return -1.0 if obj2 isn’t any valid type.*/
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    if(obj1->type != PHYLIB_ROLLING_BALL){//if object one isnt a rolling ball exit function
        return -1.0;//return -1.0 to signify incorrect object 1 type
    }else if(obj2 == NULL){//if object two is null then return 0
	    return 0;//return 0
    }
    double distance;//declare a variable for distance
    //use if statment to calculate distance with different formulas for different object types
    //the general formula for the distances is the length of the distance between the balls (phylib_sub) then
    //this total has a constant subtracted from it to form the final distance
    if(obj2->type == PHYLIB_STILL_BALL){
        distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos,obj2->obj.still_ball.pos))-PHYLIB_BALL_DIAMETER;
    }else if(obj2->type == PHYLIB_ROLLING_BALL){
        distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos,obj2->obj.rolling_ball.pos))-PHYLIB_BALL_DIAMETER;
    }else if(obj2->type == PHYLIB_HOLE){
        distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos,obj2->obj.hole.pos))-PHYLIB_HOLE_RADIUS;
    }else if(obj2->type == PHYLIB_HCUSHION){
        distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y)-PHYLIB_BALL_RADIUS;
    }else if(obj2->type == PHYLIB_VCUSHION){
	    distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x)-PHYLIB_BALL_RADIUS;
    }else{
        return -1.0;//if object two is not a known type then return -1.0
    }
    return distance;//return distance
}


/*This function updates a new phylib_object that represents the old phylib_object after it
has rolled for a period of time. If new and old are not PHYLIB_ROLLING_BALLs, then the
function should do nothing. Otherwise, it should update the values in new. Specifically the
position, and velocities should be updated as follows:

p=p1+v1t+0.5a1t^2

(For physics/math fans, this is the second integral of the acceleration.) Here, the variable
represents either the x or y position of the ball, the variable represents either the x or y
velocity of the ball, and represents either the x or y acceleration of the ball. The subscript 1
indicates we are talking about the old ball. The velocity of the new ball (in either the x or y
dimension) is given by:

v=v1+a1t

One additional constraint must be observed. If either velocity changes sign, then that velocity
and its corresponding acceleration ( x, or y) must be set to zero (if both velocities change sign,
then both velocities and both accelerations must be set to zero).*/
void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    if(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL){
	//calculate position with this formula p=p1+v1t+0.5a1t^2
        new->obj.rolling_ball.pos.x = (old->obj.rolling_ball.pos.x) + (old->obj.rolling_ball.vel.x*time) +(0.5*old->obj.rolling_ball.acc.x*(time*time));
        new->obj.rolling_ball.pos.y = (old->obj.rolling_ball.pos.y) + (old->obj.rolling_ball.vel.y*time) +(0.5*old->obj.rolling_ball.acc.y*(time*time));
	//calculate velocity with this formula v=v1+a1t
        new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x*time);
        new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y*time);
	
	//if the either velocity changes sign set acc and vel to 0
	//find if it changes sign by multiplying and checking if its negitive
        if(new->obj.rolling_ball.vel.x*old->obj.rolling_ball.vel.x < 0){
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }

        if(new->obj.rolling_ball.vel.y*old->obj.rolling_ball.vel.y < 0){
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }
    }
}


/*This function will check whether a ROLLING_BALL has stopped, and if it has, will convert it to a
STILL_BALL. You may assume that object is a ROLLING_BALL. The function will return 1 if it
converts the ball, 0 if it does not.
For the purposes of this simulation a ball is considered to have stopped if its speed (which is the
length of its velocity) is less than PHYLIB_VEL_EPSILON.
Do not assume that the number, and x and y positions of the rolling ball will be automatically
transferred to the still ball.*/
unsigned char phylib_stopped( phylib_object *object ){
    //declare variable for speed (as length of velocity
    double speed = phylib_length(object->obj.rolling_ball.vel);
    if(speed<PHYLIB_VEL_EPSILON){//if the speed if below our constant threshold
	//transfer the number and position
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
	//change type to phylib still ball
        object->type = PHYLIB_STILL_BALL;
        return 1;//return 1
    }else{//if the speed is above our constant threshold return 0
        return 0;//return 0
    }
}

/*This is the most complicated function in the assignment but it can be handled by divide and
conquer based on the type of object b. You may assume that object a is a ROLLING_BALL.
Note that the two arguments to this function are double pointers. That is, they are pointers to
pointers to phylib_objectss.
CASE 1: b is a HCUSHION:
In this case the y velocity and y acceleration of a are reversed (negated). This is the
physical principle of angle of incidence equals angle of reflection.
CASE 2: b is a VCUSION:
In this case the x velocity and x acceleration of a are reversed (negated). This is the
physical principle of angle of incidence equals angle of reflection.
CASE 3: b is a HOLE:
In this case, free the memory of a and set it to NULL. This represents the ball falling off
the table.
CASE 4: b is a STILL_BALL:
In this case, “upgrade” the STILL_BALL to a ROLLING BALL and proceed directly to CASE
5 (do not collect $200). HINT: if you leave out the break statement at the end of a case
condition, the code will continue with the next case.
CASE 5: b is a ROLLING_BALL:
This one is a little bit tricky and will require us to calculate a few intermediate values
before we can know the speeds and directions of the two balls after they collide.
Compute the position of a with respect to b: subtract the position of b from a; call it
r_ab.
Compute the relative velocity of a with respect to b: subtract the velocity of a from b;
call it v_rel.
Divide the x and y components of r_ab by the length of r_ab; call that a normal
vector, n.
Calculate the ratio of the relative velocity, v_rel, in the direction of ball a by computing
the dot_product of v_rel with respect to n; call that v_rel_n.
Now, ball a will roll perpendicular to the direction from a to b, and b will run in the
direction from a to b.
Update the x velocity of ball a by subtracting v_rel_n multipied by the x component of
vector n. Similarly, Update the x velocity of ball a by subtracting v_rel_n multipied by
the x component of vector n.
Update the x and y velocities of ball b by adding the product of v_rel_n and vector n.
Compute the speed of a and b as the lengths of their velocities. If the speed is greater
than PHYLIB_VEL_EPSILON then set the acceleration of the ball to the negative
velocity divided by the speed multiplied by PHYLIB_DRAG.*/
void phylib_bounce( phylib_object **a, phylib_object **b ){
    //use switch statement to handle difference outcomes based on the type of b
    switch ((*b)->type) {

        case PHYLIB_HCUSHION:
	    //negate the y velocity and acceleration of the rolling ball
    	    (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
    	    (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
            break;//break

        case PHYLIB_VCUSHION:
	    //negate the x velocity and acceleration of the rolling ball
            (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
    	    (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
            break;//break

        case PHYLIB_HOLE:
	    //free the ball and set its pointer to null
            free(*a);
            *a = NULL;
            break;//break

        case PHYLIB_STILL_BALL: {
	    //transfer the pos and number of ball
	    (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
	    //set the velocity nd acceleration of ball to 0
	    (*b)->obj.rolling_ball.vel = (phylib_coord){0.0, 0.0};
            (*b)->obj.rolling_ball.acc = (phylib_coord){0.0, 0.0};

	    (*b)->type = PHYLIB_ROLLING_BALL;//set object type to rolling ball
            
	    //NO BREAK: continue into rolling ball case
	}

        case PHYLIB_ROLLING_BALL: {
	    //compute relative position and velocity with phylib_sub
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos,(*b)->obj.rolling_ball.pos);
    	    phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel,(*b)->obj.rolling_ball.vel);
	    //declare variables for normal vector
	    //compute x and y attributes by the relivate position divided by the length of the relative position
    	    double normalX = r_ab.x / phylib_length(r_ab);
    	    double normalY = r_ab.y / phylib_length(r_ab);
	    //declare coordinate for normal n
    	    phylib_coord n ;
    	    n.x = normalX;
    	    n.y = normalY;
	    //calculate ratio of relative velocity with dot product
    	    double v_rel_n = phylib_dot_product(v_rel,n);
	    //subtract product of normal and ratio of relative velocity
    	    (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
    	    (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
	    //add product of normal and ratio of relative velocity
    	    (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
    	    (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;
	    //calculate speeds as length of respective velocities
    	    double aSpeed = phylib_length((*a)->obj.rolling_ball.vel);
    	    double bSpeed = phylib_length((*b)->obj.rolling_ball.vel);
            
	    //if either speed is greater than our constant for still balls then compute acceleration as negitive velocity divided by speed multiplied to our drag constant
	    if(aSpeed > PHYLIB_VEL_EPSILON){
        	(*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x)/ aSpeed*PHYLIB_DRAG;
        	(*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y)/ aSpeed*PHYLIB_DRAG;
    	    }
    	    if(bSpeed > PHYLIB_VEL_EPSILON){
        	(*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x)/ bSpeed*PHYLIB_DRAG;
        	(*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y)/ bSpeed*PHYLIB_DRAG;
		
    	    }
            break;//break
        }

        default://break on catch case
            break;//break
    }
}


/*This function should return the number of ROLLING_BALLS on the table*/
unsigned char phylib_rolling( phylib_table *t ){
    unsigned char count = 0;//declare variable to count rolling balls
    if(t == NULL){//if table pointer is empty return -1
	return -1;
    }else{//if not
        for(int i=0; i<PHYLIB_MAX_OBJECTS;i++){//loop through all objects
            if(t->object[i] != NULL){//if the object is not null
                if(t->object[i]->type == PHYLIB_ROLLING_BALL){//check to see if it is a rolling ball
                    count = count +1;//accumulate count variable
                }
	    }
        }
        return count;//return the rolling ball count
    }
}


/*This function should return a segment of a pool shot, as follows.
If there are no ROLLING_BALLs on the table, it should return NULL.
Otherwise, it should return a phylib_copy_table. The returned table should be the result of
applying the phylib_roll function to each ROLLING_BALL with a value of time that starts at
PHYLIB_SIM_RATE and increments by PHYLIB_SIM_RATE. All the balls should roll at the same
time, so make sure to put the loop over the OBJECTS inside the loop over the time. The loop
over the time should end if:
1) PHYLIB_MAX_TIME is reached,
2) The phylib_distance between the ball and another phylib_object is less than 0.0.
If this happens, apply the phylib_bounce function to the ball and the object before
returning the copy of the table.
3) A ROLLING_BALL has stopped.*/
phylib_table *phylib_segment( phylib_table *table ){
    unsigned char count = phylib_rolling(table);//declare variable and initialize with number of rolling balls
    if(count == 0){//if there are no rolling balls left return null
        return NULL;//return null
    }
    phylib_table *newTable = phylib_copy_table(table);//declare new table object and copy our table over
    //double time = PHYLIB_SIM_RATE;
    //newTable->time = table-> time;//copy time again here *i dont know why it doesnt work in other function
    //newTable->time += PHYLIB_SIM_RATE;//accumulate by our sim rate
    double relativeTime = PHYLIB_SIM_RATE;//declare another time variable to represent time from the start of this segment call
    while(relativeTime<PHYLIB_MAX_TIME){//loop until we reach max time constant
        for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){//loop through every object in table
	        if(newTable->object[i] != NULL){//as long as the object is not null continue
                if(newTable->object[i]->type == PHYLIB_ROLLING_BALL){//if the object is a rolling ball continue
                    //printf("TIME: %lf\tPOS.y: %lf\tVEL.y: %lf\tACC.y: %lf",newTable->time,table->object[i]->obj.rolling_ball.pos.y,table->object[i]->obj.rolling_ball.vel.y,table->object[i]->obj.rolling_ball.acc.y);
		            //run roll function
                    phylib_roll(newTable->object[i],table->object[i],relativeTime);
	            }
            }
        }
        for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
            if(newTable->object[i] != NULL){//as long as the object is not null continue
                if(newTable->object[i]->type == PHYLIB_ROLLING_BALL){//if the object is a rolling ball continue
                    for(int j=0;j<PHYLIB_MAX_OBJECTS;j++){//loop through all objects again
        		        if(i == j){//if we find this same rolling ball object then dont compare
            		        //do nothing but dont compare
        		        }else if(newTable->object[j] == NULL){//if we find a null pointer dont compare
            	            //do nothing but dont compare null pointer
        		        }else if(phylib_distance(newTable->object[i],newTable->object[j])<0.0){//compare the distance between the two objects
			                //if the distance if less than 0 then the objects have collided
            		        phylib_bounce(&(newTable->object[i]),&(newTable->object[j]));//call the bounce function
                            newTable->time += relativeTime;
                            return newTable;//return the new table
        		        }
                    }
	            }
            }
        }

        for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
            if(newTable->object[i] != NULL){//as long as the object is not null continue
                if(newTable->object[i]->type == PHYLIB_ROLLING_BALL){//if the object is a rolling ball continue
                    if(phylib_stopped(newTable->object[i])){
                        newTable->time += relativeTime;
                        return newTable;//return the new table
                    }
	            }
            }
        }
        relativeTime += PHYLIB_SIM_RATE;
    }
    newTable->time += relativeTime;
    return newTable;//return the new table
}

//Provided function from proffesor
char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf( string, 80, "STILL_BALL (%d,%6.1lf,%6.1lf)", object->obj.still_ball.number, object->obj.still_ball.pos.x, object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80, "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)", object->obj.rolling_ball.number, object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y, object->obj.rolling_ball.vel.x, object->obj.rolling_ball.vel.y, object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80, "HOLE (%6.1lf,%6.1lf)", object->obj.hole.pos.x, object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80, "HCUSHION (%6.1lf)", object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80, "VCUSHION (%6.1lf)", object->obj.vcushion.x );
            break;
    }
    return string;
}


int main(int argc,char ** argv){
	return 1;
}
