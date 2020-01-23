/**
* Name: Assignment2
* Author: Khushdeep Singh
* Description: 
* Tags: Tag1, Tag2, TagN
*/

model Assignment2

/* Insert your model definition here */

global {
	geometry bounds <- rectangle ( {0,0}, {200,200});
	
	int cloth_price <- 500;
	int cd_price<- 850;
	int number_of_buyers<- 12;
	int i <-0;
	int j <- 0;
	int k<- 0;
	
	int cloth_buyers<- 0;
	int cd_buyers <- 0;
	int highest_value<- 0;
	list<int> highest<- [1,2,3,4,5,6,7,8,9,10,11,12];
	
	point dutch_selling_position<- { 80,80};
	point english_selling_position<- { 80,20};
	point leaving_place<- { 100,0};
	
	bool No_selling_dutch<- false;
	bool No_selling_english<- false; 
	bool dutch_auction_ended<- true;
	bool english_auction_ended<- true;
	
	bool reached_dutch_auction<- false;
	bool reached_english_auction<- false; 
    bool dutch_participant_move<- false; 
    bool english_participant_move<- false;
    
    bool start_english_auction<- false;
 
	init {	
		create Participant number: number_of_buyers { location<- {rnd(100),rnd(100)} ; }
		create Dutch_Initiator number: 1   { location<- flip(0.5) ? {15 + rnd(10), 70 + rnd(10)} : { 70+ rnd(10), 15+ rnd(10)}; }	 
		create English_Initiator number: 1   { location<- flip(0.5) ? {55 + rnd(10), 30 + rnd(10)} : { 10+ rnd(10), 55+ rnd(10)}; }
		create selling_place number: 1      {  }
 	   }
	}


species Dutch_Initiator skills: [fipa,moving]{
	list<Participant> part;
	
	point target_point<- nil;	
    bool motion <- true;
				
	reflex movement when: motion 
		{	target_point<- dutch_selling_position;
			dutch_auction_ended<- false;
			do goto target:target_point speed: 2.0 ;	
			if(location distance_to(target_point ) < 3){
	 				 motion<- false;  
	 				 dutch_participant_move<- true; 
	 				 write 'Dutch Auction begins' ; }
		}
		
	reflex send_request when: !motion and !dutch_auction_ended and reached_dutch_auction  {
		part<- Participant ;	
		do start_conversation to: part protocol: 'fipa-contract-net' performative: 'cfp' contents: ['go sleeping'];
		write 'selling clothes at: ' + cloth_price;
		}
		
	reflex read_agree_message when: !(empty(proposes)) and !dutch_auction_ended {
		No_selling_dutch <- true;	
		dutch_auction_ended<- true;

		loop a over: proposes{
			write 'agree message with content: ' + string(a.contents);
	 	    }  
	    }
	    
	reflex read_failure_message when: !(empty(refuses)) and empty(proposes) and !dutch_auction_ended 
		{	cloth_price<- cloth_price - 5;			
			if ( cloth_price<300)
				{ write ' Auction has been cancelled now!! ';
				  No_selling_dutch<- true;
				  dutch_auction_ended<- true;   }
          }
          
     reflex goto_die when: No_selling_dutch and dutch_auction_ended
     	{   start_english_auction<- true;
			target_point<- leaving_place;
			do goto target: target_point speed: 3.0;
			if ( location distance_to(target_point)<3)
				  	{ do die;    }
	    }      
	
	aspect default{
		draw ellipse(8,4) at: location color: #green;
	}
}

species English_Initiator skills: [fipa,moving]{
	list<Participant> part;
	
	point target_point<- nil;	
    bool motion <- true;
				
	reflex movement when: motion and start_english_auction
		{	target_point<- english_selling_position;
			english_auction_ended<- false;
			do goto target:target_point speed: 2.0 ;	
			if(location distance_to(target_point ) < 3){
	 				 motion<- false;  
	 				 english_participant_move<- true; 
	 				 write 'English Auction begins' ; }
		}
		
	reflex send_request when: !motion and !english_auction_ended and reached_english_auction {
		part<- Participant ;	
		do start_conversation to: part protocol: 'fipa-contract-net' performative: 'cfp' contents: ['go sleeping'];
		}
		
	reflex read_agree_message when: !(empty(proposes)) and !english_auction_ended {
		No_selling_english <- true;	
		english_auction_ended<- true;
		loop a over: proposes{
			write 'agree message with content: ' + string(a.contents);
	 	    }  
	    }
	    
	reflex read_failure_message when: !(empty(refuses)) and empty(proposes) and !english_auction_ended 
		{	 write ' You do not enough money for English Auction';
             write ' English Auction has been cancelled now!! ';  
             No_selling_english<- true;
			 english_auction_ended<- true; 
          }
     reflex goto_die when: No_selling_english and english_auction_ended
     	{ 
			target_point<- leaving_place;
			do goto target: target_point speed: 3.0;
			if ( location distance_to(target_point)<3)
				  	{ do die;    }
	    }      
	
	aspect default{
		draw ellipse(5,8) at: location color: #brown;
	}
}
species Participant skills: [moving,fipa] {
	
	point target_point<- nil;
	bool motion<- true;
	rgb mycolor<- #red;
	int my_price_dutch ;
	int my_price_english;
	int b<- rnd(2,3);
	bool random_movement<- true ;
	bool count<- true; 
	  
	reflex count_people when: count
	{  if( cloth_buyers + cd_buyers != number_of_buyers)
		{ if (b=2)
			{ cloth_buyers <- cloth_buyers +1;	}
		 if (b=3)
			{ cd_buyers<- cd_buyers + 1 ;	 }	
		}
		
		else if ( cloth_buyers + cd_buyers = number_of_buyers) 
		     {   	count<- false;  }
	}
	
	reflex random_move when: dutch_auction_ended and english_auction_ended
		{   
			target_point<- flip(0.5) ? {10+ rnd(10),20+ rnd(10)} : { 20+ rnd(20), 30+ rnd(30)} ;
		    do goto target: target_point speed: 3.0;
		    if( location distance_to(target_point)<10)
				 { mycolor<- #red;   }			
		}
	
	reflex goto_clothes_seller when: motion and (b=2) and  dutch_participant_move
	{ 		my_price_dutch<- rnd(250,400); 			
			mycolor<- #green;		    
		    target_point<- dutch_selling_position;
		    do goto target:target_point speed: 4.0 ; 
		    
		    if(location distance_to(target_point ) < 8){
	 			 motion<- false;
	 			 write 'Dutch ' + ( i+1) +  ' referred price is: ' + my_price_dutch;
	 	  			  if (i != cloth_buyers)
	 			  		 { i<- i+1; }
	 			}
	 	    if ( i= cloth_buyers )
	 			   { 	reached_dutch_auction<- true;  }
	   }     
	     
	reflex goto_cd_seller when: motion and (b=3) and english_participant_move
	{		my_price_english<- rnd(600,900);			
			mycolor<- #red;
		    target_point<- english_selling_position;
		    do goto target:target_point speed: 4.0; 
		    if(location distance_to(target_point ) < 3){
	 			motion<- false;
	 			write 'English ' + ( j+1) +  ' referred price is: ' + my_price_english;
	 	  			  if (j != cd_buyers+ 1)
	 			  		 {  
	 			  		 	highest[j+1]<- my_price_english ;	 
	 			  		 		  		 	
	 			  		 	if ( highest[j+1]> highest_value) 
	 			  		 	{ highest_value<- highest[j+1]; }	
	 			  		 	} 	    
       					j<- j+1;
	 			     }    
           
	 	    if ( j= cd_buyers  )
	 		{    write 'Highest possible value is '+ highest_value;
                 if (cd_price < highest_value)
                    { cd_price<- highest_value; }
             	 reached_english_auction<- true;  
             	}	   
	 	}         
	
	reflex success_dutch_message when: !(empty(cfps)) and !motion and !dutch_auction_ended and (my_price_dutch >= cloth_price) {
		dutch_auction_ended<- true; 
		No_selling_dutch <- true;
		message requestFromInitiator <- (cfps at 0);
		do propose with: (message: requestFromInitiator, contents: ['I accept']);	
		write 'selling clothes at: ' + cloth_price;
	 	write ' Auction selling was a success';		
		write ' clothes sold at: ' + (cloth_price );
		mycolor<- #blue; 
		}
	
	reflex failure_dutch_message when: !(empty(cfps)) and !motion  and !dutch_auction_ended and !No_selling_dutch and (my_price_dutch <= cloth_price) 
		{	message requestFromInitiator <- (cfps at 0);  	    
		    do refuse with: (message: requestFromInitiator, contents: []);    }
	
	reflex success_english_message when: !(empty(cfps)) and !motion and !english_auction_ended and (my_price_english >= cd_price) and reached_english_auction
	 {
		english_auction_ended<- true; 
		No_selling_english <- true;
		message requestFromInitiator <- (cfps at 0);
		do propose with: (message: requestFromInitiator, contents: ['I accept']);	
	 	write ' Auction selling was a success';		
		write ' cds sold at: ' + (cd_price );
		mycolor<- #blue;
		}
		
	reflex failure_english_message when: !(empty(cfps)) and !motion and !english_auction_ended and !No_selling_english and (my_price_english <= cd_price) 
	   { message requestFromInitiator <- (cfps at 0);  	    
		 do refuse with: (message: requestFromInitiator, contents: []);  
		 }
	
	aspect default{
		draw sphere(4) at: location color: mycolor;
		draw geometry: 'Participant' + i color: #black  size: 2 at: {location.x-6,location.y-4} ;	

		}
	}
			

species selling_place {
	aspect default{
	  	draw pyramid(5) at: dutch_selling_position color: #black ;  	
	  	}
	}
	
experiment guests_assignment type: gui{
	output{
		display map type: opengl{
			species Participant ;
			species Dutch_Initiator ;
			species English_Initiator;
			species selling_place;
		}
	}	
}