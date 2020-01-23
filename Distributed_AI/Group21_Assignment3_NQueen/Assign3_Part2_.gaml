/**
* Name: Assign3part2
* Author: Khushdeep Singh
* Description: 
* Tags: Tag1, Tag2, TagN
*/

model Assign3_part2

/* Insert your model definition here */

global {
	geometry bounds <- rectangle ( {0,0}, {200,200});

	int stage_num <- 4;
	int part_num <- 20;
	int count <- 1;
    
    int count0 <- 0;
    int count1<- 0;
    int count2<- 0;
    int count3<- 0;
	int get_stage<- 0;
	int stage_max_ppl <- 0;
	int interest;
	int timer<- 0;
	
	bool giveResult<- true;
	bool goLocation<- false;
	bool count_each_stage<- false;
	bool max_ppl_stage_number<- false;
	bool go_elsewhere<- false;
	bool interest1_start<- false;
	
	list<point> places<- [ {20,20}, {20,80}, {80,20}, {80,80}];
	list<int> winner_stage;
	list<int> ppl_in_stages;
	
	point get_max_ppl_location<- nil;
	 
	init {
		int j<- 0;	
		create stages number: stage_num
		 {  
		 	location <- places[j];
            j<- j+1;
		 }
		create participant number: part_num 
		  { location<- (rnd(10),rnd(10)); }
		
		create leader number: 1 
		  { location<- {50,50}; } 		 
	}
}


species stages 
{   
	float sound <- flip(0.5) ? rnd(2.0): rnd(9.0);
	float light <- flip(0.5) ? rnd(4.0): rnd(14.0);
	float music <- flip(0.5) ? rnd(0.50): rnd(5.0);
	float dance <-  rnd(1.0);
	float area  <- flip(0.5) ? rnd(7.0): rnd(17.0);
	float drama <- flip(0.5) ? rnd(2.0): rnd(12.0);
	float food  <- rnd(3.0);
	
	aspect default{
		draw pyramid(5) at: location color: #blue;		
		}
}

species participant skills: [moving] 
{  	float light <- flip(0.5) ? rnd(2.0): rnd(9.0);
	float dance <- flip(0.5) ? rnd(4.0): rnd(14.0);
	float drama <- rnd(5.0);
	float sound <- flip(0.5) ? rnd(1.0): rnd(19.0);
	float food  <- flip(0.5) ? rnd(7.0): rnd(17.0);
	float music <- rnd(12.0);
	float area  <- flip(0.5) ? rnd(3.0): rnd(13.0);
	
	float result<- 0.0 ;
	int i<- 1;
	
	float utility<- 0.0;
	point saveLocation<- nil;
		
	reflex finding_utility when: giveResult
	{   interest<- rnd(1,2);
		write ' interest value is ' + interest;
		loop k over: stages
		{
			ask k {
			myself.result <- ((myself.sound * self.sound) + (myself.light * self.light) +(myself.music * self.music) +(myself.dance * self.dance) +(myself.area * self.area) +(myself.drama * self.drama) +(myself.food * self.food) );
			write  ' result value for stage '+ k + ' is ' + myself.result;		
		    
		    if ( myself.result > myself.utility)
		    	{ myself.utility<- myself.result ;
		    		myself.saveLocation<- k.location; 
		    		get_stage<- k;    		
		    	} 		 	      
	        } 
	    }
	    count_each_stage<- true;
		write ' Maximum utility is ' + utility + ' for stage ' + get_stage;
		winner_stage<< get_stage;
		write ' winner stage is '+ winner_stage; 
		write ' ';
		
		if ( count= part_num)
			{   
				giveResult<- false;				
			}
		else 
			{  count <- count + 1; }			
	}
		     
	reflex goto_acquired_position when:  goLocation 
 		{  	if(interest=2)		
 			{       write ' I am going interest =2 ';
		  			write ' save location is ' + saveLocation;
					write ' condition is true';
					do goto target: saveLocation speed: 4.0;		
					if(location distance_to( saveLocation ) < 2)
						  { do wander;  }
		  if (interest=1)
		  {
	  		   write ' interest=1 going to target ';
				do goto target: saveLocation speed: 4.0;		
				  if(location distance_to( saveLocation ) < 6)
				    { do wander; }
		  }				  			  			  			    
		}	
	}

	aspect default{
		draw circle(3) at: location color: #red;
		}
}


species leader 
 { 
    reflex count_of_each_stage when: count_each_stage
		{   write ' Leader is counting '   ;
			loop i over: winner_stage
			{
				if ( i= 0)
			  		{ count0<- count0 + 1; }
			  	 if ( i= 1)
			  		{ count1<- count1 + 1; }
			  	if ( i= 2)
			  		{ count2<- count2 + 1; }
			  	if ( i= 3)
			  		{ count3<- count3 + 1; }
			}
			
			write ' stage 0 contains '+ count0 + ' participants';
			write ' stage 1 contains '+ count1 + ' participants';
			write ' stage 2 contains '+ count2 + ' participants';
			write ' stage 3 contains '+ count3 + ' participants';
            
            count_each_stage<- false;
            max_ppl_stage_number<- true;
      }
      
      reflex get_max_ppl_stage_number when: max_ppl_stage_number     
       {     
	            ppl_in_stages<< count0;
	            ppl_in_stages<< count1;
	            ppl_in_stages<< count2;
	            ppl_in_stages<< count3;  

            loop i from: 0 to: (stage_num-1)
            {
            	if ( ppl_in_stages[i]> ppl_in_stages[stage_max_ppl])
            	{
            		stage_max_ppl <- i;
            	}
            }
            
            write ' maximum people are in stage '+ stage_max_ppl ;
            get_max_ppl_location<- places[stage_max_ppl];
            write ' max ppl location is ' + get_max_ppl_location;
            goLocation<- true;	
            max_ppl_stage_number<- false;		
		}
 	
 	aspect default{
		draw ellipse(6,8) at: location color: #orange;
		}
 }
 
 
experiment Assignment3_stages type: gui {
	
	output {
		display map type: opengl {
			species stages;
			species participant;
			species leader;
		}
	}
}