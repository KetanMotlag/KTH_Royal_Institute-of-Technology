/**
* Name: assignment1
* Authors: Khushdeep Singh Mann and Ketan Motlag
* Tags: Tag1, Tag2, TagN
*/

model Assigment_1_GAMA_Agents

/* Insert your model definition here */

global {
	point infocenter<- {50,50};
	point hunger_location <- {0,0};
	geometry bounds <- rectangle ( {0,0}, {200,200});
	init {	
		create thirst_shop number: 2 {
			location<- flip(0.5) ? {15 + rnd(10), 70 + rnd(10)} : { 70+ rnd(10), 15+ rnd(10)};
		}
		create food_shop number: 2 { 
			location<- flip(0.5) ? {30 + rnd(10), 60 + rnd(10)} : { 60+ rnd(10), 30+ rnd(10)};
		}
		create guests number: 10    { 
			location<- flip(0.5) ? {10 + rnd(30), 20 + rnd(30)} : { 70+ rnd(10), 60+ rnd(10)};
		}
		create information_center number: 1 { }
		create police number:1
		   { location<- {70 + rnd(20),80 + rnd(10)}; }
		   }
		   
 	   }


species guests skills: [moving]{
	point location <- any_location_in(bounds);
	rgb mycolor<- #green;
	point target_point<- nil;
	bool hungry <- false;
	bool thirsty <- false;
	bool target_location<- false;
	point knownFoodstall;
	point knownDrinksStall;
	bool bad_guest <-false;
	bool food_loca_mem <- false;
	bool drink_loca_mem <- false;
	bool bad_agent<- false;
	int cnt <-0;
	
	reflex dance when: !hungry and !thirsty and !target_location 
	{   
		do wander;		
	    hungry <-  flip(0.01);
	    if(hungry and !bad_agent)
	    	{ mycolor<- #yellow;}
	    else if (bad_agent)
	    	{ mycolor<- #red;
	    	}
	  	
	  	else if (!hungry)
	  		{ thirsty <- flip(0.01);
	  			if(thirsty and !bad_agent)
	  			{ mycolor<- #blue;}
	  			else if (bad_agent)
	  			{ mycolor<- #red;}
	  		}	  	  
	 }
	  
	reflex if_hungry when: !thirsty and hungry and !target_location{
	 	if (knownFoodstall = nil or !food_loca_mem){
	 		target_location<- true;
	 		target_point<-infocenter;
	 		
	 		if(bad_agent )
	 		{ mycolor<- #yellow;	 }		 		
	 	}
	 	else{
	 			target_location<- true;
	 	 		target_point<-knownFoodstall;
	 	 		hungry<-false;	 		 
	 	}
	 } 
	 reflex if_thirsty when: thirsty and !hungry and !target_location{
	 	if (knownDrinksStall = nil or !drink_loca_mem){
	 		target_location<- true;
	 		target_point<-infocenter;
	 		
	 		if(bad_agent)
	 			{ mycolor<- #blue; }	 		 		
	 	}
	 	else{
	 			target_location<- true;
	 	 		target_point<-knownDrinksStall;
	 	 		thirsty<-false;	 	
	 
	 	}
	 } 
	 
	 reflex goto_target when:(thirsty or hungry) and target_location {
	 	do goto target: target_point;
	 	if(location distance_to(target_point)<1){
	 		target_location <- false;
	 		target_point<-nil;
	 		if(bad_agent and thirsty)
	 			{ mycolor<- #blue; }
	 		if ( bad_agent and hungry)
	 			{ mycolor<- #yellow; }
	 			
	 		list<information_center> infocenters <- information_center at_distance(100);
	 		write 'infocenters '+infocenters;
	 		
	 		if(!empty(infocenters)){
	 			information_center i <- infocenters at 0;
	 			if(hungry){
	 						if(bad_agent)
	 							{ mycolor<- #yellow;}
	 							
	 						write 'ásking for food';
	 						ask i{
	 							myself.knownFoodstall <- self.foodstores[rnd(length(self.foodstores)-1)];
	 							myself.target_point <- self.foodstores[rnd(length(self.foodstores)-1)];	 						 	
	 							}	
	 						target_location<-true;
	 						hungry<-false;	
	 					   }
	 					   
	 			else if (thirsty){
	 				if(bad_agent)
	 					{ mycolor<- #blue;}
	 				write 'ásking for water';
	 				ask i{
	 					myself.knownDrinksStall <-self.thirststores[rnd(length(self.thirststores)-1)];	
	 					myself.target_point <- self.thirststores[rnd(length(self.thirststores)-1)];	 	
	 				}
	 				thirsty<-false;
	 				target_location<-true;
	 			}			
	 		} 		
	 	} 	 	
	 }

	 
	 reflex goTo_target when: !hungry and !thirsty and  target_location {
	 	do goto target:target_point speed: 2.50; 
	  	if(location distance_to(target_point ) < 1){
	 			target_point<-nil;
	 			target_location<- false;
	 			food_loca_mem<- flip(0.85);
	 			drink_loca_mem<- flip(0.85);
	 			
	 			if(bad_agent)
	 				{ mycolor<- #red;}
	 			else 
	 				{ mycolor<- #green;}
	 		}
		}
						
	reflex breaking_bad when:!bad_guest{
		cnt <- cnt+1;
		bad_guest<- flip(cnt/10000);
		if (bad_guest){
			mycolor <- #red;
			bad_agent<- true;
		}
	}
	aspect default{
		draw sphere(2) at: location color: mycolor;
	} 	
}


species thirst_shop{
	point locat_thirst <- {rnd(100),rnd(100)};
	
	aspect default{
		draw square(4) at: locat_thirst color: #blue;
	}
}


species food_shop{
	point locat_food<- {rnd(100),rnd(100)};
	
	aspect default{		
		draw square(4) at: locat_food color: #yellow;
	}
}


species information_center{
	list<point> foodstores <- [];
	list<point> thirststores <- [];

	reflex getStoreLocations when: empty(foodstores) and empty(thirststores){
		
		ask food_shop {
			add self.locat_food to: myself.foodstores;
		}
		ask thirst_shop{
			add self.locat_thirst to: myself.thirststores;
		}
	}
	
		reflex checkBadGuy
	{		
		ask guests 
		{
			
			if (infocenter distance_to (self.location) < 3)
			{
			if(self.bad_guest = true)
			{
				write"checking";
				guests target <- self;
				
				if( bad_agent and thirsty)
					{ self.mycolor <- #blue; }
				else if ( bad_agent and hungry)
					{ self.mycolor <- #yellow; }
				
				ask police
				{
					self.prey <- target;
				}	
			}
			
			}
		}
	}
	aspect default{
		draw triangle(4) at: infocenter color: #black;
	}
}

species police skills:[moving]{
	guests prey <- nil;
	bool reached<- true;
	
	reflex do_wonder when: prey= nil 	
		{ 
	 		 do goto target: location speed: 2.0;
	 		 if(location distance_to(location ) < 10)
	  		{    reached<- false;
	  			 location<- nil;
	  		}	
	 		 do wander;
		}
	
	reflex chaseAndKill when: prey != nil 
	{
		do goto target:prey.location speed: 1.5;
	
		ask guests
		{
			if (self = myself.prey)
			{
				if (myself.location distance_to (self.location) < 3)
				{
					myself.prey <- nil;
					do die;				
				}
			}
		}
		reached<- true;
	}
	aspect base{
		draw sphere(3) at: location color:#blueviolet;
	}
}


experiment guests_assignment type: gui{
	output{
		display map type: opengl{
			species guests ;
			species thirst_shop;
			species food_shop;
			species information_center;
			species police aspect:base;
			
		}
	}	
}

